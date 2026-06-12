#!/usr/bin/env python3
import json, os, base64, httpx, re
from datetime import datetime

DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop")
API_KEY = "8d8ffff0a0d1467991a089cdc58d799d.9GhcEVtLT1nPYsyf"
API_URL = "https://api.z.ai/api/coding/paas/v4/chat/completions"

def glm(msg, system="", json_mode=False):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    msgs = []
    if system: msgs.append({"role": "system", "content": system})
    msgs.append({"role": "user", "content": msg})
    payload = {"model": "glm-5.1", "messages": msgs, "max_tokens": 4096}
    if json_mode: payload["response_format"] = {"type": "json_object"}
    try:
        resp = httpx.post(API_URL, headers=headers, json=payload, timeout=180)
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"ERROR: {e}"
    return ""

print("IP Weave Demo")
print()

ip_name = input("链上 IP: ").strip() or "azuki"
print(f"目标: {ip_name}")
print()

# 读取链上数据
print("步骤 1: 读取链上数据")
chain_name = ip_name
try:
    from web3 import Web3
    KNOWN = {"pepe":"0x6982508145454Ce325dDbE47a25d4ec3d2311933","bayc":"0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D","punk":"0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB","azuki":"0xED5AF388653567Af2F388E6224dC7C4b3241C544"}
    addr = KNOWN.get(ip_name.lower(), "")
    if addr:
        w3 = Web3(Web3.HTTPProvider("https://ethereum-rpc.publicnode.com"))
        abi = json.loads('[{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"}]')
        c = w3.eth.contract(address=w3.to_checksum_address(addr), abi=abi)
        chain_name = c.functions.name().call()
        print(f"  IP: {chain_name}")
except:
    pass

# 分析风格
print("步骤 2: GLM-5.1 分析风格")
style_result = glm(
    f"分析链上IP {chain_name} 的独特风格和文化背景。"
    f"返回JSON格式: {{\"lore\":\"世界观背景\",\"character\":\"角色性格\",\"tone\":\"风格基调\",\"setting\":\"世界观设定\",\"theme\":\"核心主题\",\"symbols\":[\"代表符号\"],\"vibe\":\"氛围描述\"}}",
    system="你是IP文化研究员。",
    json_mode=True
)
try:
    style = json.loads(style_result)
except:
    style = {"lore":"", "character":"", "tone":"", "setting":"", "theme":"", "symbols":[], "vibe":""}
print(f"  基调: {style.get('tone','')}")

# 创作故事
print("步骤 3: GLM-5.1 创作衍生故事")
story = glm(
    f"根据以下IP信息创作一篇完整的衍生故事。\n\n"
    f"IP名称: {chain_name}\n"
    f"世界观: {style.get('setting','')}\n"
    f"角色性格: {style.get('character','')}\n"
    f"文化背景: {style.get('lore','')}\n"
    f"核心主题: {style.get('theme','')}\n"
    f"氛围: {style.get('vibe','')}\n\n"
    f"要求: 写一个完整故事,包括开头发展高潮结局。人物要有真实动机和情感变化。"
    f"2000到4000字。直接写故事,不要介绍不要分析不要评论。",
    system="你是出版过畅销小说的职业作家。"
)
# 清理故事中的 markdown 符号
story = re.sub(r'\*\*', '', story)
story = re.sub(r'##?\s*', '', story)
story = re.sub(r'---', '', story)
print(f"  字数: {len(story)}")

# 生成动画分镜脚本
print("步骤 4: GLM-5.1 生成动画分镜脚本")
script = glm(
    f"根据以下故事创作动画分镜脚本,供动画制作团队直接使用。\n\n"
    f"故事:\n{story[:3000]}\n\n"
    f"创作6到8个分镜,每个分镜包含:\n"
    f"镜号: 数字编号\n"
    f"画面: 场景描述,画面构成,色彩基调\n"
    f"对白: 角色的台词或旁白\n"
    f"镜头: 镜头运动方式(推拉摇移跟升降)\n"
    f"时长: 秒数\n\n"
    f"每个分镜之间用一行 --- 分隔。不要介绍不要评论,直接写分镜。",
    system="你是资深动画导演,参与过多部动画电影的分镜设计。"
)
print(f"  分镜数: {len(script)} 字")

# 设计资产
print("步骤 5: GLM-5.1 设计周边资产")
assets_json = glm(
    f"为IP {chain_name} 设计2款可以铸造为NFT的周边资产概念。\n\n"
    f"IP背景: {style.get('lore','')[:200]}\n"
    f"风格: {style.get('tone','')}\n"
    f"代表符号: {json.dumps(style.get('symbols',[]), ensure_ascii=False)}\n\n"
    f"返回JSON格式:\n"
    f"{{\"assets\":[{{\"name\":\"产品名称\",\"type\":\"类型\",\"description\":\"详细设计描述包括材质尺寸和使用场景\",\"concept\":\"设计理念和灵感来源\"}}]}}",
    system="你是Web3产品设计师。",
    json_mode=True
)
try:
    assets = json.loads(assets_json)
except:
    assets = {"assets":[]}
print(f"  设计: {len(assets.get('assets',[]))} 款")

# 生成 HTML 文件
print("\n生成交付文件...")
out = os.path.join(DESKTOP, "IP-Weave成果")
os.makedirs(out, exist_ok=True)

# 故事 HTML - 干净排版
story_clean = re.sub(r'\n\n\n+', '\n\n', story.strip())
story_para = ''.join(f'<p>{p}</p>' for p in story_clean.split('\n') if p.strip())

with open(os.path.join(out, "story.html"), "w", encoding="utf-8") as f:
    f.write(f'''<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>{chain_name} 衍生故事 - IP Weave</title>
<style>
body{{background:#0a0a0f;color:#d0d0d0;font-family:'Noto Serif SC',serif;line-height:2;max-width:740px;margin:0 auto;padding:60px 24px 120px}}
h1{{color:#ffffff;font-size:2.2em;font-weight:700;text-align:center;margin-bottom:8px}}
.sub{{text-align:center;color:#666;font-size:0.9em;margin-bottom:48px;padding-bottom:24px;border-bottom:1px solid #1a1a2e}}
p{{margin-bottom:16px;text-indent:2em;color:rgba(255,255,255,0.85)}}
.footer{{text-align:center;color:#333;font-size:0.8em;margin-top:80px;padding-top:24px;border-top:1px solid #1a1a2e}}
</style></head>
<body>
<h1>{chain_name}</h1>
<div class="sub">衍生故事 · IP Weave · GLM-5.1 · {datetime.now().strftime('%Y-%m-%d')}</div>
{story_para}
<div class="footer">由 IP Weave Agent 基于 GLM-5.1 自主生成 · Casual Hackathon Z.AI 赛道</div>
</body></html>''')

# 脚本 HTML - 分镜表格格式
script_clean = re.sub(r'\*\*', '', script)
scenes = script_clean.split('---')
scene_html = ""
for i, scene in enumerate(scenes, 1):
    scene = scene.strip()
    if not scene: continue
    lines = scene.split('\n')
    details = {}
    current_key = ""
    for line in lines:
        line = line.strip()
        if not line: continue
        for key in ["镜号", "画面", "对白", "镜头", "时长"]:
            if line.startswith(key):
                details[key] = line[len(key):].strip().lstrip(": ")
                current_key = key
                break
        if current_key and not any(line.startswith(k) for k in ["镜号", "画面", "对白", "镜头", "时长"]):
            details[current_key] = (details.get(current_key, "") + " " + line).strip()

    scene_html += f'''
<div style="background:#111;border:1px solid #222;border-radius:8px;padding:20px;margin-bottom:16px">
<div style="display:flex;gap:12px;align-items:center;margin-bottom:12px">
<span style="background:#4ade80;color:#000;padding:2px 12px;border-radius:4px;font-weight:700;font-size:0.9em">SCENE {i}</span>
<span style="color:#888;font-size:0.9em">{details.get("镜号","")} {details.get("时长","")}</span>
</div>
<div style="color:#ccc;line-height:1.8;font-size:0.95em">
<div style="margin-bottom:8px"><span style="color:#4ade80;font-weight:600">画面:</span> {details.get("画面","")}</div>
<div style="margin-bottom:8px"><span style="color:#f472b6;font-weight:600">镜头:</span> {details.get("镜头","")}</div>
<div style="margin-bottom:8px"><span style="color:#fbbf24;font-weight:600">对白:</span> {details.get("对白","")}</div>
</div>
</div>'''

with open(os.path.join(out, "script.html"), "w", encoding="utf-8") as f:
    f.write(f'''<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>{chain_name} 动画分镜脚本 - IP Weave</title>
<style>
body{{background:#0a0a0f;color:#d0d0d0;font-family:'Noto Sans SC',sans-serif;max-width:800px;margin:0 auto;padding:60px 24px 120px}}
h1{{color:#ffffff;font-size:2.2em;font-weight:700;text-align:center}}
.sub{{text-align:center;color:#666;font-size:0.9em;margin-bottom:48px;padding-bottom:24px;border-bottom:1px solid #1a1a2e}}
.footer{{text-align:center;color:#333;font-size:0.8em;margin-top:60px;padding-top:24px;border-top:1px solid #1a1a2e}}
</style></head>
<body>
<h1>{chain_name}</h1>
<div class="sub">动画分镜脚本 · IP Weave · GLM-5.1</div>
{scene_html}
<div class="footer">由 IP Weave Agent 基于 GLM-5.1 自主生成 · Casual Hackathon Z.AI 赛道</div>
</body></html>''')

# 资产 HTML
asset_cards = ""
for a in assets.get("assets", []):
    asset_cards += f'''
<div style="background:#111;border:1px solid #222;border-radius:12px;padding:24px;margin-bottom:20px">
<div style="font-size:1.2em;color:#fff;font-weight:600;margin-bottom:4px">{a.get("name","")}</div>
<div style="color:#4ade80;font-size:0.85em;margin-bottom:12px">{a.get("type","")}</div>
<div style="color:#ccc;line-height:1.8;margin-bottom:12px">{a.get("description","")}</div>
<div style="color:#888;font-size:0.9em;line-height:1.7;padding:12px;background:#0d0d1a;border-radius:6px"><strong style="color:#aaa;">设计理念:</strong> {a.get("concept","")}</div>
</div>'''

with open(os.path.join(out, "assets.html"), "w", encoding="utf-8") as f:
    f.write(f'''<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>{chain_name} 周边资产 - IP Weave</title>
<style>
body{{background:#0a0a0f;color:#d0d0d0;font-family:'Noto Sans SC',sans-serif;max-width:800px;margin:0 auto;padding:60px 24px 120px}}
h1{{color:#ffffff;font-size:2.2em;font-weight:700;text-align:center}}
.sub{{text-align:center;color:#666;font-size:0.9em;margin-bottom:48px;padding-bottom:24px;border-bottom:1px solid #1a1a2e}}
.footer{{text-align:center;color:#333;font-size:0.8em;margin-top:60px;padding-top:24px;border-top:1px solid #1a1a2e}}
</style></head>
<body>
<h1>{chain_name}</h1>
<div class="sub">周边资产概念设计 · IP Weave · GLM-5.1</div>
{asset_cards}
<div class="footer">由 IP Weave Agent 基于 GLM-5.1 自主生成 · Casual Hackathon Z.AI 赛道</div>
</body></html>''')

# Index page
with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
    f.write(f'''<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>IP Weave - {chain_name}</title>
<style>
body{{background:#0a0a0f;color:#d0d0d0;font-family:'Noto Sans SC',sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh}}
.container{{max-width:480px;padding:40px;text-align:center}}
h1{{font-size:2.5em;font-weight:700;background:linear-gradient(135deg,#4ade80,#22d3ee);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}}
.tagline{{color:#666;margin-bottom:32px}}
.card{{display:block;background:#111;border:1px solid #222;border-radius:12px;padding:20px;margin:12px 0;text-decoration:none;color:#d0d0d0;transition:all 0.2s}}
.card:hover{{border-color:#4ade80;transform:translateY(-2px)}}
.card-icon{{font-size:1.5em;display:block;margin-bottom:4px}}
.card-title{{font-size:1.1em;color:#fff;font-weight:600}}
.card-desc{{font-size:0.85em;color:#666;margin-top:4px}}
.footer{{color:#333;font-size:0.8em;margin-top:40px}}
</style></head>
<body>
<div class="container">
<h1>IP Weave</h1>
<div class="tagline">{chain_name} · 基于 GLM-5.1 的链上 IP 衍生内容 Agent</div>
<a class="card" href="story.html">
<span class="card-icon">★</span>
<div class="card-title">衍生故事</div>
<div class="card-desc">{len(story)} 字的完整叙事</div>
</a>
<a class="card" href="script.html">
<span class="card-icon">★</span>
<div class="card-title">动画分镜脚本</div>
<div class="card-desc">专业分镜格式</div>
</a>
<a class="card" href="assets.html">
<span class="card-icon">★</span>
<div class="card-title">周边资产概念</div>
<div class="card-desc">{len(assets.get('assets',[]))} 款可上链资产设计</div>
</a>
<div class="footer">IP Weave · GLM-5.1 · Casual Hackathon Z.AI</div>
</div>
</body></html>''')

print(f"\n完成! 文件在桌面 IP-Weave成果 文件夹")
print(f"  index.html   - 首页")
print(f"  story.html   - 衍生故事 ({len(story)} 字)")
print(f"  script.html  - 动画分镜 ({len(script)} 字, {scene_html.count('SCENE')} 个分镜)")
print(f"  assets.html  - 周边资产 ({len(assets.get('assets',[]))} 款)")

print("步骤 6: 混元 3D 生成周边资产模型...")
HUNYUAN_KEY = "GMH0WpwoRpTu77tRfnhNp434Ypqc9SWL"
import time

def gen_3d(prompt_text):
    try:
        resp = httpx.post(
            "https://tokenhub.tencentmaas.com/v1/api/3d/submit",
            headers={"Authorization": f"Bearer {HUNYUAN_KEY}", "Content-Type": "application/json"},
            json={"model": "hy-3d-3.1", "prompt": prompt_text, "face_count": 50000, "result_format": "glb"},
            timeout=30
        )
        if resp.status_code != 200: return None
        task_id = resp.json().get("data", {}).get("task_id", "")
        if not task_id: return None
        print(f"  3D任务已提交: {task_id[:16]}... 等待生成...")
        for _ in range(20):
            time.sleep(10)
            qr = httpx.post("https://tokenhub.tencentmaas.com/v1/api/3d/query",
                headers={"Authorization": f"Bearer {HUNYUAN_KEY}"},
                json={"model": "hy-3d-3.1", "task_id": task_id}, timeout=30)
            if qr.status_code != 200: continue
            s = qr.json().get("data", {}).get("status", "")
            if s == "completed":
                url = qr.json().get("data", {}).get("model_url", "")
                print(f"  3D完成: {url[:60]}...")
                return url
            elif s == "failed":
                print(f"  3D生成失败")
                return None
        print(f"  3D超时")
    except Exception as e:
        print(f"  3D错误: {str(e)[:60]}")
    return None

for i, asset in enumerate(assets.get("assets", [])):
    name = asset.get("name", f"Asset {i+1}")
    desc = asset.get("description", "")[:200]
    prompt_3d = f"3D model of {name}, {desc}, stylized collectible, game-ready asset, PBR texture"
    print(f"  生成3D: {name[:30]}...")
    model_url = gen_3d(prompt_3d)
    if model_url:
        asset["model_url"] = model_url
        print(f"    模型链接: {model_url}")
        # 生成NFT元数据
        meta = {"name": f"IP Weave - {name}", "description": desc[:200],
                "image": model_url, "animation_url": model_url,
                "attributes": [{"trait_type": "IP", "value": ip_name},
                               {"trait_type": "Format", "value": "GLB"},
                               {"trait_type": "Generator", "value": "Hunyuan 3D"}]}
        meta_b64 = base64.b64encode(json.dumps(meta, ensure_ascii=False).encode()).decode()
        asset["metadata_uri"] = f"data:application/json;base64,{meta_b64}"
        print(f"    NFT元数据已生成")
    else:
        print(f"    3D生成跳过")
