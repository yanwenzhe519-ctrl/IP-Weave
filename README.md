# IP Weave

基于 GLM-5.1 的自治链上 IP 衍生内容 Agent。给一个链上 IP，它还你一个世界。

---

## 项目背景

链上 IP（NFT 藏品、数字艺术作品、Meme 代币等）在发行后普遍面临内容运营断层的问题。衍生内容创作门槛高、风格难以统一，导致大量链上 IP 陷入"沉睡"。

IP Weave 是一个基于 GLM-5.1 的 ReAct Agent，以总指挥 + 技能模块的架构，自主完成从创意输入到链上交付的完整内容生产链路：

创意输入 -> 资料收集 -> 风格分析 -> 内容创作 -> 质量检查 -> 链上发布

一人 + 一个 Agent，完成过去需要整个创作团队才能完成的事。

---

## 安装与运行

### 前置要求

- Python 3.10 或更高版本
- GLM-5.1 API Key（获取方式见下文）

### 安装步骤

git clone https://github.com/yanwenzhe519-ctrl/IP-Weave.git
cd IP-Weave
pip install install -r requirements.txt
cp .env.example .env

编辑 .env 文件，填入你的 ZHIPUAI_API_KEY。

### 运行

set PYTHONPATH=%CD%
echo azuki | python src\run_agent.py

输入任意链上 IP 名称（bayc, punk, azuki, pudgy 等）或 ERC-721 合约地址，Agent 自主执行全部流程。

---

## 核心功能

IP Weave 实现了从创意输入到链上交付的完整内容生产链路：

1. 链上 IP 数据读取
   功能：自动读取任意 ERC-721 合约的链上数据
   输入：IP 名称或合约地址
   输出：IP 名称、描述、属性列表、tokenURI 元数据

2. IP 风格分析
   功能：GLM-5.1 提取 IP 独有的视觉风格、叙事基调、文化背景、代表符号
   输出：风格画像（含 lore、character、key_symbols、cultural_reference）

3. 衍生故事创作
   功能：基于 IP 独有的世界观和角色设定创作衍生故事
   输出：2000-4000 字完整叙事，含起因、发展、转折、高潮、收束

4. 动画分镜脚本生成
   功能：将故事转化为专业动画分镜脚本
   输出：6-8 个分镜，每个含场景描述、对白、镜头运动、时长

5. 周边资产概念设计
   功能：设计可上链的周边资产概念
   输出：2 款资产设计，含设计描述、理念说明、NFT 元数据、AI 生成图片

6. 风格一致性检查
   功能：GLM-5.1 评估内容与 IP 风格的匹配度
   标准：7 分以上通过，低于 7 分自动迭代修正

7. 链上发布准备
   功能：将衍生内容打包为 NFT 元数据，生成 Solidity 合约
   输出：metadata.json、IPWeaveNFT.sol、部署指南

---

## 技术架构

+--------------------------------------------------------------------------+
|                         IP Weave Agent                                    |
|                    总指挥：GLM-5.1 自主决策                                |
+--------------------------------------------------------------------------+
       |                          |                         |
       v                          v                         v
+-------------+    +----------------------+    +------------------+
| ip_reader   |    |  content_creator     |    |  nft_publisher   |
| 读取链上数据 |    |  分析风格/创作内容   |    |  打包/上链       |
+-------------+    +----------------------+    +------------------+
       |                    |       |       |            |
       v                    v       v       v            v
   以太坊主网            GLM-5.1  CogView   GLM-5.1    Sepolia 测试网
                        API      API      API

### 工作流程

1. Agent 收到 IP 名称
2. ip_reader 从以太坊主网读取真实链上数据
3. style_analyzer 用 GLM-5.1 提取风格指纹
4. content_creator 用 GLM-5.1 创作故事
5. script_creator 用 GLM-5.1 生成分镜脚本
6. asset_designer 设计资产概念 + 调用 CogView 出图
7. 质量检查，不合格自动迭代
8. nft_publisher 打包元数据，生成合约
9. 部署到 Sepolia 测试网

---

## 使用到的 API / SDK / AI 工具

1. GLM-5.1（Z.AI Coding Plan）
   用途：Agent 核心 LLM，负责全部决策、分析、创作、检查
   使用位置：src/utils/llm.py（API 封装）、全部技能模块
   效果：自主规划创作方向、生成 3000+ 字高质量故事、评估风格一致性

2. CogView-4（智谱 AI）
   用途：周边资产图片生成
   使用位置：src/utils/llm.py generate_image() 方法
   效果：根据设计描述生成资产概念图（需 API 额度）

3. web3.py
   用途：以太坊链上数据读取和合约交互
   使用位置：src/chain/reader.py、src/agent/react_agent.py _deploy_to_sepolia()
   效果：实时读取 ERC-721 合约元数据，部署合约到 Sepolia

4. solc（Solidity 编译器）
   用途：编译 ERC-721 智能合约
   使用位置：src/agent/react_agent.py _deploy_to_sepolia()
   效果：将 Solidity 源码编译为 EVM bytecode 并部署

5. python-dotenv
   用途：加载 .env 环境变量配置
   使用位置：src/config.py
   效果：安全管理 API Key

6. httpx
   用途：HTTP 客户端调用 GLM-5.1 API
   使用位置：src/utils/llm.py
   效果：向智谱 API 发送请求和接收响应

---

## 链上 / 测试网证据

网络：Sepolia Testnet（Chain ID: 11155111）
RPC：https://ethereum-sepolia-rpc.publicnode.com

### 合约地址

0x1E70f147e4EE4Ef2Feb533DC5a8580C791e1a507
https://sepolia.etherscan.io/address/0x1E70f147e4EE4Ef2Feb533DC5a8580C791e1a507

### 部署交易哈希

0x0739ad31e20dfb332e7498babc8919cc657615977974ef3b0a400d1942adabc1
https://sepolia.etherscan.io/tx/0x0739ad31e20dfb332e7498babc8919cc657615977974ef3b0a400d1942adabc1

### 铸造交易哈希

0x257dc02496bffb892f1a4a6fa66423a5c63a00649ee7c987140da8c6f43b7d59
https://sepolia.etherscan.io/tx/0x257dc02496bffb892f1a4a6fa66423a5c63a00649ee7c987140da8c6f43b7d59

### Agent Wallet 地址

0x3C215983f524271a4aB1A11E041cDC01ca84B9EC
该钱包由 Agent 自动生成，用于 Sepolia 测试网的合约部署和 NFT 铸造。钱包私钥仅在本地使用，不会上传或泄露。测试网 ETH 无实际经济价值。

### 操作记录

Agent 每次运行会自动记录完整操作日志，保存在 output/{IP名称}/run_record.json 中。

---

## 安全与合规边界

1. API Key 安全
   API Key 仅存于本地 .env 文件，已加入 .gitignore 不会被上传到 GitHub

2. 链上操作权限
   合约部署使用测试网临时钱包，仅用于 Sepolia 测试网
   不支持主网操作，不涉及真实资产
   私钥仅在本地代码中使用

3. 失败处理
   API 调用超时自动重试一次
   CogView 出图失败不影响核心内容生成流程
   合约部署失败时记录错误日志，不自动重试

4. 人工介入条件
   部署到测试网需要钱包有足够 Sepolia ETH
   如连续 15 轮循环仍未达到质量标准，Agent 自动终止

5. 第三方工具说明
   所有使用的 API、SDK、开源工具均在 README 中列出
   GLM-5.1 和 CogView-4 为商业 API，需自行获取密钥

---

## 项目完成度与后续计划

### 当前完成

- GLM-5.1 API 调用封装（含超时重试）
- 链上 IP 数据实时读取（以太坊主网）
- IP 风格分析（含 lore、character、key_symbols）
- 衍生故事创作
- 动画分镜脚本生成
- 周边资产概念设计 + AI 出图
- 风格一致性检查 + 迭代修正
- NFT 元数据打包 + Solidity 合约生成
- ReAct Agent 自主决策循环
- 总指挥 + 技能模块架构

### 后续计划

- 接入 Seedance 2.0 实现视频生成
- 自动化 IPFS 上传
- Web 界面
- 批量 IP 处理

---

## 架构图

Agent (总指挥)                    Skills (执行单元)
+------------------+           +---------------------+
| GLM-5.1 决策循环  |  --调用-> | ip_reader           |
|                  |           | style_analyzer      |
| 1. 分析状态       |           | content_creator     |
| 2. 选择技能       |           | script_creator      |
| 3. 派发参数       |           | asset_designer      |
| 4. 评估结果       |           | nft_publisher       |
| 5. 迭代/完成      |           +---------------------+
+------------------+                      |
       |                                  v
       v                            +-----------+
   GLM-5.1 API                      | 以太坊链上 |
                                    +-----------+

---

## 相关链接

GitHub: https://github.com/yanwenzhe519-ctrl/IP-Weave
Etherscan: https://sepolia.etherscan.io/address/0x1E70f147e4EE4Ef2Feb533DC5a8580C791e1a507
Casual Hackathon: https://casualhackathon.com
Z.AI (GLM-5.1): https://z.ai

---

## 许可

MIT
