---
name: ip-reader
description: 读取任意链上 IP 的元数据和链上属性
model: glm-5.1
when: 需要从区块链上获取 IP 信息时
---

# IP Reader

读取任意 ERC-721 合约的链上数据，返回 IP 名称、描述、属性列表。

## 用法

```python
from src.chain.reader import OnChainIPReader

reader = OnChainIPReader()
data = reader.fetch(ip_name="pepe")
# 或传入合约地址
data = reader.fetch(contract="0x...")
```

## 返回数据

- name: IP 名称
- contract: 合约地址
- metadata.attributes: 属性列表（世界观、色调、角色类型等）
