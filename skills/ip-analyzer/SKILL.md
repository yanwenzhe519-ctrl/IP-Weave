---
name: ip-analyzer
description: 分析链上 IP 的风格指纹，提取视觉和叙事特征
model: glm-5.1
when: 需要理解 IP 的风格特征时
---

# IP Analyzer

使用 GLM-5.1 分析 IP 数据，提取风格指纹。

## 用法

```python
from src.utils.style import StyleAnalyzer

analyzer = StyleAnalyzer()
profile = analyzer.extract(chain_data)
```

## 返回数据

- visual: 配色方案、美术风格、角色设计
- narrative: 叙事基调、世界观、核心主题
- vibe: 氛围关键词
