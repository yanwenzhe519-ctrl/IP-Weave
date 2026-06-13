# IP Weave

基于 GLM-5.1 的自治链上 IP 衍生内容 Agent。给一个链上 IP，它还你一个世界。

---

## 项目背景

链上 IP 资产在发行后普遍面临一个核心困境：mint 即终点。大量 NFT 项目在发售结束后缺乏持续的内容运营能力，社区成员想参与衍生创作但受限于专业技能（写作、分镜、设计），自发产出的内容质量参差不齐且风格难以统一。这导致大量链上 IP 陷入沉睡，其文化和商业价值远未被充分挖掘。

传统的内容生产需要完整的创作团队：作家负责故事创作、编剧负责分镜脚本、设计师负责视觉和周边、3D 建模师负责数字资产、开发者负责上链部署。这个过程周期长、成本高、协调复杂。

IP Weave 的目标是用一个 AI Agent 替代整个人类创作团队。一人加一 Agent，完成从创意输入到链上交付的完整内容生产链路。Agent 自主完成需求理解、资料收集、风格分析、内容创作、质量检查和链上发布，全程无需人工介入。

这个项目的核心价值在于将 Web3 内容生产的成本降低一个数量级，同时保证产出质量的稳定和风格的统一。

---

## 解决的问题

IP Weave 解决了链上 IP 生态中三个核心问题：

第一，内容生产门槛高。NFT 持有者想为持有的 IP 创作衍生内容，但缺乏写作、分镜、设计等专业技能。IP Weave 让用户只需要输入一个 IP 名称或合约地址，Agent 自动完成全部创作流程。

第二，风格不统一。社区自发创作的内容风格参差，难以与原始 IP 的视觉和叙事风格对齐。IP Weave 通过 GLM-5.1 深度分析每个 IP 的独特风格特征，确保所有产出在视觉和叙事上与原始 IP 保持一致。

第三，缺乏变现路径。衍生内容创作后缺少上链变现的渠道。IP Weave 自动将生成内容打包为 NFT 元数据，生成 Solidity 智能合约，支持部署到 Sepolia 测试网验证。

---

## 为什么能做到自主决策

IP Weave 采用 ReAct（Reasoning + Acting）架构，GLM-5.1 在每个循环中分析当前状态并自主决定下一步动作。每轮循环中 Agent 会评估已经完成了什么、还缺什么、下一步最应该做什么。这不是按固定顺序执行的流水线，而是真实的思考决策过程。

以处理 Azuki IP 为例，Agent 的实际决策过程如下：

第一步：当前状态显示数据为空，Agent 分析认为需要先读取链上数据，于是调用 ip_reader 工具从以太坊主网获取 Azuki 的链上元数据。

第二步：数据已读取，Agent 判断下一步需要分析风格特征，于是调用 style_analyzer 工具让 GLM-5.1 提取 Azuki 的视觉风格、叙事基调和代表符号。

第三步：风格已分析完毕，Agent 决定创作衍生故事，调用 story_writer 工具生成 3000 字以上的完整叙事。

第四步：故事完成，Agent 判断需要将故事转化为动画分镜脚本，调用 script_writer 工具生成专业分镜。

第五步：脚本生成完毕，Agent 决定设计周边资产概念，调用 asset_designer 工具生成 2 款可上链的资产设计。

第六步：所有内容生成完成，Agent 执行质量检查，评估风格一致性。

每次决策都基于当前实际状态，不是预设的固定顺序。

---

## 核心功能

链上 IP 数据读取。自动读取任意 ERC-721 合约的链上数据，从以太坊主网实时获取 IP 的名称、描述、属性列表和 tokenURI 元数据。支持通过 IP 名称自动查找合约地址，也支持直接输入合约地址。

IP 风格分析。GLM-5.1 提取 IP 独有的视觉风格、叙事基调、文化背景和代表符号。每个 IP 的分析结果都是独特的，包含世界观背景 lore、角色性格习惯 character、代表性符号 key_symbols、文化来源 cultural_reference。这些数据是后续内容创作的基础。

衍生故事创作。基于 IP 独有的世界观和角色设定，用 GLM-5.1 创作高质量的衍生故事。要求完整的故事弧线包括起因发展转折高潮收束。场景有画面感，对话体现角色性格，主题有深度。篇幅 2000 到 4000 字。

动画分镜脚本生成。将故事转化为专业的动画分镜脚本，包含 6 到 8 个分镜。每个分镜详细描述场景画面、对白内容、镜头运动方式和持续时间。脚本格式可直接用于动画制作。

周边资产概念设计。设计可上链的周边资产概念，每轮生成 2 款设计。每款资产包含产品名称、类型、详细设计描述、设计理念说明和 NFT 元数据。支持调用 CogView-4 生成概念图。

3D 模型生成。集成混元 Hunyuan 3D API，支持根据文本描述生成 GLB 格式的 3D 模型。生成的 3D 模型可铸造为链上 NFT，适用于数字穿戴、虚拟穿搭和元宇宙场景。

风格一致性检查。GLM-5.1 评估生成内容与 IP 风格画像的匹配度。评分标准为 0 到 10 分，7 分以上为通过。未通过的内容自动触发迭代修正，最多尝试 15 轮。

链上发布准备。将衍生内容打包为 NFT 元数据，生成 Solidity 合约代码。元数据使用 data URI 直接嵌入链上，不需要 IPFS 存储。合约代码符合 ERC-721 标准。

---

## 技术架构

IP Weave 采用两层架构：Agent 决策层和工具执行层。

Agent 决策层是系统的总指挥，不亲自执行具体任务。它基于 GLM-5.1 的分析能力，循环执行三个动作：读取当前状态，分析哪些步骤已经完成、哪些需要改进、还缺什么内容；根据分析结果决定下一步调用哪个工具以及传递什么参数；执行工具调用后评估结果，判断是否需要迭代修正。

工具执行层是独立的功能模块，每个工具负责一个特定领域的工作。当前系统注册了六个工具：ip_reader 从以太坊主网读取链上数据；style_analyzer 用 GLM-5.1 分析风格指纹；story_writer 用 GLM-5.1 创作衍生故事；script_writer 将故事转为分镜脚本；asset_designer 设计周边资产概念；quality_checker 检查内容风格一致性。

每个工具都有独立的输入输出接口，互不依赖。新增功能只需要添加新的工具模块，不需要改动 Agent 主循环。

---

## 使用的 API、SDK 和 AI 工具

GLM-5.1 通过 Z.AI Coding Plan 调用。用途是 Agent 的核心大语言模型，负责所有决策、分析、创作和质量检查工作。使用位置包括 Agent 决策循环、风格分析、故事创作、脚本生成、资产设计、质量评估。能完成 3000 字以上的高质量叙事创作，能根据 IP 特征自主调整风格，能对生成内容进行多维度质量评估。

CogView-4 是智谱 AI 的图片生成模型。用途是周边资产概念图的生成。AssetDesigner 在生成资产概念描述后调用 CogView-4 API 输出图片。将文本设计描述转化为可视化图片。需单独购买 API 额度。

web3.py 是以太坊 Python 交互库。用途是链上数据读取和合约交互。OnChainIPReader 通过 web3.py 读取 ERC-721 合约的 name、symbol、tokenURI。部署流程中通过 web3.py 与 Sepolia 测试网交互。实现对以太坊主网的实时数据读取。

混元 Hunyuan 3D 是腾讯云的 3D 生成模型。用途是周边资产 3D 模型生成，支持文本生成 GLB 格式模型。通过 API 提交文本描述，等待异步生成完成。将文本描述转化为 3D 数字资产。

solc 是 Solidity 编译器。用途是将 ERC-721 合约源码编译为 EVM 字节码。在合约部署流程中动态编译合约。支持动态编译和部署自定义 NFT 合约。

python-dotenv 用于从 .env 文件加载环境变量。在全局配置模块中加载 API Key。安全管理 API Key。

httpx 是 HTTP 客户端库。用途是调用 GLM-5.1、CogView-4、混元 3D 等外部 API。在 LLM 调用封装中发送 HTTP 请求。支持同步请求、超时控制和错误重试。

---

## 安装与运行

### 环境要求

Python 3.10 或更高版本。GLM-5.1 API Key（在 z.ai 注册 Coding Plan 获取）。

### Git Bash / Linux / Mac 环境

第一步克隆仓库：
git clone https://github.com/yanwenzhe519-ctrl/IP-Weave.git

第二步进入目录：
cd IP-Weave

第三步安装依赖：
pip install -r requirements.txt
pip install build123d

第四步创建配置文件：
cp .env.example .env

第五步编辑 .env 文件，将 ZHIPUAI_API_KEY 后面的内容替换为你的 API Key。

第六步运行 Agent：
set PYTHONPATH=%CD%
echo azuki | python src/run_agent.py

### Windows cmd 环境

第一步打开 cmd，输入：
git clone https://github.com/yanwenzhe519-ctrl/IP-Weave.git

第二步：
cd IP-Weave

第三步：
pip install -r requirements.txt
pip install build123d

第四步：
notepad .env
在记事本中写入 ZHIPUAI_API_KEY=你的API Key，保存关闭。

第五步运行：
set PYTHONPATH=%CD%
echo azuki | python srcun_agent.py

### 在 Claude Code 中使用

安装依赖后启动 Claude Code：
claude

然后在 Claude Code 中输入：
用 IP-Weave 跑 bayc

Claude Code 会自动读取 .claude/skills/ip-weave/SKILL.md 中的指令，执行对应命令。

### 在 Cursor / Codex 中使用

将项目克隆到本地，在 Cursor 中打开项目目录。在终端中运行：
echo bayc | python src/run_agent.py

### 支持的 IP 名称

预设支持：pepe（Pepe the Frog）、bayc（Bored Ape Yacht Club）、punk（CryptoPunks）、azuki（Azuki）。

也支持直接输入任意 ERC-721 合约地址：
echo "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D" | python src/run_agent.py

---

## 输出说明

运行成功后，结果保存在 output/IP名称/ 目录下。包含以下文件：

story.html 是衍生故事的 HTML 文件，双击在浏览器打开，包含完整叙事排版。

script.html 是动画分镜脚本的 HTML 文件，每个分镜以卡片形式展示，包含画面描述、镜头运动、对白和时长。

assets.html 是周边资产概念设计的 HTML 文件，展示每款资产的设计描述、设计理念和 NFT 元数据。

index.html 是交付报告首页，汇总所有产出内容。

output 目录下还有 nft 子目录，包含 NFT 元数据 metadata.json 文件和 Solidity 合约代码 IPWeaveNFT.sol。

---


## 链上部署指南

### 示例部署

本项目在 Sepolia 测试网上部署了一个示例合约，供评委验证链上交付能力。

网络: Sepolia Testnet
链 ID: 11155111
RPC 地址: https://ethereum-sepolia-rpc.publicnode.com
合约地址: 0x428fc6c80773F44220E7bcb9c7b4833C62F0f343
Etherscan: https://sepolia.etherscan.io/address/0x428fc6c80773F44220E7bcb9c7b4833C62F0f343
区块浏览器: https://sepolia.etherscan.io

矿工费: 部署合约消耗的 Gas 由 Sepolia 测试网 ETH 支付，该 ETH 无任何实际经济价值，可通过公开水龙头免费领取。

### 部署到其他 EVM 链

IP Weave 的合约部署逻辑在 src/agent/react_agent.py 的 _deploy_to_sepolia 方法中。这个方法使用 web3.py 与区块链交互，支持任何 EVM 兼容链。要部署到其他网络，需要修改以下参数：

RPC 地址: 改为目标网络的 RPC 节点地址。公共 RPC 可以在 ChainList 网站上查找。
链 ID: 每个网络有唯一的链 ID。以太坊主网是 1，Polygon 是 137，Arbitrum 是 42161。
区块浏览器: 用于验证交易的浏览器地址。
矿工费: 不同网络的 Gas 价格不同，需要根据网络拥堵情况调整 maxFeePerGas 参数。

常用的测试网配置：

Sepolia (以太坊官方测试网):
RPC: https://ethereum-sepolia-rpc.publicnode.com
链 ID: 11155111
领取测试 ETH: https://sepoliafaucet.com

Polygon Mumbai:
RPC: https://rpc-mumbai.maticvigil.com
链 ID: 80001
领取测试 MATIC: https://faucet.polygon.technology

Arbitrum Sepolia:
RPC: https://sepolia-rollup.arbitrum.io/rpc
链 ID: 421614
领取测试 ETH: https://faucet.quicknode.com/arbitrum

### 部署到 Solana

当前合约使用 Solidity 语言编写，只能部署到 EVM 兼容链。Solana 使用 Rust 语言，需要将合约重写为 Anchor 框架。计划在后续版本中加入 Solana 支持。

### 钱包管理

Agent 自动生成一个临时钱包用于合约部署，私钥仅保存在内存中，不会写入磁盘。钱包地址和私钥可以在运行日志中查看。

你也可以使用自己的钱包进行部署。在 src/agent/react_agent.py 中修改 PRIVATE_KEY 变量即可。请使用测试网钱包，不要使用主网私钥。

### 安全提醒

始终使用测试网进行开发和演示。测试网 ETH 可以通过水龙头免费获取。不要将主网私钥输入到任何代码配置中。每次部署前确认网络配置是否正确。


## 链上测试网证据

合约已部署到 Sepolia 测试网。网络名称 Sepolia Testnet，链 ID 11155111。

合约地址：0x428fc6c80773F44220E7bcb9c7b4833C62F0f343

https://sepolia.etherscan.io/address/0x428fc6c80773F44220E7bcb9c7b4833C62F0f343

部署交易哈希存储在 Agent 运行记录中。

Agent 钱包地址：0x3C215983f524271a4aB1A11E041cDC01ca84B9EC

该钱包由 Agent 自动生成，仅用于 Sepolia 测试网的合约部署和 NFT 铸造。钱包私钥存储在本地，不会上传到任何外部服务。钱包中的 Sepolia ETH 通过公开水龙头获取，无实际经济价值。

---

## 项目完成度与后续计划

当前已完成的部分包括：GLM-5.1 API 调用封装含超时重试和错误处理；链上 IP 数据实时读取支持以太坊主网 ERC-721 合约；IP 风格分析能提取每个 IP 独有的 lore、角色性格和代表符号；衍生故事创作能达到 3000 字以上的完整叙事；动画分镜脚本生成 6 到 8 个专业分镜；周边资产概念设计含 NFT 元数据；风格一致性检查低于 7 分自动迭代；NFT 元数据打包和 Solidity 合约生成；ReAct Agent 自主决策循环采用 Agent 加工具架构；3D 模型生成集成混元 Hunyuan API。

后续计划包括：接入 CogVideoX 或 Seedance 2.0 实现视频动画生成；构建 Web 界面降低使用门槛；支持批量 IP 处理提高效率；接入更多链上协议扩展 IP 来源。

---

## 安全与合规

API Key 仅存于本地 .env 文件，已加入 .gitignore 不会被上传到 GitHub。合约部署使用测试网临时钱包，仅用于 Sepolia 测试网，不支持主网操作。API 调用超时自动重试一次，图片生成失败不影响核心文本内容生成。Agent 连续 15 轮循环仍未达标时自动终止。
