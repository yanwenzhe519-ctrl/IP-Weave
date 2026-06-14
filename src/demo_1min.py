#!/usr/bin/env python3
"""1 分钟极速 Demo — 展示 Agent 流程和结果"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DEMO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(DEMO_DIR, "docs", "demo_output")
os.makedirs(OUT, exist_ok=True)

try:
    with open(os.path.join(DEMO_DIR, ".env")) as f:
        for line in f:
            if "ZHIPUAI_API_KEY" in line:
                os.environ["ZHIPUAI_API_KEY"] = line.split("=")[1].strip()
except:
    pass

print("\n" + "="*50)
print("  IP Weave · 1 分钟极速 Demo")
print("="*50)

# 第1步: 链上读取
print("\n[1/5] 读取链上数据...")
from src.chain.reader import OnChainIPReader
reader = OnChainIPReader()
data = reader.fetch(ip_name="azuki")
print(f"  IP: {data.get('name','')} ✅")

# 第2步: GLM-5.1 风格分析
print("[2/5] GLM-5.1 分析风格...")
from src.utils.style import StyleAnalyzer
style = StyleAnalyzer().extract(data)
print(f"  风格: {style.get('narrative',{}).get('tone','')[:50]} ✅")

# 第3步: GLM-5.1 创作故事（限制字数加快速度）
print("[3/5] GLM-5.1 创作故事...")
from src.utils.llm import glm
from src.content.generators import StoryGenerator
plan = {"narrative_direction": "热血青春成长", "key_elements": ["街头", "滑板", "友谊"]}
story = StoryGenerator().generate(style, plan)
print(f"  故事: {len(story)} 字 ✅")

# 第4步: 脚本
print("[4/5] 生成分镜脚本...")
from src.content.generators import ScriptGenerator
script = ScriptGenerator().generate(story[:3000], style)
print(f"  脚本: {len(script)} 字 ✅")

# 第5步: 资产
print("[5/5] 设计周边资产...")
from src.content.generators import AssetDesigner
assets = AssetDesigner().generate(style)
print(f"  资产: {len(assets.get('assets',[]))} 款 ✅")

# 生成文件
print("\n生成交付文件...")
from src.utils.reporter import generate_html_report
from src.utils.visualizer import save_visual_assets
from src.chain.publisher import NFTPublisher
save_visual_assets(OUT, style, assets)
generate_html_report("azuki", story, script, assets, OUT)
pub = NFTPublisher(OUT)
pub.prepare_metadata("azuki", story, script, assets)
pub.generate_deploy_script()

# 证明页
import time
html_parts = []
html_parts.append('<!DOCTYPE html><html><head><meta charset="UTF-8"><title>链上证明</title>')
html_parts.append('<style>body{background:#0a0a0f;color:#e0e0e0;font-family:sans-serif;max-width:800px;margin:0 auto;padding:40px 24px 80px}')
html_parts.append('h1{color:#fff;font-size:2em;border-bottom:1px solid #1a1a2e}')
html_parts.append('h2{color:#4ade80;font-size:1.2em;margin:24px 0 12px}')
html_parts.append('.card{background:#111;border:1px solid #222;border-radius:8px;padding:16px;margin:10px 0}')
html_parts.append('.row{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #0d0d1a;font-size:0.9em}')
html_parts.append('.label{color:#888}.value{color:#4ade80}a{color:#22d3ee}.footer{text-align:center;color:#333;font-size:0.8em;margin-top:40px}')
html_parts.append('</style></head><body>')
html_parts.append(f'<h1>链上证明</h1><p style="color:#888">IP Weave Agent | {time.strftime("%Y-%m-%d %H:%M")}</p>')
html_parts.append('<div class="card"><h2>执行记录</h2>')
html_parts.append(f'<div class="row"><span class="label">IP</span><span class="value">Azuki</span></div>')
html_parts.append(f'<div class="row"><span class="label">故事</span><span class="value">{len(story)} 字</span></div>')
html_parts.append(f'<div class="row"><span class="label">脚本</span><span class="value">{len(script)} 字</span></div>')
html_parts.append(f'<div class="row"><span class="label">资产</span><span class="value">{len(assets.get("assets",[]))} 款</span></div></div>')
html_parts.append('<div class="card"><h2>链上信息</h2>')
html_parts.append('<div class="row"><span class="label">网络</span><span class="value">Sepolia Testnet</span></div>')
html_parts.append('<div class="row"><span class="label">合约</span><span class="value">0x428fc6c80773F44220E7bcb9c7b4833C62F0f343</span></div>')
html_parts.append('<div class="row"><span class="label">钱包</span><span class="value">0x3C215983f524271a4aB1A11E041cDC01ca84B9EC</span></div></div>')
html_parts.append('<div class="footer">IP Weave · GLM-5.1 · Casual Hackathon Z.AI</div></body></html>')
with open(os.path.join(OUT, "proof.html"), "w", encoding="utf-8") as f:
    f.write("\n".join(html_parts))

# 简单的 3D 展示
_3d_html = '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Azuki 3D</title>'
_3d_html += '<style>body{margin:0;overflow:hidden;background:#0a0a0f}</style></head><body>'
_3d_html += '<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}</script>'
_3d_html += '<script type="module">import*as THREE from"three";import{OrbitControls}from"three/addons/controls/OrbitControls.js";const s=new THREE.Scene();s.background=new THREE.Color(0x0a0a0f);const c=new THREE.PerspectiveCamera(35,innerWidth/innerHeight,0.1,100);c.position.set(4,3,5);const r=new THREE.WebGLRenderer({antialias:true});r.setSize(innerWidth,innerHeight);r.shadowMap.enabled=true;document.body.appendChild(r.domElement);new OrbitControls(c,r.domElement).target.set(0,1.2,0);'
_3d_html += 'const b=new THREE.MeshStandardMaterial({color:0xe63946,roughness:0.3,metalness:0.1});const body=new THREE.Mesh(new THREE.CylinderGeometry(0.7,0.5,1.4,8),b);body.position.y=1.1;body.castShadow=true;s.add(body);'
_3d_html += 'const h=new THREE.MeshStandardMaterial({color:0xf5d0a0,roughness:0.4});const head=new THREE.Mesh(new THREE.SphereGeometry(0.5,20,20),h);head.position.y=2.1;head.castShadow=true;s.add(head);'
_3d_html += 'const e=new THREE.MeshStandardMaterial({color:0x111});const el=new THREE.Mesh(new THREE.SphereGeometry(0.06,8,8),e);el.position.set(-0.15,2.2,0.45);s.add(el);const er=new THREE.Mesh(new THREE.SphereGeometry(0.06,8,8),e);er.position.set(0.15,2.2,0.45);s.add(er);'
_3d_html += 'const a=new THREE.AmbientLight(0xffffff,0.6);s.add(a);const k=new THREE.DirectionalLight(0xffffff,1.2);k.position.set(5,8,5);k.castShadow=true;s.add(k);const fl=new THREE.DirectionalLight(0xe63946,0.3);fl.position.set(-3,2,-3);s.add(fl);'
_3d_html += 'const hemi=new THREE.HemisphereLight(0xe63946,0x222244,0.4);s.add(hemi);'
_3d_html += 'function a(){requestAnimationFrame(a);r.render(s,c)}a();'
_3d_html += 'window.addEventListener("resize",()=>{c.aspect=innerWidth/innerHeight;c.updateProjectionMatrix();r.setSize(innerWidth,innerHeight)});'
_3d_html += '</script></body></html>'
with open(os.path.join(OUT, "azuki_3d.html"), "w", encoding="utf-8") as f:
    f.write(_3d_html)

# 输出
print(f"\n{'='*50}")
print(f"  完成! 浏览器打开:")
print(f"\n  📖 故事: https://yanwenzhe519-ctrl.github.io/IP-Weave/demo_output/story.html")
print(f"  🎬 脚本: https://yanwenzhe519-ctrl.github.io/IP-Weave/demo_output/script.html")
print(f"  🧸 资产: https://yanwenzhe519-ctrl.github.io/IP-Weave/demo_output/assets.html")
print(f"  🎨 3D:   https://yanwenzhe519-ctrl.github.io/IP-Weave/demo_output/azuki_3d.html")
print(f"  📋 证明: https://yanwenzhe519-ctrl.github.io/IP-Weave/demo_output/proof.html")
print(f"\n  或直接打开: {OUT}/index.html")
print(f"{'='*50}")
