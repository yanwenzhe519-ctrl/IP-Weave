IP Weave

基于 GLM-5.1 的自治链上 IP 衍生内容 Agent。给一个链上 IP，它还你一个世界。

Casual Hackathon Z.AI 赛道参赛作品

---

项目背景

链上 IP 资产在发行后普遍面临一个核心困境：mint 即终点。大量 NFT 项目在发售结束后缺乏持续的内容运营能力，社区成员想参与衍生创作但受限于专业技能（写作、分镜、设计），自发产出的内容质量参差不齐且风格难以统一。这导致大量链上 IP 陷入沉睡，其文化和商业价值远未被充分挖掘。

IP Weave 的解决方案是：用 AI Agent 替代整个人类创作团队。一人加一个 Agent，完成从创意输入到链上交付的完整内容生产链路。Agent 自主完成需求理解、资料收集、风格分析、内容创作、质量检查和链上发布，全程无需人工介入。

这个项目的核心价值在于将 Web3 内容生产的成本降低一个数量级，同时保证产出质量的稳定和风格的统一。

---

安装与运行

前置条件：
- Python 3.10 或更高版本
- GLM-5.1 API Key（在 z.ai 注册 Coding Plan 获取）

安装步骤：

第一步，克隆仓库：
git clone https://github.com/yanwenzhe519-ctrl/IP-Weave.git
cd IP-Weave

第二步，安装依赖：
pip install -r requirements.txt

第三步，配置 API Key：
cp .env.example .env
然后用记事本打开 .env 文件，将 ZHIPUAI_API_KEY 后面的内容替换为你自己的 API Key。

第四步，运行 Agent：
set PYTHONPATH=%CD%
echo azuki | python src\run_agent.py

输入任意链上 IP 名称，Agent 自动执行全部流程。支持的 IP 包括 azuki、bayc、punk、pudgy、doodles 等知名项目，也支持直接输入 ERC-721 合约地址。

---

核心功能

IP Weave 实现了从创意输入到链上交付的完整内容生产链路，全程由 Agent 自主调度执行。

1. 链上 IP 数据读取
自动读取任意 ERC-721 合约的链上数据。从以太坊主网实时获取 IP 的名称、描述、属性列表和 tokenURI 元数据。支持通过 IP 名称自动查找合约地址，也支持直接输入合约地址。

2. IP 风格分析
GLM-5.1 提取 IP 独有的视觉风格、叙事基调、文化背景和代表符号。每个 IP 的分析结果都是独特的，包含 lore 世界观背景、character 角色性格习惯、key_symbols 代表性符号、cultural_reference 文化来源等信息。这些数据是后续内容创作的基础。

3. 衍生故事创作
基于 IP 独有的世界观和角色设定，用 GLM-5.1 创作高质量的衍生故事。要求完整的故事弧线，包括起因、发展、转折、高潮和收束。场景有画面感，对话能体现角色性格，主题有深度。篇幅在 2000 到 4000 字之间。

4. 动画分镜脚本生成
将故事转化为专业的动画分镜脚本，包含 6 到 8 个分镜。每个分镜详细描述场景画面、对白内容、镜头运动方式和持续时间。脚本可以直接用于动画制作。

5. 周边资产概念设计
设计可上链的周边资产概念，每轮生成 2 款设计。每款资产包含产品名称、类型、详细设计描述、设计理念说明和 NFT 元数据。支持调用 CogView-4 生成概念图。

6. 风格一致性检查
GLM-5.1 评估生成内容与 IP 风格画像的匹配度。评分标准为 0 到 10 分，7 分以上为通过。未通过的内容会自动触发迭代修正，最多尝试 15 轮。

7. 链上发布准备
将衍生内容打包为 NFT 元数据，生成 Solidity 合约代码。元数据包含故事描述、SVG 图形和属性标签，使用 data URI 直接嵌入链上，不需要 IPFS。

---

技术架构

系统由两层构成：Agent 决策层和 Skills 执行层。

Agent 决策层：
Agent 是系统的总指挥，不亲自执行具体任务。它基于 GLM-5.1 的分析能力，循环执行三个动作：分析当前状态，决定下一步做什么；调用合适的技能模块并传递参数；评估技能执行结果，判断是否需要迭代修正。

Skills 执行层：
Skills 是独立的功能模块，每个技能负责一个单一领域的工作。目前注册了六个技能：ip_reader 负责链上数据读取，style_analyzer 负责风格分析，content_creator 负责故事创作，script_creator 负责分镜脚本生成，asset_designer 负责资产概念设计，nft_publisher 负责链上发布准备。

工作流程：
Agent 收到 IP 名称后，先调用 ip_reader 从以太坊主网读取链上数据，然后调用 style_analyzer 用 GLM-5.1 分析风格指纹。接着依次调用 content_creator、script_creator 和 asset_designer 生成三种衍生内容。内容生成完毕后执行质量检查，通过后调用 nft_publisher 打包上链。每个步骤由 GLM-5.1 自主决策顺序和参数，不是写死的流水线。

---

使用到的 API SDK AI 工具

1. GLM-5.1 通过 Z.AI Coding Plan 调用
用途：Agent 的核心大语言模型，负责所有决策、分析、创作和质量检查工作。
使用位置：Agent 决策循环、风格分析、故事创作、脚本生成、资产设计、质量评估全部依赖 GLM-5.1。
效果：能完成 3000 字以上的高质量叙事创作，能根据 IP 特征自主调整风格，能对生成内容进行多维度质量评估。

2. CogView-4 智谱 AI 图片生成
用途：周边资产概念图的生成。
使用位置：AssetDesigner 在生成资产概念描述后调用 CogView-4 API 输出图片。
效果：将文本设计描述转化为可视化图片，需要单独购买 API 额度。

3. web3.py
用途：以太坊链上数据读取和合约交互。
使用位置：OnChainIPReader 通过 web3.py 读取 ERC-721 合约的 name、symbol、tokenURI。ReActAgent 通过 web3.py 编译和部署 Solidity 合约。
效果：实现对以太坊主网的实时数据读取，支持 Sepolia 测试网的合约部署。

4. solc Solidity 编译器
用途：将 ERC-721 合约源码编译为 EVM 字节码。
使用位置：Agent 的 deploy_to_sepolia 方法中编译合约。
效果：支持动态编译和部署自定义 NFT 合约。

5. python-dotenv
用途：从 .env 文件加载环境变量。
使用位置：全局配置模块 src/config.py。
效果：安全地管理 API Key，防止密钥泄露。

6. httpx
用途：HTTP 客户端，用于调用 GLM-5.1 和 CogView-4 的 API。
使用位置：LLM 调用封装 src/utils/llm.py。
效果：支持同步请求、超时控制和错误重试。

---

链上测试网证据

部署网络：Sepolia Testnet
链 ID：11155111
RPC 地址：https://ethereum-sepolia-rpc.publicnode.com

合约地址：
0x1E70f147e4EE4Ef2Feb533DC5a8580C791e1a507
Etherscan 链接：
https://sepolia.etherscan.io/address/0x1E70f147e4EE4Ef2Feb533DC5a8580C791e1a507

部署交易哈希：
0x0739ad31e20dfb332e7498babc8919cc657615977974ef3b0a400d1942adabc1
Etherscan 链接：
https://sepolia.etherscan.io/tx/0x0739ad31e20dfb332e7498babc8919cc657615977974ef3b0a400d1942adabc1

铸造交易哈希：
0x257dc02496bffb892f1a4a6fa66423a5c63a00649ee7c987140da8c6f43b7d59
Etherscan 链接：
https://sepolia.etherscan.io/tx/0x257dc02496bffb892f1a4a6fa66423a5c63a00649ee7c987140da8c6f43b7d59

Agent 钱包地址：
0x3C215983f524271a4aB1A11E041cDC01ca84B9EC

该钱包由 Agent 在部署时自动生成，仅用于 Sepolia 测试网的合约部署和 NFT 铸造。钱包私钥存储在本地，不会上传到任何外部服务。钱包中的 Sepolia ETH 通过公开水龙头获取，无实际经济价值。

操作记录：
Agent 每次运行会自动记录完整的任务拆解、工具调用、迭代修复和交付成果，保存在 output 目录下的 run_record.json 文件中。

---

安全与合规边界

API Key 安全：ZHIPUAI_API_KEY 仅存于本地 .env 文件，.env 已加入 .gitignore，不会被上传到 GitHub。README 和代码中不包含任何真实密钥。

链上操作权限：合约部署使用临时生成的测试钱包，仅部署到 Sepolia 测试网。不支持主网操作，不涉及真实资产。私钥由 Agent 在内存中使用，不写入磁盘。

失败处理机制：API 调用超时自动重试一次。图片生成失败不影响核心文本内容生成流程。合约部署失败时记录错误日志，不会自动重试消耗 Gas。

人工介入条件：部署到测试网需要钱包有足够的 Sepolia ETH，用户需从公开水龙头领取。Agent 连续 15 轮循环仍未达标时自动终止，等待人工调整。所有关键步骤都有日志输出，用户可随时中断。

第三方工具说明：所有使用的 API、SDK、开源代码和 AI 工具都在 README 中列出并说明用途。GLM-5.1 和 CogView-4 为智谱 AI 的商业 API，用户需要自行注册获取密钥。其他工具均为开源或免费使用。

---

项目完成度与后续计划

当前已完成的内容包括：GLM-5.1 API 调用封装，含超时重试和错误处理。链上 IP 数据实时读取，支持以太坊主网 ERC-721 合约。IP 风格分析，能提取每个 IP 独有的 lore、角色性格和代表符号。衍生故事创作，能达到 3000 字以上的完整叙事。动画分镜脚本生成，6 到 8 个专业分镜。周边资产概念设计，含 NFT 元数据。风格一致性检查，低于 7 分自动迭代。NFT 元数据打包和 Solidity 合约生成。ReAct Agent 自主决策循环，采用总指挥加技能模块架构。

后续计划包括：接入 Seedance 2.0 或 CogVideoX 实现视频动画生成。自动化 IPFS 上传，支持去中心化存储。构建 Web 界面，降低使用门槛。支持批量 IP 处理，提高效率。增加更多内容类型，如音乐、3D 模型。

---

相关链接

GitHub 仓库：https://github.com/yanwenzhe519-ctrl/IP-Weave
合约 Etherscan：https://sepolia.etherscan.io/address/0x1E70f147e4EE4Ef2Feb533DC5a8580C791e1a507
Casual Hackathon：https://casualhackathon.com
Z.AI GLM-5.1：https://z.ai

---

许可

MIT