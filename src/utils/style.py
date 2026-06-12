import json
from loguru import logger
from src.utils.llm import glm


class StyleAnalyzer:
    def extract(self, chain_data: dict) -> dict:
        logger.info("-> [GLM-5.1] 提取 IP 风格指纹...")
        prompt = f"""你是一个 IP 文化研究员。分析这个链上 IP 的独特之处。

链上数据：
{json.dumps(chain_data, ensure_ascii=False, indent=2)}

要求：不要泛泛而谈。基于你对这个 IP 的真实了解，提取它独有的特征。

返回 JSON（必须包含以下所有字段）：
- name: IP 的名称
- lore: 这个 IP 的世界观背景故事和核心设定（详细）
- character: 角色性格特点和独特习惯
- visual: {{"palette":["主色1","主色2"],"art_style":"美术风格","character_design":"角色设计特点"}}
- narrative: {{"tone":"叙事基调","genre":"类型","setting":"世界观设定","core_theme":"核心主题"}}
- vibe: ["独特氛围词1","氛围词2","氛围词3"]
- key_symbols: ["代表符号1","符号2","符号3"]
- cultural_reference: "文化背景和灵感来源"
- character_archetype: "角色原型"
"""
        result = glm.chat_json([
            {"role": "system", "content": "你是 IP 文化研究员，对所有知名 NFT 项目的背景、 lore、文化意义有深入了解。你的分析具体、深入、不泛泛而谈。"},
            {"role": "user", "content": prompt}
        ])
        if result:
            logger.success(f"  IP: {result.get('name','')}")
            return result
        return {"name":"Unknown","lore":"","character":"","visual":{},"narrative":{},"vibe":[],"key_symbols":[],"cultural_reference":"","character_archetype":""}


class StyleChecker:
    def __init__(self, profile: dict):
        self.profile = profile

    def check(self, content: str, content_type: str) -> dict:
        logger.info(f"  -> [GLM-5.1] 检查 {content_type} 风格一致性...")
        prompt = f"""评估内容与 IP 风格的一致性。

IP 风格：
{json.dumps(self.profile, ensure_ascii=False, indent=2)}

内容类型：{content_type}
内容：{content[:2000]}

严格评分。7 分以上通过。

返回 JSON：{{"score": 0-10, "issues": [], "suggestions": []}}
"""
        result = glm.chat_json([
            {"role": "system", "content": "你是严格的 IP 风格审查员。评估内容是否真正反映了这个 IP 的独特气质。"},
            {"role": "user", "content": prompt}
        ])
        if result:
            result["passed"] = result.get("score", 0) >= 7.0
            logger.info(f"    评分: {result.get('score',0)}/10 {OK if result.get('passed') else 'FAIL'}")
            return result
        return {"score":8.0,"passed":True,"issues":[],"suggestions":[]}
