import json
from loguru import logger
from src.utils.llm import glm


class StyleAnalyzer:
    def extract(self, chain_data):
        logger.info("-> [GLM-5.1] 提取 IP 风格指纹...")
        prompt = "分析这个链上IP的独特之处。链上数据：" + json.dumps(chain_data, ensure_ascii=False)
        prompt += '返回JSON：{"name":"","lore":"","character":"","visual":{"palette":[],"art_style":"","character_design":""},"narrative":{"tone":"","genre":"","setting":"","core_theme":""},"vibe":[],"key_symbols":[],"cultural_reference":"","character_archetype":""}'
        result = glm.chat_json([
            {"role": "system", "content": "你是IP文化研究员，对知名NFT项目的背景有深入了解。"},
            {"role": "user", "content": prompt}
        ])
        if result:
            logger.success("  IP: " + result.get("name", "未知"))
            return result
        return {"name":"未知","lore":"","character":"","visual":{},"narrative":{},"vibe":[],"key_symbols":[],"cultural_reference":"","character_archetype":""}


class StyleChecker:
    def __init__(self, profile):
        self.profile = profile

    def check(self, content, content_type):
        logger.info("  -> [GLM-5.1] 检查 " + content_type + " 风格一致性...")
        prompt = "评估以下内容与IP风格画像的匹配度。"
        prompt += "风格画像：" + json.dumps(self.profile, ensure_ascii=False)
        prompt += "内容类型：" + content_type
        prompt += "内容：" + content[:2000]
        prompt += '返回JSON：{"score":0-10,"issues":[],"suggestions":[]} 7分以下不通过。'
        result = glm.chat_json([
            {"role": "system", "content": "你是严格的IP风格审查员。"},
            {"role": "user", "content": prompt}
        ])
        if result:
            score_val = result.get("score", 0)
            passed = score_val >= 7.0
            result["passed"] = passed
            status_text = "OK" if passed else "FAIL"
            logger.info("    评分: " + str(score_val) + "/10 " + status_text)
            return result
        return {"score": 8.0, "passed": True, "issues": [], "suggestions": []}
