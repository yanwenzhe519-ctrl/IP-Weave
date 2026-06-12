import json
from loguru import logger
from src.utils.llm import glm


class StoryGenerator:
    def generate(self, profile, plan):
        logger.info("  -> [GLM-5.1] 创作衍生故事...")
        name = str(profile.get("name", "IP"))
        prompt = "你是一位出版过畅销小说的作家。请基于以下IP的独特背景创作衍生故事。"
        prompt += "IP名称：" + name
        prompt += "世界观：" + str(profile.get("lore", ""))[:500]
        prompt += "角色性格：" + str(profile.get("character", ""))[:300]
        prompt += "文化背景：" + str(profile.get("cultural_reference", ""))[:300]
        prompt += "代表符号：" + json.dumps(profile.get("key_symbols", []), ensure_ascii=False)
        prompt += "风格基调：" + str(profile.get("narrative", {}).get("tone", ""))
        prompt += "核心主题：" + str(profile.get("narrative", {}).get("core_theme", ""))
        prompt += "创作方向：" + json.dumps(plan, ensure_ascii=False)
        prompt += "要求：2000-4000字完整故事。直接写故事。"
        return glm.chat([
            {"role": "system", "content": "你是擅长为" + name + "创作衍生故事的作家。你的文风成熟、结构严谨。"},
            {"role": "user", "content": prompt}
        ]) or "# 生成失败"


class ScriptGenerator:
    def generate(self, story, profile):
        logger.info("  -> [GLM-5.1] 生成动画分镜脚本...")
        name = str(profile.get("name", "IP"))
        prompt = "你是一位资深动画导演。根据故事和IP视觉风格创作分镜脚本。"
        prompt += "IP：" + name
        prompt += "视觉风格：" + str(profile.get("visual", {}).get("art_style", ""))
        prompt += "代表符号：" + json.dumps(profile.get("key_symbols", []), ensure_ascii=False)
        prompt += "故事全文：" + story[:3000]
        prompt += "要求：6-8个分镜，每个含镜号、场景描述、对白、镜头运动、时长。"
        return glm.chat([
            {"role": "system", "content": "你是资深动画导演，擅长将IP视觉风格转化为动画分镜。"},
            {"role": "user", "content": prompt}
        ]) or "# 生成失败"


class AssetDesigner:
    def generate(self, profile):
        logger.info("  -> [GLM-5.1] 设计周边资产概念...")
        name = str(profile.get("name", "IP"))
        prompt = "你是Web3产品设计师。根据IP的独特文化设计2款可上链的周边资产。"
        prompt += "IP名称：" + name
        prompt += "世界观：" + str(profile.get("lore", ""))[:300]
        prompt += "角色特点：" + str(profile.get("character", ""))[:200]
        prompt += "代表符号：" + json.dumps(profile.get("key_symbols", []), ensure_ascii=False)
        prompt += "文化背景：" + str(profile.get("cultural_reference", ""))[:200]
        prompt += "视觉风格：" + str(profile.get("visual", {}).get("art_style", ""))
        prompt += '返回JSON：{"assets":[{"name":"","type":"","description":"","concept":"","metadata":{"name":"","description":"","attributes":[]},"image_prompt":""}]}'
        result = glm.chat_json([
            {"role": "system", "content": "你是Web3产品设计师，擅长将IP文化符号转化为可上链的数字资产。"},
            {"role": "user", "content": prompt}
        ])
        if result and "assets" in result:
            count = len(result["assets"])
            logger.success("    设计了 " + str(count) + " 款")
            for asset in result["assets"]:
                url = glm.generate_image(asset.get("image_prompt", ""))
                asset["image_url"] = url or ""
            return result
        return {"assets": []}
