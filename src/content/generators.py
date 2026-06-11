"""内容生成器 — 高质量 prompt 发挥 GLM-5.1 真正实力"""

import json
from loguru import logger
from src.utils.llm import glm


class StoryGenerator:
    def generate(self, style_profile: dict, plan: dict) -> str:
        logger.info("  → [GLM-5.1] 创作衍生故事...")
        prompt = f"""你是一位获得过星云奖的科幻作家。请根据以下 IP 的风格画像和创作计划，创作一篇高质量的衍生故事。

IP 风格画像：
{json.dumps(style_profile, ensure_ascii=False, indent=2)}

创作计划：
{json.dumps(plan, ensure_ascii=False, indent=2)}

写作要求：
- 故事必须忠实于原始 IP 的世界观和角色气质
- 要有独特的文学质感，避免 AI 套话
- 人物塑造要有深度，对话要自然
- 场景描写要有画面感
- 篇幅不限，写到故事自然收束为止"""
        return glm.chat([
            {"role": "system", "content": "你是星云奖级别的科幻作家，擅长基于 IP 创作高质量的衍生叙事。你的文风独特，人物鲜活，从不写套路化的内容。"},
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
