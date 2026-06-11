"""链上发布模块 — 将 Agent 产出准备为 NFT 并部署到测试网"""

import os
import json
import subprocess
from pathlib import Path
from loguru import logger
from src.config import settings


class NFTPublisher:
    """将衍生内容打包为 NFT 并准备部署"""

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.nft_dir = os.path.join(output_dir, "nft")
        os.makedirs(self.nft_dir, exist_ok=True)

    def prepare_metadata(self, ip_name: str, story_text: str,
                         script_text: str, assets: dict) -> dict:
        """
        第一步：将 Agent 产出打包为 NFT 元数据
        生成 ERC-721 标准的 metadata JSON
        """
        logger.info("→ [上链] 打包 NFT 元数据...")

        # 保存故事和脚本为 IPFS-ready 文件
        with open(os.path.join(self.nft_dir, "story.txt"), "w", encoding="utf-8") as f:
            f.write(story_text)
        with open(os.path.join(self.nft_dir, "script.txt"), "w", encoding="utf-8") as f:
            f.write(script_text)

        # 生成 NFT 元数据
        metadata = {
            "name": f"IP Weave · {ip_name}",
            "description": f"由 IP Weave Agent 基于 {ip_name} 链上 IP 自主生成的衍生内容 NFT。"
                           f"包含衍生故事、动画分镜脚本和周边资产概念设计。",
            "image": "ipfs://QmPlaceholder/image.png",
            "attributes": [
                {"trait_type": "IP", "value": ip_name},
                {"trait_type": "生成引擎", "value": "GLM-5.1"},
                {"trait_type": "内容类型", "value": "衍生故事 + 动画脚本 + 周边资产"},
                {"trait_type": "生成时间", "value": self._timestamp()},
            ],
            "properties": {
                "files": [
                    {"uri": "ipfs://QmPlaceholder/story.txt", "type": "text/markdown"},
                    {"uri": "ipfs://QmPlaceholder/script.txt", "type": "text/markdown"},
                ],
                "creators": [{"address": "0x...（部署者钱包）", "share": 100}]
            }
        }

        meta_path = os.path.join(self.nft_dir, "metadata.json")
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        logger.success(f"  NFT 元数据已生成: {meta_path}")
        return metadata

    def generate_deploy_script(self) -> str:
        """
        第二步：生成 Solidity 合约 + 部署脚本（Foundry/Hardhat 兼容）
        用户只需一条命令即可部署
        """
        logger.info("→ [上链] 生成部署脚本...")

        # 生成一个简单的 ERC-721 合约
        contract_code = '''// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";

/// @title IP Weave - 链上衍生内容 NFT
/// @notice 由 IP Weave Agent 基于 GLM-5.1 自主生成
contract IPWeaveNFT is ERC721, Ownable {
    using Strings for uint256;

    uint256 private _tokenIdCounter;
    string private _baseTokenURI;

    constructor(string memory name, string memory symbol, string memory baseURI)
        ERC721(name, symbol)
        Ownable(msg.sender)
    {
        _baseTokenURI = baseURI;
    }

    function safeMint(address to) public onlyOwner returns (uint256) {
        _tokenIdCounter++;
        uint256 tokenId = _tokenIdCounter;
        _safeMint(to, tokenId);
        return tokenId;
    }

    function _baseURI() internal view override returns (string memory) {
        return _baseTokenURI;
    }

    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        _requireOwned(tokenId);
        return bytes(_baseTokenURI).length > 0
            ? string(abi.encodePacked(_baseTokenURI, tokenId.toString(), ".json"))
            : "";
    }
}
'''
        contract_path = os.path.join(self.nft_dir, "IPWeaveNFT.sol")
        with open(contract_path, "w", encoding="utf-8") as f:
            f.write(contract_code)

        # 生成部署脚本
        deploy_script = '''// SPDX-License-Identifier: MIT
// 部署脚本 — Foundry 用法:
// forge script Deploy.s.sol --rpc-url $RPC_URL --private-key $PRIVATE_KEY --broadcast

pragma solidity ^0.8.20;

import "forge-std/Script.sol";
import "../IPWeaveNFT.sol";

contract DeployScript is Script {
    function run() external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        address deployer = vm.addr(deployerPrivateKey);

        vm.startBroadcast(deployerPrivateKey);

        IPWeaveNFT nft = new IPWeaveNFT(
            "IP Weave Derivative",
            "IPW",
            "ipfs://YOUR_CID_HERE/"
        );

        // 铸造第一个衍生内容 NFT
        nft.safeMint(deployer);

        vm.stopBroadcast();

        console.log("NFT deployed at:", address(nft));
        console.log("Token #1 minted to:", deployer);
    }
}
'''
        deploy_path = os.path.join(self.nft_dir, "Deploy.s.sol")
        with open(deploy_path, "w", encoding="utf-8") as f:
            f.write(deploy_script)

        # 生成 README 部署说明
        readme = f"""# NFT 部署指南

## 前置要求
1. 安装 Foundry: `curl -L https://foundry.paradigm.xyz | bash`
2. 安装依赖: `forge install OpenZeppelin/openzeppelin-contracts`
3. 准备测试网 ETH（从 https://sepoliafaucet.com 领取）

## 部署步骤

```bash
# 1. 部署合约
forge script Deploy.s.sol \\
  --rpc-url https://sepolia.infura.io/v3/YOUR_KEY \\
  --private-key YOUR_TEST_WALLET_KEY \\
  --broadcast

# 2. 验证合约（可选）
forge verify-contract <合约地址> IPWeaveNFT \\
  --chain sepolia
```

## 安全说明
- 使用**测试网私钥**，不要用主网钱包
- 测试网 ETH 免费，无实际价值
- 部署后合约归你所有，可自由铸造

## 生成的 NFT 元数据
- metadata.json — OpenSea 标准的 NFT 元数据
- story.txt — 衍生故事全文
- script.txt — 动画分镜脚本
"""
        readme_path = os.path.join(self.nft_dir, "DEPLOY_README.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme)

        logger.success(f"  📜 合约已生成: {contract_path}")
        logger.success(f"  📋 部署指南: {readme_path}")
        return str(contract_path)

    def generate_burner_wallet(self) -> dict:
        """
        第三步：生成一个临时测试钱包（仅供 Demo 使用）
        用户需从水龙头领测试 ETH 后才能部署
        """
        logger.info("→ [上链] 生成测试钱包...")
        try:
            # 尝试用 web3 生成钱包（如果安装了）
            result = subprocess.run(
                ["python", "-c", """
from web3 import Web3
w3 = Web3()
acct = w3.eth.account.create('ip_weave_demo')
print(acct.address)
print(acct.key.hex())
"""],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                wallet = {
                    "address": lines[0],
                    "private_key": lines[1],
                    "mnemonic": "(随机生成，用完即弃)"
                }
            else:
                raise Exception("web3 not available")
        except Exception:
            # 纯 Python 生成钱包（无依赖）
            import hashlib
            import secrets
            priv = secrets.token_hex(32)
            wallet = {
                "address": f"0x{hashlib.sha256(priv.encode()).hexdigest()[:40]}",
                "private_key": f"0x{priv}",
                "mnemonic": "(随机生成，仅用于测试网)"
            }

        # 保存钱包信息（警告：仅用于测试网）
        wallet_path = os.path.join(self.nft_dir, "test_wallet.json")
        with open(wallet_path, "w") as f:
            json.dump(wallet, f, indent=2)

        logger.info(f"  💳 测试钱包地址: {wallet['address']}")
        logger.info(f"  ⚠️  仅用于测试网！需从水龙头领测试 ETH")
        logger.info(f"  水龙头: https://sepoliafaucet.com")
        return wallet

    def _timestamp(self) -> str:
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
