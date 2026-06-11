"""内容生成器 — 衍生故事 / 动画脚本 / 周边资产"""

import json
from loguru import logger
from src.utils.llm import glm


class StoryGenerator:
    def generate(self, style_profile: dict, plan: dict) -> str:
        logger.info("  → [GLM-5.1] 创作衍生故事...")
        prompt = f"""你是伟大的故事作家。根据以下 IP 风格和创作计划，创作精彩的衍生故事。

风格：{json.dumps(style_profile, ensure_ascii=False, indent=2)}
计划：{json.dumps(plan, ensure_ascii=False, indent=2)}

要求：
- 2000字以内，有完整起承转合
- 保留IP核心风格，但内容必须原创
- 用 markdown 格式"""
        return glm.chat([
            {"role": "system", "content": "你是才华横溢的故事作家。"},
            {"role": "user", "content": prompt}
        ]) or "# 生成失败"


class ScriptGenerator:
    def generate(self, story: str, style_profile: dict) -> str:
        logger.info("  → [GLM-5.1] 生成动画分镜脚本...")
        prompt = f"""你是专业动画导演。把故事转为分镜脚本。

IP 风格：{json.dumps(style_profile, ensure_ascii=False, indent=2)}
故事：{story[:3000]}

拆成 6 个分镜，每个包含：镜号、场景描述、对白、镜头运动、时长。
用 markdown 表格输出。"""
        return glm.chat([
            {"role": "system", "content": "你是专业动画导演和分镜师。"},
            {"role": "user", "content": prompt}
        ]) or "# 生成失败"


class AssetDesigner:
    def generate(self, style_profile: dict) -> dict:
        logger.info("  → [GLM-5.1] 设计周边资产概念...")
        prompt = f"""你是 IP 周边设计师。设计 2 款周边资产。

风格：{json.dumps(style_profile, ensure_ascii=False, indent=2)}

返回 JSON：
{{"assets": [
  {{"name":"名称","type":"角色立绘/道具/场景",
    "description":"详细设计描述","style_notes":"风格要点",
    "image_prompt":"英文 AI 出图提示词（详细描述画面）"}}
]}}"""
        result = glm.chat_json([
            {"role": "system", "content": "你是专业的 IP 周边设计师。"},
            {"role": "user", "content": prompt}
        ])
        if result and "assets" in result:
            logger.success(f"    设计了 {len(result['assets'])} 款资产概念")
            for asset in result["assets"]:
                url = glm.generate_image(asset.get("image_prompt", ""))
                asset["image_url"] = url or ""
                if url:
                    logger.success(f"      ✅ 图片已生成: {url}")
                else:
                    logger.info(f"      ℹ️ 图片生成需额外充值")
            return result
        return {"assets": []}
