# IP Weave

基于 GLM-5.1 的自治链上 IP 衍生内容 Agent。给一个链上 IP，它还你一个世界。

---

## 项目背景

链上 IP 资产在发行后普遍面临一个核心困境：mint 即终点。大量 NFT 项目在发售结束后缺乏持续的内容运营能力，社区成员想参与衍生创作但受限于专业技能（写作、分镜、设计），自发产出的内容质量参差不齐且风格难以统一。这导致大量链上 IP 陷入沉睡，其文化和商业价值远未被充分挖掘。

传统的内容生产需要完整的创作团队：作家负责故事创作、编剧负责分镜脚本、设计师负责视觉和周边、3D 建模师负责数字资产、开发者负责上链部署。这个过程周期长、成本高、协调复杂。一个完整的 IP 衍生内容从构思到交付往往需要数周时间和数十万的成本。

IP Weave 的核心理念是用一个 AI Agent 替代整个人类创作团队。一人加一 Agent，完成从创意输入到链上交付的完整内容生产链路。Agent 自主完成需求理解、资料收集、风格分析、内容创作、质量检查和链上发布，全程无需人工介入。这个项目的核心价值在于将 Web3 内容生产的成本降低一个数量级，同时保证产出质量的稳定和风格的统一。

本项目参加 Casual Hackathon Z.AI 赛道，聚焦于 Long-Horizon Task 的长程自主执行能力。

---

## 解决的问题

IP Weave 解决了链上 IP 生态中三个核心问题：

第一，内容生产门槛高。NFT 持有者想为持有的 IP 创作衍生内容，但缺乏写作、分镜、设计等专业技能。传统的解决方案是组建团队或外包，成本高效率低。IP Weave 让用户只需要输入一个 IP 名称或合约地址，Agent 自动完成从数据读取、风格分析、内容创作到上链交付的全部流程。用户不需要任何专业技能，只需要有一个想法。

第二，风格不统一。社区自发创作的内容风格参差，难以与原始 IP 的视觉和叙事风格对齐。不同创作者对同一 IP 的理解不同，产出内容往往缺乏一致性。IP Weave 通过 GLM-5.1 深度分析每个 IP 的独特风格特征，在每步创作前都检查风格一致性，确保所有产出在视觉语言、叙事基调和情感氛围上与原始 IP 保持一致。

第三，缺乏变现路径。衍生内容创作后缺少上链变现的渠道。创作者花费时间和精力创作内容，但难以将其转化为数字资产。IP Weave 自动将生成内容打包为 NFT 元数据，生成 Solidity 智能合约，支持部署到 Sepolia 测试网验证。同时集成了 RevenueSplitter 分润合约，支持多地址按比例分配收益。

---

## 为什么能做到自主决策

IP Weave 采用 ReAct（Reasoning + Acting）架构，GLM-5.1 在每个循环中分析当前状态并自主决定下一步动作。每轮循环中 Agent 会评估已经完成了什么、还缺什么、下一步最应该做什么。这不是按固定顺序执行的流水线，而是真实的思考决策过程。

与传统 AI 工作流的区别在于，传统工作流是线性的：第一步做什么、第二步做什么都是写死的。而 IP Weave 的 Agent 每步都由 GLM-5.1 根据实际状态做出判断。如果某一步失败了，Agent 可以选择重试、跳过或尝试替代方案，而不是崩溃或返回错误。

以处理 Azuki IP 为例，Agent 的实际决策过程如下：

第一步：当前状态显示数据为空，Agent 分析认为需要先读取链上基础数据，于是调用 read_ip 工具从以太坊主网获取 Azuki 的链上元数据和属性信息。

第二步：链上数据已成功读取，Agent 判断下一步需要分析 IP 的风格特征，于是调用 analyze_style 工具让 GLM-5.1 提取 Azuki 的视觉风格（日式街头、赛璐璐画风）、叙事基调（热血青春、成长）和代表符号（红色花瓣、街头服饰）。

第三步：风格分析完成，Agent 认为所有前置条件已满足，决定创作衍生故事，调用 write_story 工具生成完整叙事。

第四步：故事创作完成，Agent 判断需要将故事转化为可视化的分镜脚本，调用 write_script 工具生成包含镜号、画面描述、对白、镜头运动和时长的专业分镜。

第五步：脚本生成完毕，Agent 决定设计周边资产概念，调用 design_assets 工具生成两款可上链的资产设计，包含详细的材质、尺寸和使用场景描述。

第六步：资产设计完成后，Agent 调用 render_3d 工具为每款资产生成 3D 模型文件。

第七步：所有内容生成完成，Agent 执行质量检查，评估故事、脚本和资产与 IP 风格的一致性。如果评分低于 7 分，Agent 会自动重新生成不合格的内容。

第八步：质量检查通过后，Agent 执行交付，生成 HTML 报告和 NFT 合约代码。

每次决策都基于当前实际状态，不是预设的固定顺序。GLM-5.1 在每个决策点都会分析已经完成的工作、评估剩余工作量、权衡优先级后做出最优选择。

---

## 核心功能

链上 IP 数据读取。自动读取任意 ERC-721 合约的链上数据。从以太坊主网实时获取 IP 的名称、描述、属性列表和 tokenURI 元数据。支持通过 IP 名称自动查找合约地址（内置 Pepe、BAYC、CryptoPunks、Azuki 等知名项目的合约地址），也支持直接输入任意的 ERC-721 合约地址。读取到的数据会作为后续风格分析和内容创作的基础。

IP 风格分析。GLM-5.1 提取 IP 独有的视觉风格、叙事基调、文化背景和代表符号。每个 IP 的分析结果都是独特的，包含世界观背景 lore、角色性格习惯 character、代表性符号 key_symbols、文化来源 cultural_reference、角色原型 character_archetype。这些数据用于指导后续所有内容创作，确保产出的风格一致性。

衍生故事创作。基于 IP 独有的世界观和角色设定，用 GLM-5.1 创作高质量的衍生故事。要求完整的故事弧线包括起因、发展、转折、高潮和收束。场景有画面感，对话体现角色性格，主题有深度。篇幅 2000 到 4000 字。创作过程中会参考风格分析阶段提取的所有特征数据。

动画分镜脚本生成。将故事转化为专业的动画分镜脚本，包含 6 到 8 个分镜。每个分镜详细描述场景画面、对白内容、镜头运动方式和持续时间，以及场景的色彩基调和光影效果。脚本格式采用 markdown 表格，可直接用于动画制作团队的分工协作。

周边资产概念设计。设计可上链的周边资产概念，每轮生成 2 款设计。每款资产包含产品名称、类型、详细设计描述、设计理念说明和 NFT 元数据。设计描述涵盖材质、尺寸、工艺和使用场景等详细信息。支持调用 CogView-4 生成概念图。

3D 模型生成。内置基于 build123d 的参数化 3D 建模工具，为每款周边资产生成 GLB 格式的 3D 模型文件。模型可以在 Three.js 浏览器中查看，支持旋转、缩放和截面查看。生成的 3D 模型可以导入到 Unity、Unreal 等游戏引擎中，也可以铸造为链上 NFT。

风格一致性检查。GLM-5.1 评估生成内容与 IP 风格画像的匹配度。评分标准为 0 到 10 分，7 分以上为通过。检查维度包括视觉风格匹配度、叙事基调和情感氛围对齐度、角色设定一致性。未通过的内容自动触发迭代修正，最多尝试 15 轮。

链上发布准备。将衍生内容打包为 NFT 元数据，生成 Solidity 合约代码。元数据使用 data URI 直接嵌入链上，不需要 IPFS 存储。合约代码符合 ERC-721 标准，包含 name、symbol、ownerOf、tokenURI 等标准接口。同时生成 RevenueSplitter 分润合约，支持多地址按比例分配收益。

---

## 技术架构

IP Weave 采用两层架构：Agent 决策层和工具执行层。

Agent 决策层是系统的总指挥，不亲自执行具体任务。它基于 GLM-5.1 的分析能力执行循环：启动时先让 GLM-5.1 分析任务目标，将其拆解为多个可执行的步骤并排定优先级和顺序；每轮循环中 Agent 读取当前状态，分析哪些步骤已经完成、哪些需要改进、还缺什么内容；然后根据分析结果决定下一步调用哪个工具以及传递什么参数；执行工具调用后评估结果，判断是否需要迭代修正；全部完成后执行交付。

工具执行层是独立的功能模块，每个工具负责一个特定领域的工作。当前系统注册了八个工具：read_ip 从以太坊主网读取链上数据；analyze_style 用 GLM-5.1 分析风格指纹；write_story 用 GLM-5.1 创作衍生故事；write_script 将故事转为分镜脚本；design_assets 设计周边资产概念；render_3d 用 build123d 生成 3D 模型；check_quality 检查内容风格一致性；deliver 生成交付物。

每个工具都有独立的输入输出接口，互不依赖。新增功能只需要添加新的工具模块，不需要改动 Agent 主循环。工具之间通过 Agent 的 state 对象共享数据，state 中保存了所有步骤的中间结果。

系统的数据流是：Agent 收到 IP 名称后，先调用 read_ip 从以太坊主网读取链上数据，将结果存入 state。然后调用 analyze_style 用 GLM-5.1 分析风格特征。接着依次调用 write_story、write_script、design_assets 生成三种衍生内容。如果需要 3D 模型，调用 render_3d。所有内容生成完毕后执行 quality_checker 检查风格一致性。最后调用 deliver 生成 HTML 报告和 NFT 合约。

---

## 使用的 API、SDK 和 AI 工具

GLM-5.1 通过 Z.AI Coding Plan 调用。用途是 Agent 的核心大语言模型，负责所有决策、分析、创作和质量检查工作。使用位置包括 Agent 决策循环中的任务拆解和状态分析、风格分析中的特征提取、故事创作中的文本生成、脚本生成中的格式转换、资产设计中的概念描述、质量评估中的一致性检查。GLM-5.1 能够完成 3000 字以上的高质量叙事创作，能够根据 IP 特征自主调整创作风格，能够对生成内容进行多维度质量评估，能够分析复杂状态并做出合理决策。

CogView-4 是智谱 AI 的图片生成模型。用途是周边资产概念图的生成。使用位置在 AssetDesigner 生成资产概念描述后调用 CogView-4 API 输出图片。效果是将文本设计描述转化为可视化图片，方便用户直观了解资产外观。需要单独购买 API 额度。

web3.py 是以太坊 Python 交互库。用途是链上数据读取和合约交互。使用位置在 OnChainIPReader 通过 web3.py 读取 ERC-721 合约的 name、symbol、tokenURI。部署流程中通过 web3.py 与 Sepolia 测试网交互发送交易。web3.py 实现了对以太坊主网的实时数据读取和测试网合约部署。

build123d 是 Python 参数化 3D 建模库。用途是为周边资产生成 3D 模型文件。使用位置在 Agent 的 render_3d 工具中。通过 Python 代码创建几何体组合、布尔运算、拉伸旋转等操作生成 3D 模型。效果是不需要外部 API，纯代码即可生成 GLB 格式的 3D 模型文件。

solc 是 Solidity 编译器。用途是将 ERC-721 合约源码编译为 EVM 字节码。使用位置在合约部署流程中动态编译合约。支持动态编译和部署自定义 NFT 合约。

python-dotenv 用于从 .env 文件加载环境变量。用途是安全管理 API Key，避免密钥硬编码在代码中。使用位置在全局配置模块中加载 ZHIPUAI_API_KEY 等敏感信息。

httpx 是 HTTP 客户端库。用途是调用 GLM-5.1、CogView-4 等外部 API。使用位置在 LLM 调用封装中发送 HTTP 请求。支持同步请求、超时控制和自动重试。

---

## 安装与运行

### 环境要求

Python 3.10 或更高版本。GLM-5.1 API Key，在 z.ai 注册 Coding Plan 获取。

### 第一步：克隆仓库

在终端中输入以下命令：

git clone https://github.com/yanwenzhe519-ctrl/IP-Weave.git

这条命令会将项目代码下载到当前目录的 IP-Weave 文件夹中。

### 第二步：进入项目目录

cd IP-Weave

### 第三步：安装依赖

pip install -r requirements.txt
pip install build123d

这会安装项目所需的所有 Python 库，包括 web3.py、httpx、python-dotenv、loguru、build123d 等。安装过程可能需要 2 到 5 分钟。

### 第四步：配置 API Key

echo "ZHIPUAI_API_KEY=你的Key" > .env

在 Windows cmd 中请使用：
notepad .env
然后写入 ZHIPUAI_API_KEY=你的Key，保存关闭。

### 第五步：运行 Agent

交互式输入：
python src/run_agent.py
然后输入 IP 名称（如 azuki 或 bayc 等）。

或直接指定 IP：
echo "azuki" | python src/run_agent.py

### 在 Claude Code 中使用

安装完依赖后，启动 Claude Code：
claude
然后在 Claude Code 中输入：用 IP-Weave 跑 bayc

### 在 Cursor 中使用

在 Cursor 中打开项目目录，在终端中运行：
echo "bayc" | python src/run_agent.py

### 支持的 IP

预设支持：pepe、bayc、punk、azuki。也支持直接输入任意 ERC-721 合约地址。

---

## 输出说明

运行成功后，所有结果保存在 output/IP名称/ 目录下。

story.html 是衍生故事的 HTML 文件，双击在浏览器打开。页面采用深色主题排版，包含完整的叙事文本、章节分隔和页脚信息。可以直接用于阅读和展示。

script.html 是动画分镜脚本的 HTML 文件，每个分镜以卡片形式展示。包含画面描述、镜头运动方式、对白文本和持续时间等信息。可以直接用于动画制作团队的分工。

assets.html 是周边资产概念设计的 HTML 文件，展示每款资产的设计描述、类型标签、设计理念说明。如果有生成的 3D 模型，也会包含模型链接。

index.html 是交付报告首页，汇总所有产出内容并提供链接。

nft 子目录包含 NFT 元数据文件 metadata.json、Solidity 合约代码 IPWeaveNFT.sol 和部署指南 DEPLOY_README.md。

---

## 链上部署指南

### 示例部署

本项目在 Sepolia 测试网上部署了一个示例合约，供评委验证链上交付能力。

网络: Sepolia Testnet，链 ID: 11155111
RPC 地址: https://ethereum-sepolia-rpc.publicnode.com
合约地址: 0x428fc6c80773F44220E7bcb9c7b4833C62F0f343
Etherscan: https://sepolia.etherscan.io/address/0x428fc6c80773F44220E7bcb9c7b4833C62F0f343

这个示例合约仅用于演示，使用的是测试网 ETH，没有任何实际经济价值。评审可以通过 Etherscan 查看合约代码和交易记录。

### 部署到其他 EVM 链

项目支持任何 EVM 兼容链。部署时需要修改 src/agent/react_agent.py 中的 RPC 地址和链 ID。

常用测试网配置：
Sepolia: RPC https://ethereum-sepolia-rpc.publicnode.com，链 ID 11155111
Polygon Mumbai: RPC https://rpc-mumbai.maticvigil.com，链 ID 80001
Arbitrum Sepolia: RPC https://sepolia-rollup.arbitrum.io/rpc，链 ID 421614

### 钱包管理

Agent 自动生成临时钱包用于部署，私钥仅在内存中使用。也支持用户导入自己的测试网钱包。请始终使用测试网，不要使用主网私钥。

---

## 链上测试网证据

合约地址: 0x428fc6c80773F44220E7bcb9c7b4833C62F0f343
Etherscan: https://sepolia.etherscan.io/address/0x428fc6c80773F44220E7bcb9c7b4833C62F0f343

Agent 钱包地址: 0x3C215983f524271a4aB1A11E041cDC01ca84B9EC
该钱包由 Agent 自动生成，仅用于 Sepolia 测试网部署。钱包中的 Sepolia ETH 通过公开水龙头获取。

铸造交易记录可以在 Etherscan 上查看。

---

## 安全与合规

API Key 仅存于本地 .env 文件，已加入 .gitignore 不会被上传。合约部署仅使用测试网，不涉及主网和真实资产。所有 API 调用使用 HTTPS 加密传输。失败时有超时重试机制。Agent 循环上限 20 轮，超时自动终止交付。
