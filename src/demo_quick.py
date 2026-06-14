#!/usr/bin/env python3
"""20 秒极速 Demo — 展示 Agent 完整流程"""
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DEMO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(DEMO_DIR, "docs", "demo_output")
os.makedirs(OUT, exist_ok=True)

# 读取 .env
try:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")) as f:
        for line in f:
            if "ZHIPUAI_API_KEY" in line:
                os.environ["ZHIPUAI_API_KEY"] = line.split("=")[1].strip()
except:
    pass

from src.config import settings
from src.utils.llm import glm

print("\n" + "="*50)
print("  IP Weave · 极速 Demo")
print("="*50)

# 1. 链上读取 (实时)
print("\n[1/5] 读取链上数据...")
from src.chain.reader import OnChainIPReader
reader = OnChainIPReader()
data = reader.fetch(ip_name="azuki")
print(f"  IP: {data.get('name','')} ✅")

# 2. 风格分析 (GLM-5.1 快速分析)
print("\n[2/5] GLM-5.1 分析风格...")
from src.utils.style import StyleAnalyzer
style = StyleAnalyzer().extract(data)
print(f"  基调: {style.get('narrative',{}).get('tone','')[:60]} ✅")

# 3. 故事创作 (GLM-5.1)
print("\n[3/5] GLM-5.1 创作故事...")
from src.content.generators import StoryGenerator
plan = {"narrative_direction": "热血青春成长", "key_elements": ["街头","滑板","友谊"]}
story = StoryGenerator().generate(style, plan)
print(f"  {len(story)} 字 ✅")

# 4. 脚本生成 (GLM-5.1)
print("\n[4/5] GLM-5.1 生成分镜脚本...")
from src.content.generators import ScriptGenerator
script = ScriptGenerator().generate(story[:3000], style)
print(f"  {len(script)} 字 ✅")

# 5. 资产设计 (GLM-5.1)
print("\n[5/5] GLM-5.1 设计周边资产...")
from src.content.generators import AssetDesigner
assets = AssetDesigner().generate(style)
print(f"  {len(assets.get('assets',[]))} 款 ✅")

# 生成 3D 模型展示页
print("\n[6] 生成 3D 展示页面...")
import re as _re
_3d_prompt = "Generate a Three.js HTML page showing an Azuki anime-style character. Japanese streetwear aesthetic, red and black colors. OrbitControls, dark theme. Output full HTML."
_3d_result = glm.chat([{"role":"system","content":"Three.js designer. HTML only."},{"role":"user","content":_3d_prompt}])
if _3d_result:
    _match = _re.search(r"<html.*?>.*?</html>", _3d_result, _re.DOTALL|_re.IGNORECASE)
    if _match:
        with open(os.path.join(OUT, "azuki_3d.html"), "w", encoding="utf-8") as _f:
            _f.write(_match.group())
        print(f"  3D 页面已生成 ✅")
    else:
        print(f"  3D 跳过")
else:
    print(f"  3D 跳过")

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

# 链上证明页
with open(os.path.join(OUT, "proof.html"), "w", encoding="utf-8") as f:
    f.write(f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Azuki 链上证明</title>
<style>body{{background:#0a0a0f;color:#e0e0e0;font-family:sans-serif;max-width:800px;margin:0 auto;padding:40px 24px 80px}}
h1{{color:#fff;font-size:2em;border-bottom:1px solid #1a1a2e;padding-bottom:12px}}
h2{{color:#4ade80;font-size:1.2em;margin:24px 0 12px}}
.card{{background:#111;border:1px solid #222;border-radius:8px;padding:16px;margin:10px 0}}
.row{{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #0d0d1a;font-size:0.9em}}
.label{{color:#888}}.value{{color:#4ade80}}a{{color:#22d3ee}}
.footer{{text-align:center;color:#333;font-size:0.8em;margin-top:40px}}
</style></head><body>
<h1>Azuki · 链上证明</h1>
<p style="color:#888">IP Weave Agent | {time.strftime('%Y-%m-%d %H:%M')}</p>
<div class="card"><h2>执行记录</h2>
<div class="row"><span class="label">IP</span><span class="value">Azuki</span></div>
<div class="row"><span class="label">故事</span><span class="value">{len(story)} 字</span></div>
<div class="row"><span class="label">脚本</span><span class="value">{len(script)} 字</span></div>
<div class="row"><span class="label">资产</span><span class="value">{len(assets.get('assets',[]))} 款</span></div></div>
<div class="card"><h2>链上信息</h2>
<div class="row"><span class="label">网络</span><span class="value">Sepolia Testnet</span></div>
<div class="row"><span class="label">合约</span><span class="value">0x428fc6c80773F44220E7bcb9c7b4833C62F0f343</span></div>
<div class="row"><span class="label">钱包</span><span class="value">0x3C215983f524271a4aB1A11E041cDC01ca84B9EC</span></div></div>
<div class="card"><h2>交付物</h2>
<div class="row"><span class="label"><a href="story.html">故事</a></span><span class="value">{len(story)} 字</span></div>
<div class="row"><span class="label"><a href="script.html">脚本</a></span><span class="value">{len(script)} 字</span></div>
<div class="row"><span class="label"><a href="assets.html">资产</a></span><span class="value">{len(assets.get('assets',[]))} 款</span></div></div>
<div class="footer">IP Weave · GLM-5.1 · Casual Hackathon Z.AI</div>
</body></html>""")

print(f"\n{'='*50}")
print(f"  完成! 文件在:")
print(f"\n  📍 浏览器打开查看 (需先 git push 到 GitHub):")
print(f"\n  📖 故事: https://yanwenzhe519-ctrl.github.io/IP-Weave/demo_output/story.html")
print(f"  🎬 脚本: https://yanwenzhe519-ctrl.github.io/IP-Weave/demo_output/script.html")
print(f"  🧸 资产: https://yanwenzhe519-ctrl.github.io/IP-Weave/demo_output/assets.html")
print(f"  🎨 3D:   https://yanwenzhe519-ctrl.github.io/IP-Weave/demo_output/azuki_3d.html")
print(f"  📋 证明: https://yanwenzhe519-ctrl.github.io/IP-Weave/demo_output/proof.html")
print(f"{'='*50}")
