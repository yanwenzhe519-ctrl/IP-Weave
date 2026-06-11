---
name: IP-Weave
description: 链上 IP 衍生内容 Agent — 基于 GLM-5.1 的自主创作 Agent
model: glm-5.1
when: 用户需要为链上 IP 生成衍生故事、动画脚本、周边资产并上链时
---

# IP Weave

基于 GLM-5.1 的 ReAct Agent。给一个链上 IP 名称或合约地址，自动完成全部创作流程。

## 用法

在 Claude Code 中直接说：

"帮我跑 IP Weave，用 Pepe"
"用 BAYC 链上 IP 生成衍生内容"
"给合约地址 0x... 生成故事、脚本、资产并上链"

## 工作流

Agent 会自主执行以下 9 步：

1. 读取链上 IP 数据（名称、描述、属性）
2. 用 GLM-5.1 分析风格指纹（视觉、叙事、氛围）
3. 用 GLM-5.1 制定创作计划
4. 创作衍生故事（2000 字以上）
5. 生成动画分镜脚本（6 个分镜）
6. 设计周边资产概念（2 款）
7. 风格一致性检查（低于 7 分自动重做）
8. 部署合约到 Sepolia 测试网并铸造 NFT
9. 交付成果

## 预设 IP

| 名称 | 说明 |
|------|------|
| pepe | Pepe the Frog |
| bayc | Bored Ape Yacht Club |
| punk | CryptoPunks |
| azuki | Azuki |

也可直接输入任意 ERC-721 合约地址。

## 输出

运行后 output/ 目录下生成：
- 衍生故事（HTML）
- 动画分镜脚本（HTML）
- 周边资产概念设计（HTML + SVG）
- NFT 元数据和 Solidity 合约

## 链上证明

合约部署到 Sepolia 测试网后，可在 Etherscan 查看。

## 安装

```bash
git clone https://github.com/yanwenzhe519-ctrl/IP-Weave.git
cd IP-Weave
pip install -r requirements.txt
cp .env.example .env
# 填写你的 ZHIPUAI_API_KEY
```
