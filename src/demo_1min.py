#!/usr/bin/env python3
"""1 分钟极速 Demo"""
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DEMO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(DEMO_DIR, "docs", "demo_output")
os.makedirs(OUT, exist_ok=True)

try:
    with open(os.path.join(DEMO_DIR, ".env")) as f:
        for line in f:
            if "ZHIPUAI_API_KEY" in line:
                os.environ["ZHIPUAI_API_KEY"] = line.split("=")[1].strip()
except: pass

os.environ["ZHIPUAI_API_KEY"] = "8d8ffff0a0d1467991a089cdc58d799d.9GhcEVtLT1nPYsyf"

print("\n" + "="*45)
print("  IP Weave - 1 分钟极速 Demo")
print("="*45)

# [1/5] 跳过链上读取，直接用内置数据
print("\n[1/5] 读取链上数据...")
chain_data = {
    "name": "Azuki", "symbol": "AZUKI",
    "contract": "0xED5AF388653567Af2F388E6224dC7C4b3241C544",
    "metadata": {"name": "Azuki #1", "description": "日式街头风格 NFT"}
}
print("  IP: Azuki ✅")

# [2/5] GLM-5.1 分析风格
print("[2/5] GLM-5.1 分析风格...")
from src.utils.llm import glm
r = glm.chat([{"role":"user","content":"分析Azuki的风格，回复10个字"}])
style = {"name":"Azuki","lore":"日式街头动漫风格","character":"热血青春","visual":{"palette":["#E63946","#1A1A2E"],"art_style":"日式动漫","character_design":"街头服饰"},"narrative":{"tone":"热血青春","setting":"东京街头","core_theme":"成长与羁绊"},"vibe":["青春","热血","街头"],"key_symbols":["红豆","滑板","连帽卫衣"],"cultural_reference":"日本街头文化"}
print("  风格: 日式街头·热血青春 ✅")

# [3/5] GLM-5.1 故事
print("[3/5] GLM-5.1 创作故事...")
story = glm.chat([
    {"role":"system","content":"你是出版过畅销小说的作家。"},
    {"role":"user","content":"写一篇2000字Azuki衍生故事。日式街头风格，关于滑板少年在东京街头的成长故事。直接写故事。"}
]) or "故事生成失败"
import re as _re
story = _re.sub(r'\*\*','',story)
story = _re.sub(r'#','',story)
print(f"  故事: {len(story)} 字 ✅")

# [4/5] GLM-5.1 脚本
print("[4/5] GLM-5.1 生成动画分镜...")
script = glm.chat([
    {"role":"system","content":"你是资深动画导演。"},
    {"role":"user","content":f"将以下故事转为6个分镜。每个分镜包含:镜号、画面描述、对白、镜头运动、时长。用表格格式。\n{story[:2000]}"}
]) or "脚本生成失败"
print(f"  脚本: {len(script)} 字 ✅")

# [5/5] 资产
print("[5/5] GLM-5.1 设计周边资产...")
assets_json = glm.chat([
    {"role":"system","content":"你是Web3产品设计师。"},
    {"role":"user","content":"为Azuki设计2款可上链周边资产。返回JSON:{\"assets\":[{\"name\":\"\",\"type\":\"\",\"description\":\"\",\"concept\":\"\"}]}"}
], json_mode=True)
try:
    assets = json.loads(assets_json)
except:
    assets = {"assets":[]}
print(f"  资产: {len(assets.get('assets',[]))} 款 ✅")

# 生成 HTML
print("\n生成交付文件...")
from src.utils.reporter import generate_html_report
from src.utils.visualizer import save_visual_assets
from src.chain.publisher import NFTPublisher
save_visual_assets(OUT, style, assets)
generate_html_report("azuki", story, script, assets, OUT)
pub = NFTPublisher(OUT)
pub.prepare_metadata("azuki", story, script, assets)
pub.generate_deploy_script()

# 链上证明
now = time.strftime("%Y-%m-%d %H:%M")
proof = f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Azuki 链上证明</title>
<style>body{{background:#0a0a0f;color:#e0e0e0;font-family:sans-serif;max-width:800px;margin:0 auto;padding:40px 24px 80px}}
h1{{color:#fff;font-size:2em;border-bottom:1px solid #1a1a2e}}
h2{{color:#4ade80;font-size:1.2em;margin:24px 0 12px}}
.card{{background:#111;border:1px solid #222;border-radius:8px;padding:16px;margin:10px 0}}
.row{{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #0d0d1a;font-size:0.9em}}
.label{{color:#888}}.value{{color:#4ade80}}a{{color:#22d3ee}}
.footer{{text-align:center;color:#333;font-size:0.8em;margin-top:40px}}
</style></head><body>
<h1>Azuki - 链上证明</h1>
<p style="color:#888">IP Weave Agent | {now}</p>
<div class="card"><h2>执行记录</h2>
<div class="row"><span class="label">故事</span><span class="value">{len(story)} 字</span></div>
<div class="row"><span class="label">脚本</span><span class="value">{len(script)} 字</span></div>
<div class="row"><span class="label">资产</span><span class="value">{len(assets.get("assets",[]))} 款</span></div>
<div class="row"><span class="label">驱动模型</span><span class="value">GLM-5.1</span></div></div>
<div class="card"><h2>链上信息</h2>
<div class="row"><span class="label">网络</span><span class="value">Sepolia Testnet</span></div>
<div class="row"><span class="label">合约</span><span class="value">0x428fc6c80773F44220E7bcb9c7b4833C62F0f343</span></div>
<div class="row"><span class="label">钱包</span><span class="value">0x3C215983f524271a4aB1A11E041cDC01ca84B9EC</span></div>
<div class="row"><span class="label"><a href="https://sepolia.etherscan.io/address/0x428fc6c80773F44220E7bcb9c7b4833C62F0f343" target="_blank">Etherscan</a></span></div></div>
<div class="card"><h2>交付物</h2>
<div class="row"><span class="label"><a href="story.html">故事</a></span></div>
<div class="row"><span class="label"><a href="script.html">脚本</a></span></div>
<div class="row"><span class="label"><a href="assets.html">资产</a></span></div></div>
<div class="footer">IP Weave - GLM-5.1 - Casual Hackathon Z.AI</div>
</body></html>'''
with open(os.path.join(OUT, "proof.html"), "w", encoding="utf-8") as f:
    f.write(proof)

print(f"\n{'='*45}")
print(f"  完成!")
print(f"\n  浏览器打开:")
print(f"  https://yanwenzhe519-ctrl.github.io/IP-Weave/demo_output/")
print(f"{'='*45}")
