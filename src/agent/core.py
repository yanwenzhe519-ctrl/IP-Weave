"""IP Weave Agent 主循环"""

import os
import json
from loguru import logger
from src.config import settings
from src.utils.llm import glm
from src.utils.style import StyleAnalyzer, StyleChecker
from src.chain.reader import OnChainIPReader
from src.content.generators import StoryGenerator, ScriptGenerator, AssetDesigner
from src.utils.reporter import generate_html_report


class IPWeaveAgent:
    def __init__(self):
        self.reader = OnChainIPReader()
        self.style_analyzer = StyleAnalyzer()
        self.story_gen = StoryGenerator()
        self.script_gen = ScriptGenerator()
        self.asset_gen = AssetDesigner()
        self.chain_data = None
        self.style_profile = None
        self.plan = None
        self.results = {}
        self.output_dir = settings.OUTPUT_DIR

    def run(self, ip_name: str = "", contract: str = "", token_id: int = 1):
        self._print_banner()

        # Step 1
        logger.info("")
        logger.info("═══════════════════════════════════")
        logger.info("📋 [1/6] 读取链上 IP 数据")
        logger.info("═══════════════════════════════════")
        self.chain_data = self.reader.fetch(ip_name=ip_name, contract=contract, token_id=token_id)
        ip_name = self.chain_data.get("metadata", {}).get("name", "未知 IP")
        logger.info(f"  IP: {ip_name}")
        for attr in self.chain_data.get("metadata", {}).get("attributes", []):
            logger.info(f"  ▸ {attr['trait_type']}: {attr['value']}")

        # Step 2
        logger.info("")
        logger.info("═══════════════════════════════════")
        logger.info("📋 [2/6] GLM-5.1 分析风格指纹")
        logger.info("═══════════════════════════════════")
        self.style_profile = self.style_analyzer.extract(self.chain_data)

        # Step 3
        logger.info("")
        logger.info("═══════════════════════════════════")
        logger.info("📋 [3/6] GLM-5.1 制定创作计划")
        logger.info("═══════════════════════════════════")
        self.plan = self._make_plan()
        logger.info(f"  方向: {self.plan.get('narrative_direction', '')}")

        # Step 4-6
        logger.info("")
        logger.info("═══════════════════════════════════")
        logger.info("📋 [4/6] → [6/6] 执行创作并迭代")
        logger.info("═══════════════════════════════════")

        for iteration in range(1, settings.MAX_ITERATIONS + 1):
            logger.info(f"  ── 第 {iteration} 轮 ──")

            if iteration == 1 or not self.results.get("story_check", {}).get("passed", False):
                text = self.story_gen.generate(self.style_profile, self.plan)
                self.results["story_text"] = text

            if iteration == 1 or not self.results.get("script_check", {}).get("passed", False):
                text = self.script_gen.generate(
                    self.results.get("story_text", ""), self.style_profile
                )
                self.results["script_text"] = text

            if iteration == 1 or not self.results.get("asset_check", {}).get("passed", False):
                assets = self.asset_gen.generate(self.style_profile)
                self.results["assets_result"] = assets

            logger.info("  ── GLM-5.1 风格检查 ──")
            checker = StyleChecker(self.style_profile)
            self.results["story_check"] = checker.check(self.results.get("story_text", ""), "故事")
            self.results["script_check"] = checker.check(self.results.get("script_text", ""), "脚本")
            assets_text = json.dumps(self.results.get("assets_result", {}), ensure_ascii=False)
            self.results["asset_check"] = checker.check(assets_text, "资产")

            all_pass = all([
                self.results["story_check"]["passed"],
                self.results["script_check"]["passed"],
                self.results["asset_check"]["passed"],
            ])
            if all_pass:
                logger.info("  ✅ 全部通过！")
                break
            elif iteration < settings.MAX_ITERATIONS:
                logger.info("  ⚠️ 部分未通过，下一轮迭代...")

        self._deliver()

    def _make_plan(self) -> dict:
        prompt = f"""制定衍生内容创作计划，返回 JSON。

风格：{json.dumps(self.style_profile, ensure_ascii=False, indent=2)}

{{
  "narrative_direction": "叙事方向",
  "output_order": ["story","script","assets"],
  "key_elements": ["关键元素"]
}}"""
        result = glm.chat_json([
            {"role": "system", "content": "你是 IP 内容策略师。"},
            {"role": "user", "content": prompt}
        ])
        if not result:
            result = {"narrative_direction": "经典衍生故事", "output_order": ["story","script","assets"], "key_elements": ["IP 核心特征"]}
        logger.success(f"  计划: {result.get('narrative_direction', '')}")
        return result

    def _deliver(self):
        ip_name = self.chain_data.get("metadata", {}).get("name", "IP").replace(" ", "_")
        out_dir = os.path.join(self.output_dir, ip_name)
        os.makedirs(out_dir, exist_ok=True)

        # 保存原始 markdown
        for key, suffix in [("story_text", "story.md"), ("script_text", "animation_script.md")]:
            path = os.path.join(out_dir, suffix)
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.results.get(key, ""))

        assets_path = os.path.join(out_dir, "assets_info.json")
        with open(assets_path, "w", encoding="utf-8") as f:
            json.dump(self.results.get("assets_result", {}), f, ensure_ascii=False, indent=2)

        # 生成 HTML 报告
        report = generate_html_report(
            ip_name=self.chain_data.get("metadata", {}).get("name", "IP"),
            story=self.results.get("story_text", ""),
            script=self.results.get("script_text", ""),
            assets=self.results.get("assets_result", {}),
            output_dir=out_dir,
        )

        logger.info("")
        logger.info("═══════════════════════════════════")
        logger.info("✅ 交付完成！")
        logger.info("═══════════════════════════════════")
        logger.info(f"  📖 故事 → {out_dir}")
        logger.info(f"  🎬 脚本 → {out_dir}")
        logger.info(f"  🧸 资产 → {out_dir}")
        logger.info(f"")
        logger.info(f"  🌐 打开浏览器查看:")
        logger.info(f"     {report['index']}")
        logger.info(f"")
        logger.info(f"  📊 评分:")
        logger.info(f"     故事: {self.results.get('story_check', {}).get('score', '?')}/10")
        logger.info(f"     脚本: {self.results.get('script_check', {}).get('score', '?')}/10")
        logger.info(f"     资产: {self.results.get('asset_check', {}).get('score', '?')}/10")

    def _print_banner(self):
        print("")
        print("╔══════════════════════════════════════╗")
        print("║       IP Weave · 链上衍生宇宙        ║")
        print("║   基于 GLM-5.1 的自治创作 Agent      ║")
        print("╚══════════════════════════════════════╝")
