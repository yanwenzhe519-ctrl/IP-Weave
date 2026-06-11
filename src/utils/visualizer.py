"""SVG 图形生成器 — 不依赖任何外部 API，代码直接产出矢量图"""

import os
import re
import logging

logger = logging.getLogger(__name__)


def _extract_color(val: str, fallback: str = "#4ade80") -> str:
    """从调色板条目中提取十六进制颜色码"""
    if not val:
        return fallback
    match = re.search(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})', str(val))
    if match:
        return f"#{match.group(1)}"
    return fallback


def generate_character_svg(palette, name="Character"):
    mc = _extract_color(palette[0] if len(palette) > 0 else "", "#4ade80")
    ac = _extract_color(palette[1] if len(palette) > 1 else "", "#a855f7")
    bg = "#0a0a0f"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 500" width="400" height="500">
<rect width="400" height="500" fill="{bg}"/>
<defs>
  <radialGradient id="frog_glow"><stop offset="0%" stop-color="{mc}" stop-opacity="0.15"/><stop offset="100%" stop-color="{mc}" stop-opacity="0"/></radialGradient>
</defs>
<!-- 背景光晕 -->
<ellipse cx="200" cy="250" rx="180" ry="200" fill="url(#frog_glow)"/>
<!-- 青蛙身体 -->
<ellipse cx="200" cy="320" rx="85" ry="75" fill="{mc}" opacity="0.35" rx2="95"/>
<!-- 青蛙头部（宽扁） -->
<ellipse cx="200" cy="220" rx="90" ry="60" fill="{mc}" opacity="0.4"/>
<!-- 左眼（突出的大眼睛） -->
<circle cx="158" cy="195" r="24" fill="#fff" opacity="0.85"/>
<circle cx="160" cy="195" r="24" fill="{mc}" opacity="0.15"/>
<circle cx="162" cy="194" r="10" fill="#111" opacity="0.8"/>
<circle cx="163" cy="192" r="4" fill="#fff" opacity="0.9"/>
<!-- 右眼（突出的大眼睛） -->
<circle cx="242" cy="195" r="24" fill="#fff" opacity="0.85"/>
<circle cx="240" cy="195" r="24" fill="{mc}" opacity="0.15"/>
<circle cx="238" cy="194" r="10" fill="#111" opacity="0.8"/>
<circle cx="237" cy="192" r="4" fill="#fff" opacity="0.9"/>
<!-- 嘴巴（标志性半圆形） -->
<path d="M160 240 Q200 265 240 240" fill="none" stroke="#111" stroke-width="2" opacity="0.6"/>
<!-- 腮红 -->
<ellipse cx="145" cy="230" rx="12" ry="8" fill="{ac}" opacity="0.12"/>
<ellipse cx="255" cy="230" rx="12" ry="8" fill="{ac}" opacity="0.12"/>
<!-- 前肢 -->
<ellipse cx="130" cy="310" rx="20" ry="12" fill="{mc}" opacity="0.3" transform="rotate(-20 130 310)"/>
<ellipse cx="270" cy="310" rx="20" ry="12" fill="{mc}" opacity="0.3" transform="rotate(20 270 310)"/>
<!-- 头部轮廓光 -->
<ellipse cx="200" cy="218" rx="93" ry="63" fill="none" stroke="{ac}" stroke-width="0.8" opacity="0.2"/>
<text x="200" y="460" text-anchor="middle" fill="#666" font-family="sans-serif" font-size="13">{name}</text>
<text x="200" y="480" text-anchor="middle" fill="#444" font-family="sans-serif" font-size="9">IP Weave · GLM-5.1</text>
</svg>'''


def generate_scene_svg(scene_num, palette, label="", desc=""):
    mc = _extract_color(palette[0] if len(palette) > 0 else "", "#4ade80")
    ac = _extract_color(palette[1] if len(palette) > 1 else "", "#a855f7")
    bg = "#0a0a0f"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 270" width="480" height="270">
<rect width="480" height="270" fill="{bg}"/>
<defs><linearGradient id="sg{scene_num}" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="{mc}"/><stop offset="100%" stop-color="{ac}"/>
</linearGradient></defs>
<rect x="0" y="0" width="480" height="270" fill="url(#sg{scene_num})" opacity="0.12"/>
<line x1="0" y1="135" x2="480" y2="135" stroke="{ac}" stroke-width="0.5" opacity="0.15"/>
<line x1="240" y1="0" x2="240" y2="270" stroke="{ac}" stroke-width="0.5" opacity="0.15"/>
<circle cx="{120 + scene_num * 20}" cy="{100 + scene_num * 15}" r="{30 + scene_num * 3}" fill="{mc}" opacity="0.2"/>
<rect x="{200 + scene_num * 15}" y="{140 - scene_num * 8}" width="50" height="70" rx="4" fill="{ac}" opacity="0.15"/>
<text x="12" y="24" fill="{mc}" font-family="monospace" font-size="14" font-weight="bold">SCENE {scene_num}</text>
<text x="12" y="255" fill="#555" font-family="sans-serif" font-size="8">{label}</text>
<text x="450" y="255" fill="#444" font-family="monospace" font-size="8">00:{scene_num * 2 - 2:02d}</text>
</svg>'''


def generate_asset_svg(palette, name="Asset", idx=1):
    mc = _extract_color(palette[0] if len(palette) > 0 else "", "#4ade80")
    ac = _extract_color(palette[1] if len(palette) > 1 else "", "#a855f7")
    bg = "#0a0a0f"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 350" width="400" height="350">
<rect width="400" height="350" fill="{bg}"/>
<defs><radialGradient id="ag{idx}"><stop offset="0%" stop-color="{mc}" stop-opacity="0.15"/><stop offset="100%" stop-color="{ac}" stop-opacity="0.05"/></radialGradient></defs>
<circle cx="200" cy="160" r="130" fill="url(#ag{idx})"/>
<rect x="150" y="110" width="100" height="100" rx="14" fill="{mc}" opacity="0.2" stroke="{ac}" stroke-width="1.5"/>
<circle cx="200" cy="160" r="35" fill="none" stroke="{ac}" stroke-width="1.5" opacity="0.5"/>
<circle cx="200" cy="160" r="15" fill="{mc}" opacity="0.25"/>
<circle cx="165" cy="120" r="2" fill="{ac}" opacity="0.5"/>
<circle cx="235" cy="135" r="2" fill="{mc}" opacity="0.4"/>
<text x="200" y="310" text-anchor="middle" fill="#888" font-family="sans-serif" font-size="12">{name}</text>
<text x="200" y="330" text-anchor="middle" fill="#444" font-family="sans-serif" font-size="9">概念设计 · IP Weave</text>
</svg>'''


def save_visual_assets(output_dir, style_profile, assets_result):
    """保存 SVG 到输出目录"""
    vdir = os.path.join(output_dir, "visuals")
    os.makedirs(vdir, exist_ok=True)

    palette = style_profile.get("visual", {}).get("palette", ["#4ade80", "#a855f7"])
    ip_name = style_profile.get("character_archetype", "Character")

    # 角色 SVG
    with open(os.path.join(vdir, "character.svg"), "w") as f:
        f.write(generate_character_svg(palette, ip_name))

    # 6 个场景分镜
    scenes = ["世界观建立", "危机出现", "主角出发", "正面交锋", "命运抉择", "新世界开启"]
    for i, desc in enumerate(scenes, 1):
        with open(os.path.join(vdir, f"scene_{i:02d}.svg"), "w") as f:
            f.write(generate_scene_svg(i, palette, f"SCENE {i} · {desc}"))

    # 资产 SVG
    for idx, asset in enumerate(assets_result.get("assets", []), 1):
        with open(os.path.join(vdir, f"asset_{idx:02d}.svg"), "w") as f:
            f.write(generate_asset_svg(palette, asset.get("name", f"Asset #{idx}"), idx))

    # 视觉索引页
    _make_index_html(vdir, ip_name, len(scenes), len(assets_result.get("assets", [])))

    count = 1 + len(scenes) + len(assets_result.get("assets", []))
    logger.info(f"   已生成 {count} 个 SVG 矢量图形 → {vdir}")
    return vdir


def _make_index_html(vdir, ip_name, scene_count, asset_count):
    scene_cards = "".join(
        f'<div class="card"><img src="scene_{i:02d}.svg" alt="Scene {i}"><div class="label">SCENE {i}</div></div>\n'
        for i in range(1, scene_count + 1)
    )
    asset_cards = "".join(
        f'<div class="card"><img src="asset_{i:02d}.svg" alt="Asset {i}"><div class="label">Asset #{i}</div></div>\n'
        for i in range(1, asset_count + 1)
    )

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>视觉资产 · IP Weave</title>
<style>
* {{margin:0;padding:0;box-sizing:border-box;}}
body {{background:#0a0a0f;color:#e0e0e0;font-family:sans-serif;}}
.container {{max-width:1000px;margin:0 auto;padding:40px 24px;}}
h1 {{font-size:2em;background:linear-gradient(135deg,#4ade80,#a855f7);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:4px;}}
h2 {{color:#fff;margin:32px 0 16px;font-size:1.1em;}}
.grid {{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px;}}
.card {{background:#111;border:1px solid #222;border-radius:12px;overflow:hidden;}}
.card img {{width:100%;display:block;}}
.label {{padding:8px 12px;font-size:0.85em;color:#888;}}
.char-card {{max-width:360px;margin:0 auto;}}
.footer {{text-align:center;padding:32px;color:#333;font-size:0.8em;}}
</style></head>
<body><div class="container">
<h1> {ip_name} · 视觉资产</h1>
<p style="color:#666;margin-bottom:24px;">SVG 矢量图形 · 由代码直接生成</p>
<h2> 角色概念</h2>
<div style="display:flex;justify-content:center;"><div class="card char-card"><img src="character.svg" alt="Character"><div class="label">{ip_name}</div></div></div>
<h2>SCRIPT 分镜场景</h2><div class="grid">{scene_cards}</div>
<h2>ASSET 周边资产</h2><div class="grid">{asset_cards}</div>
<div class="footer">由 IP Weave · GLM-5.1 驱动生成</div>
</div></body></html>'''

    with open(os.path.join(vdir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
