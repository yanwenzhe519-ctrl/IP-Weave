"""内容生成器 — 高质量 prompt 发挥 GLM-5.1 真正实力"""

import json
from loguru import logger
from src.utils.llm import glm


class StoryGenerator:
    def generate(self, style_profile: dict, plan: dict) -> str:
        logger.info("  → [GLM-5.1] 创作衍生故事...")
        # 构建一个详细的 IP 背景描述
        ip_context = self._build_ip_context(style_profile)
        
        prompt = f"""你是一位获得过星云奖的杰出作家。请根据以下 IP 信息，创作一篇高质量的衍生故事。

IP 名称与背景：
{ip_context}

创作方向：
{json.dumps(plan, ensure_ascii=False, indent=2)}

写作要求：
1. 故事必须深刻反映这个 IP 的核心精神气质
2. 开头要有代入感，能立即把读者拉入这个世界
3. 人物要有真实的动机和情感弧线
4. 要有原创性，不是简单的复述已知内容
5. 场景描写要具体，有画面感
6. 对话要自然，能体现角色性格
7. 高潮部分要有情感冲击力
8. 结尾要有余韵，让人回味

直接写故事，不要分析或解释。"""

    def _build_ip_context(self, profile):
        v = profile.get('visual', {})
        n = profile.get('narrative', {})
        ctx = f"""
世界观：{n.get('setting','未知')}
风格基调：{n.get('tone','未知')}
核心主题：{n.get('core_theme','未知')}
视觉风格：{v.get('art_style','未知')}，配色：{', '.join(v.get('palette',['未知']))}
角色原型：{profile.get('character_archetype','未知')}
氛围：{', '.join(profile.get('vibe',['未知']))}
"""
        return ctx
        return glm.chat([
            {"role": "system", "content": "你是星云奖级别的杰出作家。你擅长深入理解 IP 的核心精神，创作出既有原作风骨又有独立文学价值的衍生作品。你的文字有温度、有力度、有记忆点。"},
            {"role": "user", "content": prompt}
        ]) or "# 生成失败"


class ScriptGenerator:
    def generate(self, story: str, style_profile: dict) -> str:
        logger.info("  → [GLM-5.1] 生成动画分镜脚本...")
        prompt = f"""你是一位资深动画导演（代表作入围过昂西动画节）。请根据以下故事和 IP 风格，创作一份专业级别的动画分镜脚本。

IP 视觉风格：
{json.dumps(style_profile.get('visual', {}), ensure_ascii=False, indent=2)}

故事全文：
{story}

要求：
- 将故事分解为 6-8 个场景
- 每个场景要写出具体的视觉氛围、色彩基调、镜头语言
- 要体现导演的独特视角和审美
- 格式用 markdown 表格"""

    def _build_ip_context(self, profile):
        v = profile.get('visual', {})
        n = profile.get('narrative', {})
        ctx = f"""
世界观：{n.get('setting','未知')}
风格基调：{n.get('tone','未知')}
核心主题：{n.get('core_theme','未知')}
视觉风格：{v.get('art_style','未知')}，配色：{', '.join(v.get('palette',['未知']))}
角色原型：{profile.get('character_archetype','未知')}
氛围：{', '.join(profile.get('vibe',['未知']))}
"""
        return ctx
        return glm.chat([
            {"role": "system", "content": "你是昂西动画节入围导演，擅长将文学作品转化为富有视觉冲击力的动画分镜。你的分镜脚本本身就是艺术品。"},
            {"role": "user", "content": prompt}
        ]) or "# 生成失败"


class AssetDesigner:
    def generate(self, style_profile: dict) -> dict:
        logger.info("  → [GLM-5.1] 设计周边资产概念...")
        prompt = f"""你是一位曾与 KAWS 和村上隆合作过的知名潮玩设计师。请根据 IP 风格画像，设计 2 款有收藏价值的周边资产概念。

IP 风格：
{json.dumps(style_profile, ensure_ascii=False, indent=2)}

要求：
- 设计要有落地性，像是真的可以在货架上买到的产品
- 材质、尺寸、工艺细节要具体
- 要有独特的设计亮点，不能是普通的印花贴牌
- 风格要点要明确

返回 JSON：
{{"assets": [
  {{"name":"产品名称","type":"潮玩/服饰/生活用品",
    "description":"详细设计描述（材质、尺寸、工艺、使用场景）",
    "style_notes":"风格要点和设计理念",
    "image_prompt":"英文 AI 出图提示词，详细描述产品外观、材质、光影、构图"}}
]}}"""
        result = glm.chat_json([
            {"role": "system", "content": "你是国际知名的潮玩设计师，作品融合艺术性与商业性，擅长将 IP 文化符号转化为有收藏价值的实体产品。"},
            {"role": "user", "content": prompt}
        ])
        if result and "assets" in result:
            logger.success(f"    设计了 {len(result['assets'])} 款资产概念")
            for asset in result["assets"]:
                url = glm.generate_image(asset.get("image_prompt", ""))
                asset["image_url"] = url or ""
                if url:
                    logger.success(f"      OK 图片已生成")
                else:
                    logger.info(f"      ℹ️ 图片生成需额外充值")
            return result
        return {"assets": []}
