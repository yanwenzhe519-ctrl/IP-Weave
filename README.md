# 🧬 IP Weave — 链上衍生宇宙

> **IP 衍生内容 Agent：基于已有链上 IP，自主生成风格一致的衍生故事、动画脚本、周边资产。**
>
> Casual Hackathon · Z.AI 赛道参赛作品

---

## ✨ 项目名称与一句话简介

**IP Weave**（链上衍生宇宙）

> 基于 GLM-5.1 的自治 AI Agent，给一个链上 IP，它还你一个世界。

---

## 🎯 项目背景与解决的问题

### 现状痛点

链上 IP（NFT 藏品、Meme 代币、数字艺术作品等）在发行后往往陷入"IP 沉睡"——缺乏持续的内容运营，社区成员参与创作门槛高，自发衍生内容质量参差不齐且风格难以统一。

### 解决方案

**IP Weave** 是一个基于 **GLM-5.1** 的自治 AI Agent，它能自主完成从"理解链上 IP"到"交付衍生内容"的完整闭环：

1. 自动读取链上 IP 数据（合约元数据、链上属性）
2. GLM-5.1 分析提取 IP 风格指纹（视觉、叙事、氛围）
3. GLM-5.1 制定多步骤创作计划（叙事方向、产出顺序、质量标准）
4. 执行生成三大类衍生内容（故事/脚本/资产）
5. GLM-5.1 风格一致性自检（低于 7 分自动迭代修正）
6. 交付成果（浏览器可直接查看的 HTML 报告）

### 目标用户

- NFT 项目方 / DAO —— 自动化 IP 内容运营
- 链上 IP 持有者 —— 为自己的 IP 生成衍生内容
- Web3 内容创作者 —— 获取创作灵感和素材

---

## 🏗️ 技术架构

### 整体架构

```
用户输入（链上 IP 地址 / 预设名称）
        ↓
┌──────────────────────────────────────────────────────────┐
│                 IP Weave Agent                             │
│                                                           │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐            │
│  │ Perceive  │───▶│   Plan   │───▶│ Execute  │            │
│  │ (感知层)  │    │ (规划层)  │    │ (执行层)  │            │
│  │ 读链上数据 │    │GLM-5.1   │    │GLM-5.1   │            │
│  │ 风格分析  │    │ 创作计划  │    │ 生成内容  │            │
│  └──────────┘    └──────────┘    └────┬─────┘            │
│                                       │                   │
│                                       ▼                   │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐            │
│  │ Deliver  │◀───│ Reflect  │◀───│  Iterate │            │
│  │ (交付层)  │    │ (反思层)  │    │ (迭代层)  │            │
│  │ HTML报告  │    │GLM-5.1   │    │ 自动重做  │            │
│  │ 原始文件  │    │ 一致性检查│    │ 不合格内容│            │
│  └──────────┘    └──────────┘    └──────────┘            │
└──────────────────────────────────────────────────────────┘
        ↓
输出：衍生故事 + 动画分镜脚本 + 周边资产概念设计（HTML 报告）
```

### GLM-5.1 调用位置与关键流程

| 模块（文件） | GLM-5.1 调用方式 | 用途 | 体现的长程任务能力 |
|-------------|-----------------|------|------------------|
| `src/utils/style.py` → `StyleAnalyzer.extract()` | `glm.chat_json()` | 从链上数据提取 IP 风格指纹 | **理解分析** — 将非结构化数据转为结构化风格画像 |
| `src/agent/core.py` → `_make_plan()` | `glm.chat_json()` | 根据风格制定多步骤创作计划 | **任务拆解** — 自主决定叙事方向、产出顺序 |
| `src/content/generators.py` → `StoryGenerator.generate()` | `glm.chat()` | 创作风格一致的衍生故事 | **内容执行** — 长文本生成，保持一致性 |
| `src/content/generators.py` → `ScriptGenerator.generate()` | `glm.chat()` | 将故事转为动画分镜脚本 | **内容执行** — 跨格式转换 |
| `src/content/generators.py` → `AssetDesigner.generate()` | `glm.chat_json()` + `glm.generate_image()` | 设计周边资产概念 | **多模态执行** — 文本 + 图像 |
| `src/utils/style.py` → `StyleChecker.check()` | `glm.chat_json()` | 检查内容与风格是否一致 | **自我纠错** — 低于 7 分触发迭代修正 |
| `src/agent/core.py` → `run()` 主循环 | 组织以上所有调用 | 控制完整工作流 | **长程稳定** — 多步骤保持目标一致 |

### 使用到的 API / SDK / AI 工具

| 工具 | 用途 |
|------|------|
| **GLM-5.1**（智谱 Z.AI） | 核心 LLM — 风格分析、规划、创作、检查 |
| **CogView-3**（智谱 Z.AI） | 图像生成 — 周边资产概念图 |
| **Python httpx** | HTTP 客户端 — 调用 OpenAI 兼容 API |
| **python-dotenv** | 环境变量管理 |

---

## 🚀 安装与运行

### 环境要求

- Python 3.10+
- GLM Coding Plan 订阅（获取 API Key → [z.ai](https://z.ai)）

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/yanwenzhe519-ctrl/IP-Weave.git
cd IP-Weave

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置 API Key
# 编辑 .env 文件，填入你的 ZHIPUAI_API_KEY
```

### 运行方式

```bash
# 使用默认 IP（Pepe）
python src/main.py --ip pepe

# 指定其他预设 IP
python src/main.py --ip bayc       # Bored Ape Yacht Club
python src/main.py --ip punk       # CryptoPunks
python src/main.py --ip azuki      # Azuki

# 自定义 ERC-721 合约
python src/main.py --contract 0x... --token 1
```

---

## 📋 输出

运行后在 `output/{IP名称}/` 目录生成：

| 文件 | 格式 | 说明 |
|------|------|------|
| `index.html` | HTML | 交付报告首页（浏览器打开） |
| `story.html` | HTML | 📖 衍生故事（深色主题排版） |
| `script.html` | HTML | 🎬 动画分镜脚本 |
| `assets.html` | HTML | 🧸 周边资产概念设计 |
| `story.md` | Markdown | 衍生故事原始文件 |
| `animation_script.md` | Markdown | 动画脚本原始文件 |
| `assets_info.json` | JSON | 资产设计结构化数据 |
| `run_record.json` | JSON | 📋 长程任务运行记录 |

---

## 📁 项目结构

```
src/
├── main.py                # 入口（命令行参数解析）
├── config.py              # 全局配置
├── agent/
│   └── core.py            # Agent 主循环（6 步闭环）
├── chain/
│   └── reader.py          # 链上 IP 数据读取
├── content/
│   └── generators.py      # 内容生成器（故事/脚本/资产）
└── utils/
    ├── llm.py             # GLM-5.1 API 调用封装
    ├── style.py           # 风格分析 + 一致性检查
    └── reporter.py        # HTML 报告生成
```

---

## 📊 长程任务运行记录

Agent 每次运行会自动记录完整的任务拆解、工具调用、迭代过程和交付记录，保存在 `output/{IP名称}/run_record.json` 中。

### 运行示例（BAYC）

```
第1步 [链上数据读取]   → 读取 Bored Ape Yacht Club 元数据
第2步 [GLM-5.1 风格分析] → "戏谑、慵懒、玩世不恭、享乐主义"
第3步 [GLM-5.1 创作计划] → "Web3 游艇派对的荒诞纪实"
第4步 [GLM-5.1 执行创作] → 故事(10/10) ✓ 脚本(10/10) ✓ 资产(10/10) ✓
第5步 [GLM-5.1 风格检查] → 全部通过，无需迭代
第6步 [交付]              → output/Bored_Ape_Yacht_Club/index.html
```

### 运行示例（Pepe）

```
第1步 [链上数据读取]   → 读取 Pepe the Frog 元数据
第2步 [GLM-5.1 风格分析] → "混沌戏谑、略带忧郁的草根幽默"
第3步 [GLM-5.1 创作计划] → "Meme 宇宙碎片化单元剧"
第4步 [GLM-5.1 执行创作] → 故事(9/10) ✓ 脚本(9/10) ✓ 资产(9.5/10) ✓
第5步 [GLM-5.1 风格检查] → 全部通过
第6步 [交付]              → output/Pepe_Frog/index.html
```

---

## 🔒 安全边界与失败处理

| 维度 | 说明 |
|------|------|
| **API Key 安全** | Key 仅存于本地 `.env` 文件，已加入 `.gitignore` 不会上传 |
| **链上操作** | 当前为只读模式（读 tokenURI），不涉及私钥或交易发送 |
| **网络请求** | 所有 API 调用走 HTTPS 加密传输 |
| **超时保护** | 每次 LLM 调用设 300 秒超时，失败自动重试一次 |
| **降级策略** | CogView 出图失败不影响故事和脚本生成核心流程 |
| **成本控制** | 采用订阅制（Coding Plan），无隐藏 API 费用 |
| **人工介入** | Agent 每步打印详细日志，关键产出需人工确认后使用 |

---

## 📝 项目完成度与后续计划

### 当前完成度

- [x] GLM-5.1 API 调用封装（含重试和超时保护）
- [x] 链上 IP 数据读取（支持 4 种预设 + 任意 ERC-721）
- [x] 风格指纹提取（GLM-5.1 驱动）
- [x] 多步骤创作计划（GLM-5.1 自主规划）
- [x] 衍生故事生成
- [x] 动画分镜脚本生成
- [x] 周边资产概念设计
- [x] 风格一致性检查 + 迭代修正
- [x] HTML 报告生成
- [ ] CogView-3 图像生成（需额外充值）
- [ ] 真实以太坊 RPC 连接（需提供 RPC URL）
- [ ] 链上部署 / 铸造能力

### 后续计划

1. 接入 Story Protocol 等链上 IP 协议
2. 支持将生成内容铸造为 NFT
3. 增加更多内容类型（音乐、3D 模型等）
4. Web 界面（非 CLI）

---

## 👥 团队

<!-- 请填写你的团队信息 -->

| 角色 | 成员 | 钱包地址 | 联系方式 |
|------|------|----------|---------|
| TBD | TBD | TBD | TBD |

---

## 🔗 相关链接

- **GitHub Repo**: https://github.com/yanwenzhe519-ctrl/IP-Weave
- **Casual Hackathon**: https://casualhackathon.com
- **Z.AI (GLM Coding Plan)**: https://z.ai
- **Demo 视频**: <!-- 录制后填入链接 -->

---

## 📄 许可证

MIT
