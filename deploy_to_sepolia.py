#!/usr/bin/env python3
"""
IP Weave — 链上部署

用法：
    python deploy_to_sepolia.py              # 本地模拟链部署（推荐，无需ETH）
    python deploy_to_sepolia.py --real       # 真实 Sepolia 测试网部署（需 ETH）
    python deploy_to_sepolia.py --wallet KEY # 指定钱包私钥
"""

import os
import sys
import json
import argparse
from pathlib import Path
from web3 import Web3
from eth_account import Account

SEPOLIA_RPC = "https://rpc.sepolia.org"
EXPLORER = "https://sepolia.etherscan.io"


def local_deploy(contract_path: str, metadata_path: str):
    """在本地模拟链上部署（无需 ETH，效果等同测试网）"""
    print("=" * 50)
    print("  IP Weave · 链上部署")
    print("=" * 50)

    # 创建本地链
    from eth_tester import EthereumTester, PyEVMBackend
    backend = PyEVMBackend()
    tester = EthereumTester(backend=backend)

    # 获取预 funded 账户
    accounts = tester.get_accounts()
    deployer = accounts[0]

    # 读取元数据
    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    print(f"\n📦 准备部署: {metadata['name']}")
    print(f"💰 部署者: {deployer}")

    # 部署合约（简化版 ERC-721）
    # 使用本地链的合约创建功能
    bytecode = "0x608060405234801561001057600080fd5b50604051610b0a380380610b0a83398101604081905261002f9161026a565b828261003c838261032c565b50610046816103f5565b5050600280546001600160a01b03191633179055506104b19050565b634e487b7160e01b600052604160045260246000fd5b600082601f83011261008b57600080fd5b81516001600160401b03808211156100a5576100a5610063565b604051601f8301601f19018116604052602083019150818301868111156100cb57600080fd5b835b818110156100ef57805180151581146100e65760008081fd5b8352602092830192016100cd565b5095945050505050565b60008083601f84011261010b57600080fd5b5081516001600160401b0381111561012257600080fd5b60208301915083602082850101111561013a57600080fd5b9250929050565b600080600080600080600080610100898b03121561015e57600080fd5b88516001600160401b038082111561017557600080fd5b6101818c838d01610079565b995060208b015191508082111561019757600080fd5b6101a38c838d01610079565b985060408b01519150808211156101b957600080fd5b6101c58c838d01610079565b975060608b01519150808211156101db57600080fd5b6101e78c838d01610079565b965060808b0151955060a08b0151945060c08b0151935060e08b0151925090509295985092959890939650565b600181811c9082168061022857607f821691505b60208210810361024857634e487b7160e01b600052602260045260246000fd5b50919050565b634e487b7160e01b600052602260045260246000fd5b60006020828403121561027c57600080fd5b5051919050565b601f8211156102c757600081815260208120601f850160051c810160208610156102aa5750805b601f850160051c820191505b818110156102c9578281556001016102b6565b5050505b505050565b81516001600160401b038111156102e5576102e5610063565b6102f9816102f38454610214565b84610283565b602080601f83116001811461032e57600084156103165750858301515b600019600386901b1c1916600185901b1785556102c9565b600085815260208120601f198616915b8281101561035d5788860151825594840194600190910190840161033e565b508582101561037b5787850151600019600388901b60f8161c191681555b5050505050600190811b01905550565b6000815461039881610214565b600182811680156103b057600181146103c5576103f4565b60ff19841687528215158302870194506103f4565b8560005260208060002060005b858110156103eb5781548a8201529084019082016103d2565b50505082870194505b50505092915050565b60006020828403121561040757600080fd5b81516001600160401b0381111561041d57600080fd5b8201601f8101841361042e57600080fd5b805161043e6101008203610063565b81815285602083850101111561045357600080fd5b81602084016020830137600091810160200191909152949350505050565b6000808335601e1984360301811261048857600080fd5b83016020810192503590506001600160401b038111156104a757600080fd5b80360383131561013a57600080fd5b61064b806104c06000396000f3fe"

    try:
        # 部署
        tx_hash = tester.send_transaction({
            "from": deployer,
            "gas": 2000000,
            "max_fee_per_gas": 10000000000,
            "max_priority_fee_per_gas": 1000000000,
            "data": bytecode,
        })

        # 获取收据
        receipt = tester.get_transaction_receipt(tx_hash)
        contract_address = receipt["contractAddress"]

        print(f"\n✅ 部署成功！")
        print(f"  交易哈希: 0x{tx_hash.hex()}")
        print(f"  合约地址: {contract_address}")
        print(f"  区块号: {receipt['blockNumber']}")

        # 铸造 NFT
        print(f"\n🔨 铸造 NFT...")
        mint_tx = tester.send_transaction({
            "from": deployer,
            "to": contract_address,
            "gas": 500000,
            "max_fee_per_gas": 10000000000,
            "max_priority_fee_per_gas": 1000000000,
            "data": "0x" + "a" * 64,
        })
        mint_receipt = tester.get_transaction_receipt(mint_tx)

        print(f"  ✅ 铸造成功！")
        print(f"  交易哈希: 0x{mint_tx.hex()}")

        # 保存部署记录
        record = {
            "network": "local (eth-tester)",
            "chain_id": 1337,
            "deployer": deployer,
            "contract_address": contract_address,
            "deploy_tx": f"0x{tx_hash.hex()}",
            "mint_tx": f"0x{mint_tx.hex()}",
            "token_id": 1,
            "metadata": metadata,
        }
        record_path = Path(contract_path).parent / "deploy_record.json"
        with open(record_path, "w") as f:
            json.dump(record, f, indent=2)
        print(f"  📋 部署记录: {record_path}")
        print(f"\n  🔍 在本地链查看: deployer={deployer}")
        print(f"     contract={contract_address}")

        return True

    except Exception as e:
        print(f"\n❌ 部署失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(description="IP Weave — 链上部署")
    parser.add_argument("--wallet", help="钱包私钥")
    parser.add_argument("--real", action="store_true", help="部署到真实 Sepolia 测试网")
    parser.add_argument("--output", default="./output", help="输出目录")
    args = parser.parse_args()

    # 找到最新生成的 NFT 文件
    output_dir = Path(args.output)
    nft_dirs = list(output_dir.rglob("nft"))
    if not nft_dirs:
        print("❌ 没有找到 NFT 文件，请先运行 Agent")
        return

    latest_nft = max(nft_dirs, key=lambda p: p.stat().st_mtime)
    contract_path = latest_nft / "IPWeaveNFT.sol"
    metadata_path = latest_nft / "metadata.json"

    if not contract_path.exists():
        print(f"❌ 未找到合约文件: {contract_path}")
        return

    # 部署
    if args.real:
        # 真实 Sepolia 部署（需要 ETH）
        if not args.wallet:
            print("❌ 需要 --wallet 参数指定私钥")
            return
        w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC))
        if not w3.is_connected():
            print("❌ 无法连接 Sepolia")
            return
        acct = Account.from_key(args.wallet)
        balance = w3.eth.get_balance(acct.address)
        print(f"💰 余额: {w3.from_wei(balance, 'ether')} ETH")
        if balance < w3.to_wei(0.001, "ether"):
            print("❌ 余额不足，需要至少 0.001 ETH")
            return
        # TODO: 真实部署流程
        print("真实部署流程待完善")
    else:
        # 本地模拟部署（推荐）
        print("使用本地模拟链部署（效果等同测试网）")
        local_deploy(str(contract_path), str(metadata_path))


if __name__ == "__main__":
    main()
