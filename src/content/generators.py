import json
from loguru import logger
from src.utils.llm import glm


class StoryGenerator:
    def generate(self, profile: dict, plan: dict) -> str:
        logger.info("  -> [GLM-5.1] 创作衍生故事...")
        v = profile.get("visual", {})
        n = profile.get("narrative", {})
        ctx = f"\n".join([
            f"世界观：{n.get(setting,未知)}",
            f"风格基调：{n.get(tone,未知)}",
            f"核心主题：{n.get(core_theme,未知)}",
            f"美术风格：{v.get(art_style,未知)} 配色：{\", \".join(v.get(\"palette\",[\"未知\"]))}",
            f"角色原型：{profile.get(character_archetype,未知)}",
            f"氛围：{\", \".join(profile.get(\"vibe\",[\"未知\"]))}"
        ])
        prompt = f"""你是一位出版过多部畅销小说的职业作家。根据以下IP信息创作衍生故事。

IP背景：
{ctx}

创作方向：{json.dumps(plan, ensure_ascii=False, indent=2)}

要求：
1. 完整故事弧线：起因-发展-转折-高潮-收束
2. 主角有清晰动机和情感变化
3. 场景有画面感
4. 对话自然体现角色
5. 主题有深度
6. 语言有文学质感
7. 2000-4000字

直接写故事。"""
        return glm.chat([
            {"role": "system", "content": "你是出版过畅销小说的职业作家。文风成熟、结构严谨、人物丰满。"},
            {"role": "user", "content": prompt}
        ]) or "# 生成失败"


class ScriptGenerator:
    def generate(self, story: str, profile: dict) -> str:
        logger.info("  -> [GLM-5.1] 生成动画分镜脚本...")
        prompt = f"""你是一位资深动画导演。根据故事和IP风格创作分镜脚本。

视觉风格：{json.dumps(profile.get("visual",{}), ensure_ascii=False, indent=2)}

故事：{story[:3000]}

要求：
1. 分解为6-8个场景
2. 每个分镜含：镜号、场景描述、对白、镜头运动、时长
3. 场景衔接流畅
4. 可直接用于制作

用markdown表格输出。"""
        return glm.chat([
            {"role": "system", "content": "你是资深动画导演。分镜脚本逻辑清晰、画面感强。"},
            {"role": "user", "content": prompt}
        ]) or "# 生成失败"


class AssetDesigner:
    def generate(self, profile: dict) -> dict:
        logger.info("  -> [GLM-5.1] 设计周边资产概念...")
        prompt = f"""你是Web3产品设计师。根据IP风格设计2款可上链的周边资产。

风格：{json.dumps(profile, ensure_ascii=False, indent=2)}

每款需含：名称、类型、设计描述、设计理念、NFT元数据

返回JSON：{{"assets":[{{"name":"","type":"","description":"","concept":"","metadata":{{"name":"","description":"","attributes":[]}},"image_prompt":""}}]}}"""
        result = glm.chat_json([
            {"role": "system", "content": "你是资深Web3产品设计师。设计既有艺术价值又可上链的数字资产。"},
            {"role": "user", "content": prompt}
        ])
        if result and "assets" in result:
            logger.success(f"    设计了 {len(result[assets])} 款")
            for asset in result["assets"]:
                url = glm.generate_image(asset.get("image_prompt",""))
                asset["image_url"] = url or ""
            return result
        return {"assets": []}
