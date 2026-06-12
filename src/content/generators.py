import json
from loguru import logger
from src.utils.llm import glm


class StoryGenerator:
    def generate(self, profile, plan):
        logger.info("  -> [GLM-5.1] 创作衍生故事...")

        name = profile.get("name", "IP")
        lore = profile.get("lore", "")
        char = profile.get("character", "")
        culture = profile.get("cultural_reference", "")
        symbols = json.dumps(profile.get("key_symbols", []), ensure_ascii=False)
        tone = profile.get("narrative", {}).get("tone", "")
        theme = profile.get("narrative", {}).get("core_theme", "")

        prompt = f"""你是一位出版过畅销小说的作家。请基于以下IP的独特背景创作衍生故事。

IP名称：{name}
IP世界观：{lore}
角色性格：{char}
文化背景：{culture}
代表符号：{symbols}
风格基调：{tone}
核心主题：{theme}

创作方向：{json.dumps(plan, ensure_ascii=False, indent=2)}

要求：
1. 故事必须根植于这个IP的独特世界观和角色设定
2. 角色行为要符合IP的性格特点
3. 融入IP的代表性符号和元素
4. 完整故事弧线
5. 场景有画面感，对话自然
6. 2000-4000字

直接写故事。"""
        return glm.chat([
            {"role": "system", "content": f"你是擅长为{name}创作衍生故事的作家。"},
            {"role": "user", "content": prompt}
        ]) or "# 生成失败"


class ScriptGenerator:
    def generate(self, story, profile):
        logger.info("  -> [GLM-5.1] 生成动画分镜脚本...")
        name = profile.get("name", "IP")
        art_style = profile.get("visual", {}).get("art_style", "")
        symbols = json.dumps(profile.get("key_symbols", []), ensure_ascii=False)

        prompt = f"""你是一位资深动画导演。根据故事和IP视觉风格创作分镜脚本。

IP：{name}
视觉风格：{art_style}
代表符号：{symbols}

故事全文：
{story[:3000]}

要求：
1. 6-8个分镜
2. 每个含：镜号、场景描述、对白、镜头运动、时长
3. 融入IP特有的视觉元素
4. 可用markdown表格"""
        return glm.chat([
            {"role": "system", "content": f"你是资深动画导演，擅长将{name}的视觉风格转化为动画分镜。"},
            {"role": "user", "content": prompt}
        ]) or "# 生成失败"


class AssetDesigner:
    def generate(self, profile):
        logger.info("  -> [GLM-5.1] 设计周边资产概念...")
        name = profile.get("name", "IP")
        lore = profile.get("lore", "")[:300]
        char = profile.get("character", "")[:200]
        symbols = json.dumps(profile.get("key_symbols", []), ensure_ascii=False)
        culture = profile.get("cultural_reference", "")[:200]
        art_style = profile.get("visual", {}).get("art_style", "")

        prompt = f"""你是Web3产品设计师。根据IP的独特文化设计2款可上链的周边资产。

IP名称：{name}
世界观：{lore}
角色特点：{char}
代表符号：{symbols}
文化背景：{culture}
视觉风格：{art_style}

要求：设计必须反映这个IP独有的文化特征。

返回JSON：
{{"assets":[
  {{"name":"","type":"","description":"设计描述","concept":"设计理念","metadata":{{"name":"","description":"","attributes":[]}},"image_prompt":"英文出图提示词"}}
]}}"""
        result = glm.chat_json([
            {"role": "system", "content": f"你是Web3产品设计师，擅长将{name}的文化符号转化为可上链的数字资产。"},
            {"role": "user", "content": prompt}
        ])
        if result and "assets" in result:
            count = len(result["assets"])
            logger.success(f"    设计了 {count} 款")
            for asset in result["assets"]:
                url = glm.generate_image(asset.get("image_prompt", ""))
                asset["image_url"] = url or ""
            return result
        return {"assets": []}
