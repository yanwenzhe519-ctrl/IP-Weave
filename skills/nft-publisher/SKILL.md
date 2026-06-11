---
name: nft-publisher
description: 将衍生内容打包为 NFT 并部署到 Sepolia 测试网
model: glm-5.1
when: 需要将内容上链时
---

# NFT Publisher

将 Agent 生成的衍生内容打包为 NFT 元数据，编译 Solidity 合约，部署到 Sepolia 测试网。

## 用法

```python
python deploy.py YOUR_PRIVATE_KEY
```

## 输出

- metadata.json: OpenSea 标准 NFT 元数据
- IPWeaveNFT.sol: ERC-721 合约代码
- DEPLOY_README.md: 部署指南

## 链上证明

部署后可在 Sepolia Etherscan 查看：
https://sepolia.etherscan.io/address/合约地址
