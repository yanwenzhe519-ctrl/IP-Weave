---
name: render-3d
description: 3D 模型生成 Skill - 基于 build123d 的参数化建模
model: glm-5.1
when: 用户需要为周边资产生成 3D 模型时
---

# Render 3D

使用 build123d 库生成参数化 3D 模型，输出 GLB 格式。

## 安装

pip install build123d

## 用法

from build123d import *
from src.skills.render_3d import Render3D

# 初始化
r3d = Render3D()

# 生成模型
r3d.generate("角色立牌", "一个 Azuki 风格的角色立牌")

# 查看输出
print(r3d.last_output)
