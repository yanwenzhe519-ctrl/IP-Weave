import os, json
from web3 import Web3
from eth_account import Account

RPC = "https://ethereum-sepolia-rpc.publicnode.com"
CHAIN_ID = 11155111
EXPLORER = "https://sepolia.etherscan.io"

class WalletManager:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(RPC))
        self.account = None
        self.address = ""

    def create_wallet(self):
        acct = Account.create("ipw_" + os.urandom(4).hex())
        self.account = acct
        self.address = acct.address
        return {"address": acct.address, "private_key": acct.key.hex()}

    def import_key(self, key):
        try:
            self.account = Account.from_key(key)
            self.address = self.account.address
            return True
        except:
            return False

    def get_balance(self):
        if not self.address:
            return 0
        bal = self.w3.eth.get_balance(self.address)
        return self.w3.from_wei(bal, "ether")

    def send_eth(self, to_addr, amount):
        if not self.account:
            return None
        tx = {"from": self.address, "to": to_addr,
              "value": self.w3.to_wei(amount, "ether"),
              "nonce": self.w3.eth.get_transaction_count(self.address),
              "gas": 21000,
              "maxFeePerGas": self.w3.to_wei(5, "gwei"),
              "maxPriorityFeePerGas": self.w3.to_wei(1, "gwei"),
              "chainId": CHAIN_ID}
        signed = self.account.sign_transaction(tx)
        tx_hash = self.w3.eth.send_raw_transaction(signed.raw_transaction)
        return self.w3.to_hex(tx_hash)

    def deploy_nft(self, token_uri, recipient=None):
        from solcx import install_solc, set_solc_version, compile_source
        install_solc("0.8.20")
        set_solc_version("0.8.20")
        src = "\n".join(['pragma solidity ^0.8.20;', 'contract IPWeaveNFT {', '    string public name = "IP Weave";', '    string public symbol = "IPW";', '    mapping(uint256 => address) private _owners;', '    mapping(uint256 => string) private _uris;', '    uint256 private _total;', '    address public owner;', '    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);', '    constructor() { owner = msg.sender; }', '    function mint(address to, string memory uri) public returns (uint256) {', '        require(msg.sender == owner);', '        _total++;', '        _owners[_total] = to;', '        _uris[_total] = uri;', '        emit Transfer(address(0), to, _total);', '        return _total;', '    }', '    function ownerOf(uint256 id) public view returns (address) { return _owners[id]; }', '    function tokenURI(uint256 id) public view returns (string memory) { return _uris[id]; }', '}'])
        compiled = compile_source(src, output_values=["abi", "bin"])
        data = list(compiled.values())[0]
        abi, bytecode = data["abi"], "0x" + data["bin"]
        contract = self.w3.eth.contract(abi=abi, bytecode=bytecode)
        nonce = self.w3.eth.get_transaction_count(self.address)
        try:
            gas_est = contract.constructor().estimate_gas({"from": self.address})
        except:
            gas_est = 500000
        tx = contract.constructor().build_transaction({
            "from": self.address, "nonce": nonce,
            "gas": int(gas_est * 1.2) + 50000,
            "maxFeePerGas": self.w3.to_wei(5, "gwei"),
            "maxPriorityFeePerGas": self.w3.to_wei(1, "gwei"),
            "chainId": CHAIN_ID})
        signed = self.account.sign_transaction(tx)
        tx_hash = self.w3.eth.send_raw_transaction(signed.raw_transaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)
        if receipt["status"] == 1:
            addr = receipt["contractAddress"]
            if token_uri and recipient:
                c = self.w3.eth.contract(address=addr, abi=abi)
                nonce2 = self.w3.eth.get_transaction_count(self.address)
                mt = c.functions.mint(recipient, token_uri).build_transaction({
                    "from": self.address, "nonce": nonce2, "gas": 200000,
                    "maxFeePerGas": self.w3.to_wei(5, "gwei"),
                    "maxPriorityFeePerGas": self.w3.to_wei(1, "gwei"),
                    "chainId": CHAIN_ID})
                s2 = self.account.sign_transaction(mt)
                h2 = self.w3.eth.send_raw_transaction(s2.raw_transaction)
                self.w3.eth.wait_for_transaction_receipt(h2, timeout=60)
            return {"contract": addr, "tx": tx_hash.hex()}
        return None
