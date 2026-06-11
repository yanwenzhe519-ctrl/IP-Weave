---
name: IP-Weave
description: 链上 IP 衍生内容 Agent — 基于 GLM-5.1 的自主创作 Agent
model: glm-5.1
when: 用户需要为链上 IP 生成衍生故事、动画脚本、周边资产并上链时
---

# IP Weave

基于 GLM-5.1 的 ReAct Agent。给一个链上 IP 名称或合约地址，自动完成全部创作流程。

## 使用方法

在 Claude Code 中输入：
帮我跑 IP Weave，用 bayc
或者：用 IP Weave 生成 pepe 的衍生内容

## 执行步骤

1. 先确认当前目录是 IP-Weave 项目根目录
2. 设置环境变量：export PYTHONPATH=$(pwd)
3. 运行命令：python src/run_agent.py
4. 当提示"链上 IP 名称或合约地址"时，输入用户指定的 IP 名称

## 工作流

Agent 会自主执行以下步骤：
1. 读取链上 IP 数据（从以太坊主网）
2. GLM-5.1 分析风格指纹
3. GLM-5.1 制定创作计划
4. 创作衍生故事（2000 字以上）
5. 生成动画分镜脚本（6 个分镜）
6. 设计周边资产概念（2 款）
7. 风格一致性检查（低于 7 分自动重做）
8. 部署合约到 Sepolia 测试网
9. 铸造 NFT（元数据直接写入链上）

## 预设 IP 名称

- pepe: Pepe the Frog
- bayc: Bored Ape Yacht Club
- punk: CryptoPunks
- azuki: Azuki

也可直接输入任意 ERC-721 合约地址。
