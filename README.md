[![GitHub stars](https://img.shields.io/github/stars/yanwenzhe519-ctrl/IP-Weave)](https://github.com/yanwenzhe519-ctrl/IP-Weave)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![GLM](https://img.shields.io/badge/LLM-GLM--5.1-green)](https://z.ai)
[![Sepolia](https://img.shields.io/badge/Deployed-Sepolia-orange)](https://sepolia.etherscan.io/address/0x72Aa0058c6D119504c5C2ea85BF7ecFfA9283862)

# IP Weave

基于 GLM-5.1 的自治链上 IP 衍生内容 Agent。给一个链上 IP，它还你一个世界。

---

## 项目背景

链上 IP（NFT 藏品、数字艺术作品等）在发行后普遍面临内容运营断层的问题。衍生内容创作门槛高、风格难以统一，导致大量链上 IP 陷入"沉睡"。

IP Weave 是一个基于 GLM-5.1 的 ReAct Agent，以自主决策循环的方式，自动完成从链上 IP 读取到衍生内容交付的完整流程。产出衍生故事、动画分镜脚本、周边资产三种内容，并生成 NFT 元数据可供链上发布。

---

## 安装与运行方式

### 前置要求

- Python 3.10 或更高版本
- GLM Coding Plan 订阅（获取 API Key 请访问 z.ai）

### 安装步骤

```bash
git clone https://github.com/yanwenzhe519-ctrl/IP-Weave.git
cd IP-Weave
pip install -r requirements.txt
cp .env.example .env
```

编辑 .env 文件，填入你的 ZHIPUAI_API_KEY。

### 运行

```bash
python src/run_agent.py --ip pepe
```

可选 IP 参数：

| 参数 | 说明 |
|------|------|
| --ip pepe | Pepe 青蛙 |
| --ip bayc | Bored Ape Yacht Club |
| --ip punk | CryptoPunks |
| --ip azuki | Azuki |

---

## 核心功能

| 功能 | 说明 |
|------|------|
| 链上 IP 读取 | 自动读取 ERC-721 元数据，支持 4 种预设 IP 和任意合约地址 |
| 风格分析 | GLM-5.1 提取 IP 的视觉配色、叙事基调、氛围关键词 |
| 创作计划 | GLM-5.1 自主制定叙事方向、产出顺序和关键元素 |
| 衍生故事 | 2000 字以上完整叙事创作，保留原 IP 风格 |
| 动画脚本 | 6 个专业分镜，含场景描述、对白、镜头运动、时长 |
| 周边资产 | 概念设计描述 + SVG 矢量图形（不依赖外部 API） |
| 风格检查 | 一致性评分，低于 7 分自动触发迭代修正 |
| 链上发布 | 生成 NFT 元数据、Solidity 合约和部署指南 |

---

## 技术架构

Agent 采用 ReAct（Reasoning + Acting）模式，GLM-5.1 在每个循环中自主决策下一步动作：

```ascii
                     IP Weave ReAct Agent
                             │
输入: 链上 IP 地址           │
                             ▼
┌──────────────────────────────────────────────────┐
│               GLM-5.1 决策循环                    │
│                                                  │
│  1. 读取 IP 数据  2. 分析风格   3. 制定计划      │
│  4. 创作故事      5. 生成脚本   6. 设计资产      │
│  7. 质量检查      8. 交付上链                    │
│                                                  │
│  每步由 GLM-5.1 自主选择工具并执行                │
│  质量不通过时自动迭代修正                         │
└──────────────────────────────────────────────────┘
                             │
                             ▼
输出: 衍生故事 + 动画脚本 + 周边资产 + NFT元数据
```

### GLM-5.1 调用位置

| 模块 | 用途 | 调用方式 |
|------|------|---------|
| StyleAnalyzer.extract() | 从链上数据提取风格指纹 | GLM-5.1 chat_json |
| Planner | 制定多步骤创作计划 | GLM-5.1 chat_json |
| StoryGenerator.generate() | 创作衍生故事 | GLM-5.1 chat |
| ScriptGenerator.generate() | 生成动画分镜脚本 | GLM-5.1 chat |
| AssetDesigner.generate() | 设计周边资产概念 | GLM-5.1 chat_json |
| StyleChecker.check() | 检查风格一致性 | GLM-5.1 chat_json |
| Agent Loop | 自主决策下一步动作 | GLM-5.1 chat_json |

---

## 使用到的 API / SDK / AI 工具

| 组件 | 工具 | 用途 |
|------|------|------|
| 大语言模型 | GLM-5.1（Z.AI Coding Plan） | 风格分析、规划、创作、检查、决策 |
| 图像生成 | CogView-4 / GLM-Image（需额外充值） | 周边资产图片生成 |
| 链上交互 | web3.py 6.0+ | 连接 Ethereum，部署合约 |
| 合约编译 | solc 0.8.20（通过 py-solc-x） | 编译 Solidity ERC-721 合约 |
| HTTP 客户端 | httpx 0.25+ | 调用 GLM-5.1 API |
| 环境管理 | python-dotenv 1.0+ | 加载 .env 配置 |
| 日志 | loguru 0.7+ | Agent 运行日志 |
| SVG 图形 | 纯 Python 代码生成 | 角色、场景、资产矢量图 |
| HTML 报告 | 纯 Python 代码生成 | 交付报告和可视化展示 |

---

## 输出说明

运行后在 output/IP名称/ 目录生成：

- story.html - 衍生故事（浏览器直接查看）
- script.html - 动画分镜脚本
- assets.html - 周边资产概念
- visuals/index.html - SVG 矢量图形
- nft/metadata.json - NFT 元数据
- nft/IPWeaveNFT.sol - Solidity 合约
- nft/DEPLOY_README.md - 部署指南

---

## 链上证明

合约已部署到 Sepolia 测试网：

- 合约地址: 0x72Aa0058c6D119504c5C2ea85BF7ecFfA9283862
- 部署交易: https://sepolia.etherscan.io/tx/0x73989f2991eb48e208f3427751cf0ca3732b237ba32ac8453688b5b0c1b68a7b
- 铸造交易: https://sepolia.etherscan.io/tx/0x2cb3651877efb1df2a7590336cae423a39f651afa41b348d962cbce191e61374

---

## 项目结构

```
IP-Weave/
├── src/
│   ├── run_agent.py       # 入口
│   ├── config.py           # 配置
│   ├── agent/
│   │   └── react_agent.py  # ReAct Agent 主循环
│   ├── chain/
│   │   ├── reader.py       # 链上数据读取
│   │   └── publisher.py    # 链上发布
│   ├── content/
│   │   └── generators.py   # 内容生成
│   └── utils/
│       ├── llm.py          # GLM-5.1 调用
│       ├── style.py        # 风格分析
│       ├── reporter.py     # HTML 报告
│       └── visualizer.py   # SVG 图形
├── output/                 # 生成成果
├── .env.example            # 配置模板
├── requirements.txt
└── README.md
```

---

## 安全说明

- API Key 仅存于本地 .env 文件，已加入 .gitignore 不会被上传
- 链上操作为只读模式，合约部署需用户主动执行
- 测试网络 ETH 无实际经济价值
- 所有 API 调用使用 HTTPS 加密传输
- 调佣超时保护，失败时自动重试一次

---

## 团队

| 角色 | 成员 | 联系方式 |
|------|------|---------|
| TBD | TBD | TBD |

---

## 许可

MIT
