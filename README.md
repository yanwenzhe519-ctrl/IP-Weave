# 🧬 IP Weave — 链上衍生宇宙

> **IP 衍生内容 Agent：基于已有链上 IP，自主生成风格一致的衍生故事、动画脚本、周边资产。**
>
> Casual Hackathon · Z.AI 赛道 — 基于 GLM-5.1 的 Long-Horizon Task

---

## ✨ 一句话

> 给它一个链上 IP，它还你一个世界。

---

## 🎯 项目目标

**IP Weave** 是一个基于 **GLM-5.1** 的自治 AI Agent。它以 **Perceive → Plan → Execute → Reflect → Iterate → Deliver** 的完整闭环，自主完成链上 IP 的衍生内容创作。

### 解决什么问题

链上 IP 在注册后陷入"IP 沉睡"——缺乏持续内容运营。IP Weave 让 Agent 自主完成从理解 IP 到交付产出的全过程。

## 🏗️ 架构

```
链上 IP 地址
    ↓
┌────────────────────────────────────────────────┐
│               IP Weave Agent                     │
│                                                  │
│  [1/6] 读取链上 IP 数据                          │
│  [2/6] GLM-5.1 分析风格指纹                      │
│  [3/6] GLM-5.1 制定创作计划                      │
│  [4/6] GLM-5.1 执行创作                          │
│        ├ 📖 衍生故事                             │
│        ├ 🎬 动画分镜脚本                         │
│        └ 🧸 周边资产概念设计                     │
│  [5/6] GLM-5.1 风格一致性检查                    │
│  [6/6] 迭代 / 交付                              │
└────────────────────────────────────────────────┘
    ↓
输出: 故事 + 脚本 + 资产概念（含浏览器可看 HTML）
```

## 🧠 GLM-5.1 调用位置

| 模块 | 用途 |
|------|------|
| StyleAnalyzer | 从链上数据提取 IP 风格指纹 |
| Planner | 自主制定多步骤创作计划 |
| StoryGenerator | 创作衍生故事 |
| ScriptGenerator | 生成动画分镜脚本 |
| AssetDesigner | 设计周边资产概念 |
| StyleChecker | 检查风格一致性，低于 7 分触发迭代 |

## 🚀 安装运行

```bash
pip install -r requirements.txt
python src/main.py
```

## 📋 输出

运行后在 `output/` 目录生成：
- **HTML 页面**（浏览器直接打开，美观排版）
  - `index.html` — 首页报告
  - `story.html` — 衍生故事
  - `script.html` — 动画分镜
  - `assets.html` — 周边资产
- **Markdown / JSON** 原始文件

## 🔒 安全边界

- API Key 仅在本地 `.env` 使用
- 链上操作为只读模式
- 图片生成失败不影响核心流程
- 所有调用有超时和重试保护

## 👥 团队

<!-- TODO: 填写团队信息 -->

## 📄 相关链接

- [Casual Hackathon](https://casualhackathon.com)
- [Z.AI (GLM Coding Plan)](https://z.ai)
