import os
import sys
from web3 import Web3
from eth_account import Account
from solcx import install_solc, set_solc_version, compile_source

RPC = "https://ethereum-sepolia-rpc.publicnode.com"
CHAIN_ID = 11155111
EXPLORER = "https://sepolia.etherscan.io"

SOURCE = '''
pragma solidity ^0.8.20;
contract IPWeaveNFT {
    string public name = "IP Weave";
    string public symbol = "IPW";
    mapping(uint256 => address) private _owners;
    uint256 private _total;
    address public owner;
    event Minted(uint256 tokenId, address to);

    constructor() { owner = msg.sender; }

    function mint(address to) public returns (uint256) {
        require(msg.sender == owner);
        _total++;
        _owners[_total] = to;
        emit Minted(_total, to);
        return _total;
    }

    function ownerOf(uint256 id) public view returns (address) {
        return _owners[id];
    }

    function totalSupply() public view returns (uint256) {
        return _total;
    }
}
'''


def deploy(private_key):
    install_solc("0.8.20")
    set_solc_version("0.8.20")

    w3 = Web3(Web3.HTTPProvider(RPC))
    if not w3.is_connected():
        print("无法连接 Sepolia RPC")
        return False

    acct = Account.from_key(private_key)
    balance = w3.eth.get_balance(acct.address)
    eth = w3.from_wei(balance, "ether")
    print(f"钱包: {acct.address}")
    print(f"余额: {eth} ETH")

    if balance < w3.to_wei(0.003, "ether"):
        print(f"余额不足，需要至少 0.003 ETH")
        return False

    compiled = compile_source(SOURCE, output_values=["abi", "bin"])
    data = list(compiled.values())[0]
    abi, bytecode = data["abi"], "0x" + data["bin"]

    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    nonce = w3.eth.get_transaction_count(acct.address)

    try:
        gas_est = contract.constructor().estimate_gas({"from": acct.address})
    except:
        gas_est = 200000

    tx = contract.constructor().build_transaction({
        "from": acct.address,
        "nonce": nonce,
        "gas": max(gas_est + 50000, 250000),
        "maxFeePerGas": w3.to_wei(5, "gwei"),
        "maxPriorityFeePerGas": w3.to_wei(1, "gwei"),
        "chainId": CHAIN_ID,
    })

    cost = tx["gas"] * tx["maxFeePerGas"]
    print(f"Gas 上限: {tx['gas']}")
    print(f"Gas 价格: 5 gwei")
    print(f"预估费用: {w3.from_wei(cost, 'ether')} ETH")

    if balance < cost:
        print(f"余额不足，需要 {w3.from_wei(cost, 'ether')} ETH")
        return False

    print("正在部署...")
    signed = acct.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    print(f"交易已发送: 0x{tx_hash.hex()}")
    print(f"等待确认...")

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)

    if receipt["status"] == 1:
        addr = receipt["contractAddress"]
        print(f"部署成功!")
        print(f"合约地址: {addr}")
        print(f"{EXPLORER}/address/{addr}")

        print("\n铸造 NFT...")
        nonce2 = w3.eth.get_transaction_count(acct.address)
        mint_tx = contract(addr).functions.mint(acct.address).build_transaction({
            "from": acct.address,
            "nonce": nonce2,
            "gas": 80000,
            "maxFeePerGas": w3.to_wei(5, "gwei"),
            "maxPriorityFeePerGas": w3.to_wei(1, "gwei"),
            "chainId": CHAIN_ID,
        })
        signed2 = acct.sign_transaction(mint_tx)
        tx_hash2 = w3.eth.send_raw_transaction(signed2.raw_transaction)
        receipt2 = w3.eth.wait_for_transaction_receipt(tx_hash2, timeout=60)

        if receipt2["status"] == 1:
            print(f"铸造成功! Token #1")
            print(f"{EXPLORER}/tx/0x{tx_hash2.hex()}")
        else:
            print("铸造失败")

        return True
    else:
        print(f"部署失败，gas 使用: {receipt['gasUsed']}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python deploy.py <私钥>")
        sys.exit(1)
    deploy(sys.argv[1])
