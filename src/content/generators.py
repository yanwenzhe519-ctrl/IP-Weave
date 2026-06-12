import json
from loguru import logger
from src.utils.llm import glm


class StoryGenerator:
    def generate(self, profile: dict, plan: dict) -> str:
        logger.info("  -> [GLM-5.1] 创作衍生故事...")
        
        # 使用 IP 独有的背景和 lore
        prompt = f"""你是一位出版过畅销小说的作家。请基于以下 IP 的独特背景创作衍生故事。

IP 名称：{profile.get("name","未知")}
IP 世界观：{profile.get("lore","")}
角色性格：{profile.get("character","")}
文化背景：{profile.get("cultural_reference","")}
代表符号：{json.dumps(profile.get("key_symbols",[]), ensure_ascii=False)}
风格基调：{profile.get("narrative",{}).get("tone","")}
核心主题：{profile.get("narrative",{}).get("core_theme","")}

创作方向：{json.dumps(plan, ensure_ascii=False, indent=2)}

要求：
1. 故事必须根植于这个 IP 的独特世界观和角色设定
2. 角色行为要符合 IP 的性格特点
3. 融入 IP 的代表性符号和元素
4. 完整故事弧线：起因-发展-转折-高潮-收束
5. 场景有画面感，对话自然
6. 2000-4000 字

直接写故事，不要分析。"""
        return glm.chat([
            {"role": "system", "content": f"你是擅长为{profile.get('name','IP')}创作衍生故事的作家。你深入了解这个 IP 的世界观、角色性格和文化背景。"},
            {"role": "user", "content": prompt}
        ]) or "# 生成失败"


class ScriptGenerator:
    def generate(self, story: str, profile: dict) -> str:
        logger.info("  -> [GLM-5.1] 生成动画分镜脚本...")
        prompt = f"""你是一位资深动画导演。根据以下故事和 IP 视觉风格创作分镜脚本。

IP：{profile.get("name","")}
视觉风格：{profile.get("visual",{}).get("art_style","")}
代表符号：{json.dumps(profile.get("key_symbols",[]), ensure_ascii=False)}

故事全文：
{story[:3000]}

要求：
1. 6-8 个分镜
2. 每个含：镜号、场景描述、对白、镜头运动、时长
3. 融入 IP 特有的视觉元素
4. 可用 markdown 表格"""
        return glm.chat([
            {"role": "system", "content": f"你是资深动画导演，擅长将{profile.get('name','IP')}的视觉风格转化为动画分镜。"},
            {"role": "user", "content": prompt}
        ]) or "# 生成失败"


class AssetDesigner:
    def generate(self, profile: dict) -> dict:
        logger.info("  -> [GLM-5.1] 设计周边资产概念...")
        prompt = f"""你是 Web3 产品设计师。根据 IP 的独特文化设计 2 款可上链的周边资产。

IP 名称：{profile.get("name","")}
世界观：{profile.get("lore","")[:300]}
角色特点：{profile.get("character","")[:200]}
代表符号：{json.dumps(profile.get("key_symbols",[]), ensure_ascii=False)}
文化背景：{profile.get("cultural_reference","")[:200]}
视觉风格：{profile.get("visual",{}).get("art_style","")}

要求：设计必须反映这个 IP 独有的文化特征，不能是通用模板。

返回 JSON：
{{"assets":[
  {{"name":"","type":"","description":"设计描述","concept":"设计理念","metadata":{{"name":"","description":"","attributes":[]}},"image_prompt":"英文出图提示词"}}
]}}"""
        result = glm.chat_json([
            {"role": "system", "content": f"你是 Web3 产品设计师，擅长将{profile.get('name','IP')}的文化符号转化为可上链的数字资产。"},
            {"role": "user", "content": prompt}
        ])
        if result and "assets" in result:
            logger.success(f"    设计了 {len(result[assets])} 款")
            for asset in result["assets"]:
                url = glm.generate_image(asset.get("image_prompt",""))
                asset["image_url"] = url or ""
            return result
        return {"assets":[]}
