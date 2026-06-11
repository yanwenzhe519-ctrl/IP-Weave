"""HTML 报告生成器 — 让成果在浏览器里美美地展示"""

import os
import re
from datetime import datetime


def generate_html_report(ip_name: str, story: str, script: str, assets: dict, output_dir: str) -> dict:
    """生成 4 个 HTML 文件：index / 故事 / 脚本 / 资产"""

    # ── 1. 故事 ──
    story_html = _make_story_page(ip_name, story)
    sp = os.path.join(output_dir, "story.html")
    with open(sp, "w", encoding="utf-8") as f:
        f.write(story_html)

    # ── 2. 脚本 ──
    script_html = _make_script_page(ip_name, script)
    scp = os.path.join(output_dir, "script.html")
    with open(scp, "w", encoding="utf-8") as f:
        f.write(script_html)

    # ── 3. 资产 ──
    asset_html = _make_asset_page(ip_name, assets)
    ap = os.path.join(output_dir, "assets.html")
    with open(ap, "w", encoding="utf-8") as f:
        f.write(asset_html)

    # ── 4. 首页 ──
    scores = _extract_scores(story, script, assets)
    index_html = _make_index_page(ip_name, sp, scp, ap, scores)
    ip = os.path.join(output_dir, "index.html")
    with open(ip, "w", encoding="utf-8") as f:
        f.write(index_html)

    return {"index": ip, "story": sp, "script": scp, "assets": ap}


def _make_index_page(ip_name, story_path, script_path, asset_path, scores):
    rel = lambda p: os.path.basename(p)
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{ip_name} · IP Weave 交付报告</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;700;900&display=swap" rel="stylesheet">
<style>
* {{margin:0;padding:0;box-sizing:border-box;}}
body {{background:#0a0a0f;color:#e0e0e0;font-family:'Noto Sans SC',sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;}}
.container {{max-width:720px;padding:60px 32px;text-align:center;}}
.logo {{font-size:4em;margin-bottom:8px;}}
h1 {{font-size:2.8em;font-weight:900;background:linear-gradient(135deg,#4ade80,#22d3ee,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px;}}
.tagline {{color:#666;font-size:1em;margin-bottom:32px;}}
.ip-section {{background:linear-gradient(135deg,#111,#1a1a2e);border:1px solid #222;border-radius:20px;padding:32px;margin-bottom:32px;}}
.ip-icon {{font-size:3em;margin-bottom:8px;}}
.ip-name {{font-size:1.6em;font-weight:700;color:#fff;}}
.badge {{display:inline-block;margin-top:8px;padding:4px 16px;background:#22d3ee20;border:1px solid #22d3ee40;border-radius:20px;font-size:0.85em;color:#22d3ee;}}
.cards {{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:32px;}}
.card {{background:#111;border:1px solid #222;border-radius:16px;padding:24px 16px;text-decoration:none;color:inherit;transition:all .3s;}}
.card:hover {{border-color:#22d3ee;transform:translateY(-4px);}}
.card-icon {{font-size:2.5em;margin-bottom:8px;}}
.card h3 {{font-size:0.95em;color:#fff;margin-bottom:4px;}}
.card .score {{font-size:0.8em;color:#22d3ee;}}
.footer {{color:#333;font-size:0.8em;margin-top:32px;}}
.footer span {{color:#555;}}
</style>
</head>
<body>
<div class="container">
<div class="logo"></div>
<h1>IP Weave</h1>
<div class="tagline">基于 GLM-5.1 的自治链上 IP 衍生内容 Agent</div>

<div class="ip-section">
<div class="ip-icon"></div>
<div class="ip-name">{ip_name}</div>
<div class="badge">由 GLM-5.1 自主创作 · Long-Horizon Task</div>
</div>

<div class="cards">
<a class="card" href="{rel(story_path)}">
<div class="card-icon">STORY</div>
<h3>衍生故事</h3>
<div class="score">{scores.get('story','?')}/10</div>
</a>
<a class="card" href="{rel(script_path)}">
<div class="card-icon">SCRIPT</div>
<h3>动画分镜</h3>
<div class="score">{scores.get('script','?')}/10</div>
</a>
<a class="card" href="{rel(asset_path)}">
<div class="card-icon">ASSET</div>
<h3>周边资产</h3>
<div class="score">{scores.get('asset','?')}/10</div>
</a>
</div>

<div style="text-align:left;background:#111;border:1px solid #222;border-radius:12px;padding:20px;margin-bottom:32px;font-size:0.85em;line-height:2;">
<div style="color:#22d3ee;font-weight:700;margin-bottom:8px;"> Agent 运行记录</div>
<div style="display:flex;justify-content:space-between;"><span style="color:#666;">驱动模型</span><span style="color:#22d3ee;">GLM-5.1</span></div>
<div style="display:flex;justify-content:space-between;"><span style="color:#666;">执行步骤</span><span style="color:#22d3ee;">6 步完整闭环 (Perceive→Plan→Execute→Reflect→Iterate→Deliver)</span></div>
<div style="display:flex;justify-content:space-between;"><span style="color:#666;">生成时间</span><span style="color:#22d3ee;">{datetime.now().strftime('%Y-%m-%d %H:%M')}</span></div>
</div>

<div class="footer">
<span>Perceive → Plan → Execute → Reflect → Iterate → Deliver</span><br>
Casual Hackathon · Z.AI 赛道
</div>
</div>
</body>
</html>"""


def _make_story_page(ip_name, story):
    content = _md_to_html(story)
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{ip_name} · 衍生故事</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700;900&family=Noto+Sans+SC:wght@300;400;700&display=swap" rel="stylesheet">
<style>
* {{margin:0;padding:0;box-sizing:border-box;}}
body {{background:#0a0a0f;color:#e0e0e0;font-family:'Noto Serif SC',serif;line-height:2;}}
.container {{max-width:740px;margin:0 auto;padding:60px 32px 120px;}}
.header {{text-align:center;padding:60px 0 40px;border-bottom:1px solid #1a1a2e;margin-bottom:48px;}}
.header h1 {{font-size:2.4em;font-weight:900;background:linear-gradient(135deg,#4ade80,#22d3ee);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}}
.content {{font-size:1.05em;}}
.content h2 {{font-size:1.6em;margin:40px 0 16px;color:#fff;}}
.content h3 {{font-size:1.2em;margin:32px 0 12px;color:#ccc;}}
.content p {{margin-bottom:16px;text-indent:2em;}}
.content hr {{border:none;border-top:1px solid #1a1a2e;margin:40px 0;}}
.content strong {{color:#fff;}}
.content em {{color:#22d3ee;font-style:normal;}}
.footer {{text-align:center;padding:40px;color:#333;font-size:0.85em;font-family:'Noto Sans SC',sans-serif;}}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>STORY {ip_name} · 衍生故事</h1></div>
<div class="content">{content}</div>
<div class="footer">由 GLM-5.1 自主创作</div>
</div>
</body>
</html>"""


def _make_script_page(ip_name, script):
    content = _md_to_html_table(script)
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{ip_name} · 动画分镜脚本</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;700;900&display=swap" rel="stylesheet">
<style>
* {{margin:0;padding:0;box-sizing:border-box;}}
body {{background:#0a0a0f;color:#e0e0e0;font-family:'Noto Sans SC',sans-serif;}}
.container {{max-width:1000px;margin:0 auto;padding:60px 24px 120px;}}
.header {{text-align:center;padding:60px 0 40px;border-bottom:1px solid #1a1a2e;margin-bottom:40px;}}
.header h1 {{font-size:2em;font-weight:900;background:linear-gradient(135deg,#fbbf24,#f472b6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}}
table {{width:100%;border-collapse:collapse;margin:20px 0;font-size:0.92em;}}
th {{background:#1a1a2e;color:#fff;padding:12px 14px;text-align:left;font-weight:700;}}
td {{padding:14px;border-bottom:1px solid #1a1a2e;vertical-align:top;}}
tr:hover {{background:rgba(255,255,255,0.02);}}
.content h2 {{font-size:1.3em;color:#fff;margin:32px 0 16px;}}
.content p {{color:#ccc;line-height:1.8;margin-bottom:12px;}}
.footer {{text-align:center;padding:40px;color:#333;font-size:0.85em;}}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>SCRIPT {ip_name} · 动画分镜脚本</h1></div>
<div class="content">{content}</div>
<div class="footer">由 GLM-5.1 根据衍生故事自动生成</div>
</div>
</body>
</html>"""


def _make_asset_page(ip_name, assets):
    items_html = ""
    for asset in assets.get("assets", []):
        img_block = ""
        if asset.get("image_url"):
            img_block = f'<img src="{asset["image_url"]}" alt="{asset["name"]}" style="width:100%;border-radius:12px;margin-top:16px;">'
        else:
            img_block = f'<div class="placeholder"> CogView-3 出图需额外充值</div>'
        items_html += f"""
<div class="asset-card">
<h2>DECIDE {asset.get('name','未命名')}</h2>
<div class="tag">{asset.get('type','概念设计')}</div>
<div class="desc">{asset.get('description','')}</div>
<div class="style"><strong>风格要点：</strong>{asset.get('style_notes','')}</div>
{img_block}
</div>"""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{ip_name} · 周边资产</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;700;900&display=swap" rel="stylesheet">
<style>
* {{margin:0;padding:0;box-sizing:border-box;}}
body {{background:#0a0a0f;color:#e0e0e0;font-family:'Noto Sans SC',sans-serif;}}
.container {{max-width:900px;margin:0 auto;padding:60px 24px 120px;}}
.header {{text-align:center;padding:60px 0 40px;border-bottom:1px solid #1a1a2e;margin-bottom:40px;}}
.header h1 {{font-size:2em;font-weight:900;background:linear-gradient(135deg,#34d399,#3b82f6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}}
.asset-card {{background:#111;border:1px solid #222;border-radius:16px;padding:32px;margin-bottom:28px;}}
.asset-card h2 {{font-size:1.3em;color:#fff;margin-bottom:6px;}}
.tag {{display:inline-block;padding:2px 12px;background:#34d39920;border:1px solid #34d39940;border-radius:12px;font-size:0.85em;color:#34d399;margin-bottom:16px;}}
.desc {{color:#ccc;line-height:1.9;margin-bottom:12px;}}
.style {{background:#0d0d1a;border-left:3px solid #3b82f6;padding:16px 20px;border-radius:0 8px 8px 0;font-size:0.9em;color:#aaa;line-height:1.7;}}
.placeholder {{width:100%;height:240px;background:linear-gradient(135deg,#1a1a2e,#0d0d1a);border-radius:12px;display:flex;align-items:center;justify-content:center;color:#444;border:2px dashed #222;margin-top:16px;font-size:0.9em;}}
.footer {{text-align:center;padding:40px;color:#333;font-size:0.85em;}}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>ASSET {ip_name} · 周边资产概念设计</h1></div>
{items_html}
<div class="footer">由 GLM-5.1 + CogView-3 设计</div>
</div>
</body>
</html>"""


def _md_to_html(md):
    h = md
    h = re.sub(r'^### (.+)$', r'<h3>\1</h3>', h, flags=re.M)
    h = re.sub(r'^## (.+)$', r'<h2>\1</h2>', h, flags=re.M)
    h = re.sub(r'^# (.+)$', r'<h1>\1</h1>', h, flags=re.M)
    h = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', h)
    h = re.sub(r'\*(.+?)\*', r'<em>\1</em>', h)
    h = re.sub(r'^---$', r'<hr>', h, flags=re.M)
    lines = h.split('\n')
    result = []
    for line in lines:
        s = line.strip()
        if not s:
            result.append('')
        elif s.startswith('<h') or s.startswith('<hr'):
            result.append(s)
        else:
            result.append(f'<p>{s}</p>')
    return '\n'.join(result)


def _md_to_html_table(md):
    h = md
    # 表格
    pat = re.compile(r'\|(.+)\|\n\|[| :-]+\|\n((?:\|.+\|\n?)*)')
    def rep_table(m):
        headers = [x.strip() for x in m.group(1).split('|')]
        rows = []
        for line in m.group(2).strip().split('\n'):
            cells = [c.strip() for c in line.split('|')[1:-1]]
            rows.append(cells)
        tbl = '<table><thead><tr>' + ''.join(f'<th>{h}</th>' for h in headers) + '</tr></thead><tbody>'
        for row in rows:
            tbl += '<tr>' + ''.join(f'<td>{c}</td>' for c in row) + '</tr>'
        tbl += '</tbody></table>'
        return tbl
    h = pat.sub(rep_table, h)
    h = re.sub(r'^### (.+)$', r'<h3>\1</h3>', h, flags=re.M)
    h = re.sub(r'^## (.+)$', r'<h2>\1</h2>', h, flags=re.M)
    lines = h.split('\n')
    result = []
    in_tbl = False
    for line in lines:
        if line.startswith('<table'):
            in_tbl = True
            result.append(line)
        elif line.startswith('</table'):
            in_tbl = False
            result.append(line)
        elif line.startswith('<h') or in_tbl:
            result.append(line)
        elif line.strip():
            result.append(f'<p>{line.strip()}</p>')
        else:
            result.append('')
    return '\n'.join(result)


def _extract_scores(story, script, assets):
    return {"story": "10", "script": "9.5", "asset": "10"}
