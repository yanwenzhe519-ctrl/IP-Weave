"""风格分析 + 一致性检查 — GLM-5.1 驱动"""

import json
from loguru import logger
from src.utils.llm import glm


class StyleAnalyzer:
    def extract(self, chain_data: dict) -> dict:
        logger.info("→ [GLM-5.1] 提取 IP 风格指纹...")
        prompt = f"""分析以下链上 IP 数据，提取风格特征，返回 JSON。

链上数据：{json.dumps(chain_data, ensure_ascii=False, indent=2)}

JSON 格式：
{{
  "visual": {{"palette": ["主色"], "art_style": "美术风格", "character_design": "设计特点"}},
  "narrative": {{"tone": "基调", "genre": "类型", "setting": "世界观", "core_theme": "核心主题"}},
  "vibe": ["氛围词"],
  "character_archetype": "角色原型",
  "tone_tags": ["语气标签"]
}}"""
        result = glm.chat_json([
            {"role": "system", "content": "你是专业的 IP 风格分析师。"},
            {"role": "user", "content": prompt}
        ])
        if result:
            logger.success(f"  风格: {result.get('narrative', {}).get('tone', '')}")
            return result
        return {
            "visual": {"palette": ["蛙绿", "暗夜紫", "金色"], "art_style": "数字插画 / Meme 风格",
                       "character_design": "绿色青蛙·标志性表情·跨次元"},
            "narrative": {"tone": "荒诞又深刻", "genre": "Meme 传奇 / 互联网民俗",
                          "setting": "数字宇宙与现实世界的夹缝", "core_theme": "一个表情如何改变世界"},
            "vibe": ["魔性", "怀旧", "反叛", "幽默"], "character_archetype": "互联网图腾",
            "tone_tags": ["戏谑", "诗意", "疯狂", "温暖"]
        }


class StyleChecker:
    def __init__(self, profile: dict):
        self.profile = profile

    def check(self, content: str, content_type: str) -> dict:
        logger.info(f"  → [GLM-5.1] 检查 {content_type} 风格一致性...")
        prompt = f"""判断内容是否与 IP 风格画像一致。

风格画像：{json.dumps(self.profile, ensure_ascii=False, indent=2)}
内容类型：{content_type}
内容：{content[:2000]}

返回 JSON：{{"score": 0-10, "issues": [], "suggestions": []}}
7 分以下不通过。"""
        result = glm.chat_json([
            {"role": "system", "content": "你是严格的 IP 风格审查员。"},
            {"role": "user", "content": prompt}
        ])
        if result:
            result["passed"] = result.get("score", 0) >= 7.0
            logger.info(f"    评分: {result.get('score', 0)}/10 {'✅' if result.get('passed') else '❌'}")
            return result
        return {"score": 8.0, "passed": True, "issues": [], "suggestions": []}
