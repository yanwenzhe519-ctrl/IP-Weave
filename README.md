# IP Weave

基于 GLM-5.1 的自治链上 IP 衍生内容 Agent。

给一个链上 IP，它还你一个世界。

---


## 项目背景


链上 IP 资产在发行后普遍面临一个核心困境：mint 即终点。大量 NFT 项目在发售结束后缺乏持续的内容运营能力，社区成员想参与衍生创作但受限于专业技能，自发产出的内容质量参差不齐且风格难以统一。这导致大量链上 IP 陷入沉睡，其文化和商业价值远未被充分挖掘。

传统的内容生产需要完整的创作团队：作家负责故事创作、编剧负责分镜脚本、设计师负责视觉和周边、3D 建模师负责数字资产、开发者负责上链部署。这个过程周期长、成本高、协调复杂。

IP Weave 的核心理念是用一个 AI Agent 替代整个人类创作团队。一人加一 Agent，完成从创意输入到链上交付的完整内容生产链路。Agent 自主完成需求理解、资料收集、风格分析、内容创作、质量检查和链上发布，全程无需人工介入。

---


## 解决的问题


IP Weave 解决了链上 IP 生态中三个核心问题。

第一，内容生产门槛高。NFT 持有者想为持有的 IP 创作衍生内容，但缺乏写作、分镜、设计等专业技能。IP Weave 让用户只需要输入一个 IP 名称或合约地址，Agent 自动完成从数据读取、风格分析、内容创作到上链交付的全部流程。用户不需要任何专业技能，只需要有一个想法。

第二，风格不统一。社区自发创作的内容风格参差，难以与原始 IP 的视觉和叙事风格对齐。IP Weave 通过 GLM-5.1 深度分析每个 IP 的独特风格特征，在每步创作前都检查风格一致性，确保所有产出在视觉语言、叙事基调和情感氛围上与原始 IP 保持一致。

第三，缺乏变现路径。衍生内容创作后缺少上链变现的渠道。IP Weave 自动将生成内容打包为 NFT 元数据，生成 Solidity 智能合约，支持部署到 Sepolia 测试网验证。

---


## 项目目标


IP Weave 的目标是构建一个基于 GLM-5.1 的自治 AI Agent，实现一人加一 Agent 完成传统需要整个创作团队才能完成的链上 IP 衍生内容生产工作。

具体目标包括：让用户只需要输入一个链上 IP 名称或合约地址，Agent 自主完成全部创作流程，不需要任何专业技能。确保所有产出内容在视觉和叙事风格上与原始 IP 保持一致。将衍生内容打包为 NFT 并部署到测试网，实现从创意到上链的完整闭环。

---


## 核心功能


链上 IP 数据读取。自动读取任意 ERC-721 合约的链上数据。从以太坊主网实时获取 IP 的名称、描述、属性列表和 tokenURI 元数据。支持通过 IP 名称自动查找合约地址，也支持直接输入任意 ERC-721 合约地址。

IP 风格分析。GLM-5.1 提取 IP 独有的视觉风格、叙事基调、文化背景和代表符号。每个 IP 的分析结果都是独特的，包含 lore 世界观背景、character 角色性格习惯、key_symbols 代表性符号等信息。

衍生故事创作。基于 IP 独有的世界观和角色设定，用 GLM-5.1 创作高质量的衍生故事。要求完整的故事弧线包括起因、发展、转折、高潮和收束。篇幅 2000 到 4000 字。

动画分镜脚本生成。将故事转化为专业的动画分镜脚本，包含 6 到 8 个分镜。每个分镜详细描述场景画面、对白内容、镜头运动方式和持续时间。

周边资产概念设计。设计可上链的周边资产概念，每轮生成 2 款设计。每款资产包含产品名称、类型、详细设计描述、设计理念说明和 NFT 元数据。

3D 模型生成。内置基于 build123d 的参数化 3D 建模工具，为每款周边资产生成 GLB 格式的 3D 模型文件。

风格一致性检查。GLM-5.1 评估生成内容与 IP 风格画像的匹配度。评分标准为 0 到 10 分，7 分以上为通过。未通过的内容自动触发迭代修正。

链上发布准备。将衍生内容打包为 NFT 元数据，生成 Solidity 合约代码。元数据使用 data URI 直接嵌入链上，不需要 IPFS 存储。

---


## 技术架构


IP Weave 采用两层架构：Agent 决策层和工具执行层。

Agent 决策层是系统的总指挥，不亲自执行具体任务。它基于 GLM-5.1 的分析能力循环执行：启动时先让 GLM-5.1 分析任务目标，将其拆解为多个可执行的步骤并排定优先级和顺序。每轮循环中 Agent 读取当前状态，分析哪些步骤已经完成、哪些需要改进、还缺什么内容。然后根据分析结果决定下一步调用哪个工具以及传递什么参数。执行工具调用后评估结果，判断是否需要迭代修正。全部完成后执行交付。

工具执行层是独立的功能模块，每个工具负责一个特定领域的工作。当前系统注册了八个工具：read_ip 读取链上数据，analyze_style 分析风格特征，write_story 创作衍生故事，write_script 生成动画脚本，design_assets 设计周边资产，render_3d 生成 3D 模型，check_quality 检查风格一致性，deliver 生成交付物。

每个工具都有独立的输入输出接口，互不依赖。新增功能只需要添加新的工具模块，不需要改动 Agent 主循环。

---


## 为什么能够做到自主决策


IP Weave 采用 ReAct（Reasoning + Acting）架构，GLM-5.1 在每个循环中分析当前状态并自主决定下一步动作。每轮循环中 Agent 会评估已经完成了什么、还缺什么、下一步最应该做什么。这不是按固定顺序执行的流水线，而是真实的思考决策过程。

与传统 AI 工作流的区别在于，传统工作流是线性的：第一步做什么、第二步做什么都是写死的。而 IP Weave 的 Agent 每步都由 GLM-5.1 根据实际状态做出判断。如果某一步失败了，Agent 可以选择重试、跳过或尝试替代方案。

以处理 Azuki IP 为例，Agent 的实际决策过程：先读取链上数据，数据为空时自主决定调用 read_ip；数据读取完成后判断需要分析风格特征，调用 analyze_style；风格分析完成后认为前置条件已满足，决定创作衍生故事，调用 write_story；故事创作完成后调用 write_script 将故事转化为分镜脚本；然后依次调用 design_assets、render_3d、check_quality、deliver。每次决策都基于当前实际状态，不是预设的固定顺序。

---


## 使用的 API、SDK 和 AI 工具


GLM-5.1 通过 Z.AI Coding Plan 调用。用途是 Agent 的核心大语言模型，负责所有决策、分析、创作和质量检查工作。使用位置包括 Agent 决策循环、风格分析、故事创作、脚本生成、资产设计、质量评估。GLM-5.1 能够完成 3000 字以上的高质量叙事创作，能够根据 IP 特征自主调整创作风格。

CogView-4 是智谱 AI 的图片生成模型。用途是周边资产概念图的生成。使用位置在 AssetDesigner 生成资产概念描述后调用 CogView-4 API 输出图片。需单独购买 API 额度。

web3.py 是以太坊 Python 交互库。用途是链上数据读取和合约交互。使用位置在 OnChainIPReader 和合约部署流程。

build123d 是 Python 参数化 3D 建模库。用途是为周边资产生成 GLB 格式的 3D 模型文件。不需要外部 API。

solc 是 Solidity 编译器。用途是将 ERC-721 合约源码编译为 EVM 字节码。

python-dotenv 用于从 .env 文件加载环境变量，安全管理 API Key。

httpx 是 HTTP 客户端库，用于调用外部 API。

---


## GLM-5.1 调用位置与关键流程


任务拆解阶段：GLM-5.1 分析用户输入的 IP 名称和任务目标，将其拆解为多个可执行步骤并排定优先级。调用方式为 chat_json，返回结构化 JSON 格式的执行计划。

状态决策阶段：GLM-5.1 读取当前状态对象中的数据，分析哪些步骤已完成、哪些需要改进、下一步最应该做什么。调用方式为 chat_json，返回包含动作名称和决策理由的 JSON。

风格分析阶段：GLM-5.1 根据链上数据提取 IP 独有的视觉风格、叙事基调和代表符号。调用方式为 chat_json，返回结构化风格画像。

故事创作阶段：GLM-5.1 根据风格画像和创作计划生成完整的衍生故事。调用方式为 chat，返回 2000 到 4000 字的叙事文本。

脚本生成阶段：GLM-5.1 将故事文本转化为专业的分镜脚本。调用方式为 chat，返回包含镜号、画面描述、对白、镜头运动和时长的结构化脚本。

资产设计阶段：GLM-5.1 根据风格画像设计周边资产概念。调用方式为 chat_json，返回包含产品名称、类型、描述和 NFT 元数据的 JSON。

质量检查阶段：GLM-5.1 评估生成内容与 IP 风格画像的匹配度。调用方式为 chat_json，返回包含评分和修改建议的 JSON。

---


## 安装与运行


环境要求：Python 3.10 或更高版本。GLM-5.1 API Key（在 z.ai 注册 Coding Plan 获取）。

第一步克隆仓库：git clone https://github.com/yanwenzhe519-ctrl/IP-Weave.git


第二步进入目录：cd IP-Weave


第三步安装依赖：pip install -r requirements.txt 然后 pip install build123d

第四步配置 API Key：在项目目录创建 .env 文件，写入 ZHIPUAI_API_KEY=你的Key

第五步运行 Agent：echo azuki | python src/run_agent.py

支持的 IP 名称：pepe、bayc、punk、azuki。也支持直接输入任意 ERC-721 合约地址。

---


## 输出说明


运行成功后，结果保存在 output/IP名称/ 目录下。

story.html 是衍生故事的 HTML 文件，双击在浏览器打开。
script.html 是动画分镜脚本的 HTML 文件，每个分镜以卡片形式展示。
assets.html 是周边资产概念设计的 HTML 文件。
index.html 是交付报告首页。
nft 子目录包含 NFT 元数据和 Solidity 合约代码。

---

<img width="1165" height="851" alt="111" src="https://github.com/user-attachments/assets/d9d2d2cd-1b55-47f9-a0b9-bf21ed4b0963" />
<img width="1256" height="891" alt="1" src="https://github.com/user-attachments/assets/37d02f6d-3529-4299-bbdb-737b3a892cce" />
<img width="1202" height="871" alt="222" src="https://github.com/user-attachments/assets/9c5aea7b-7610-4896-90d0-37bada451c46" />
<img width="1146" height="898" alt="444" src="https://github.com/user-attachments/assets/a3ec471a-4d86-4cda-854d-1e0179b474af" />



## 长程任务运行记录

Agent 每次执行后会自动生成运行记录。

示例记录（Azuki 运行）：[docs/run_record_azuki.json](https://github.com/yanwenzhe519-ctrl/IP-Weave/blob/master/docs/run_record_azuki.json)，保存在 output/IP名称/run_record.json 中。

记录内容包含任务信息、步骤拆解、工具调用时间线和交付结果。通过这些记录，评审可以完整追溯 Agent 的任务拆解过程、每一步的工具选择、执行顺序和最终交付成果。

## 链上部署与测试网证明


Agent 默认部署到 Sepolia 测试网。部署时自动生成临时钱包用于支付 Gas 费用。Sepolia ETH 可通过公开水龙头免费领取。

部署到其他 EVM 链需要修改 src/agent/react_agent.py 中的 RPC 地址和链 ID。




Sepolia: RPC https://ethereum-sepolia-rpc.publicnode.com，链 ID 11155111
Polygon Mumbai: RPC https://rpc-mumbai.maticvigil.com，链 ID 80001
Arbitrum Sepolia: RPC https://sepolia-rollup.arbitrum.io/rpc，链 ID 421614

Agent 自动生成临时部署钱包，私钥仅在内存中使用。请始终使用测试网，不要使用主网私钥。

---





本项目在 Sepolia 测试网上部署了示例合约，供评委验证链上交付能力。

示例合约地址: 0x428fc6c80773F44220E7bcb9c7b4833C62F0f343
Etherscan: https://sepolia.etherscan.io/address/0x428fc6c80773F44220E7bcb9c7b4833C62F0f343
网络: Sepolia Testnet（链 ID 11155111）

用户每次运行 Agent 后，部署的合约地址会打印在终端输出中，可在 Etherscan 上查看。

---




## 团队信息

| 角色 | 成员 | 钱包地址 |
|------|------|----------|
| 独立开发者 | Venz | 0xd4bcc91f1e632fdbc4a431a5c33e78b22e940ff1 |



## 团队信息

| 角色 | 成员 | 钱包地址 |
|------|------|----------|
| 独立开发者 | Venz | 0xd4bcc91f1e632fdbc4a431a5c33e78b22e940ff1 |

## 安全与合规


API Key 仅存于本地 .env 文件，已加入 .gitignore 不会被上传。合约部署仅使用测试网，不涉及主网和真实资产。所有 API 调用使用 HTTPS 加密传输。Agent 循环上限 20 轮，超时自动终止交付。
