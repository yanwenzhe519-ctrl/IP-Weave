import os
import json
from loguru import logger
from src.config import settings
from src.utils.llm import glm
from src.chain.reader import OnChainIPReader
from src.utils.style import StyleAnalyzer, StyleChecker
from src.content.generators import StoryGenerator, ScriptGenerator, AssetDesigner


class Agent:
    def __init__(self):
        self.state = {"ip": "", "data": None, "style": None, "story": "", "script": "", "assets": {}, "scores": {}}
        self.history = []

    def run(self, ip_name=""):
        self.state["ip"] = ip_name
        logger.info("[AGENT] 目标: " + ip_name + " 生成衍生故事/动画脚本/周边资产")

        tools = [
            {"name": "read_ip", "desc": "从以太坊主网读取IP链上数据"},
            {"name": "analyze_style", "desc": "用GLM-5.1分析IP风格指纹"},
            {"name": "write_story", "desc": "用GLM-5.1创作衍生故事"},
            {"name": "write_script", "desc": "将故事转为动画分镜脚本"},
            {"name": "design_assets", "desc": "设计周边资产概念"},
            {"name": "check_quality", "desc": "评估内容风格一致性"},
        ]

        for rnd in range(15):
            logger.info("[LOOP] 思考循环 " + str(rnd+1))
            decision = self._think(tools)
            if not decision:
                break

            action = decision.get("action", "")
            reason = decision.get("reason", "")
            logger.info("[REASON] " + reason[:100])
            logger.info("[DECIDE] " + action)

            if action == "done":
                logger.info("[DONE] 任务完成")
                self._deliver()
                break

            ok = self._execute(action)
            logger.info("[OK] " + action if ok else "[FAIL] " + action)

        if self.state.get("story") or self.state.get("script") or self.state.get("assets"):
            self._deliver()

    def _think(self, tools):
        status = "IP: " + self.state["ip"] + "\n"
        status += "data: " + ("已读取" if self.state["data"] else "空") + "\n"
        status += "style: " + ("已分析" if self.state["style"] else "空") + "\n"
        status += "story: " + str(len(self.state.get("story", ""))) + "字\n"
        status += "script: " + str(len(self.state.get("script", ""))) + "字\n"
        status += "assets: " + ("有" if self.state.get("assets", {}).get("assets") else "空\n")

        prompt = "你是IP Weave Agent总指挥。目标是给" + self.state["ip"] + "生成衍生故事/动画脚本/周边资产。\n\n当前状态:\n" + status
        prompt += "\n可用工具:\n" + "\n".join(["  " + t["name"] + ": " + t["desc"] for t in tools])
        prompt += '\n\n返回JSON: {"action":"工具名或done","reason":"理由"}'
        prompt += "\n先读数据再分析风格再创作再检查。不要重复已完成的工作。"

        return glm.chat_json([
            {"role": "system", "content": "你是IP Weave总指挥。分析状态决定下一步。"},
            {"role": "user", "content": prompt}
        ])

    def _execute(self, action):
        try:
            if action == "read_ip":
                reader = OnChainIPReader()
                self.state["data"] = reader.fetch(ip_name=self.state["ip"])
                return True
            elif action == "analyze_style":
                if not self.state["data"]: return False
                self.state["style"] = StyleAnalyzer().extract(self.state["data"])
                return bool(self.state["style"])
            elif action == "write_story":
                if not self.state.get("style"): return False
                style = self.state["style"]
                plan = glm.chat_json([{"role":"system","content":"策略师"},{"role":"user","content":"计划。风格:"+json.dumps(style,ensure_ascii=False)+' 返回JSON:{"direction":"方向"}'}]) or {}
                text = StoryGenerator().generate(style, plan)
                if text and len(text) > 200:
                    self.state["story"] = text; return True
                return False
            elif action == "write_script":
                if not self.state.get("story") or not self.state.get("style"): return False
                text = ScriptGenerator().generate(self.state["story"], self.state["style"])
                if text and len(text) > 100:
                    self.state["script"] = text; return True
                return False
            elif action == "design_assets":
                if not self.state.get("style"): return False
                self.state["assets"] = AssetDesigner().generate(self.state["style"])
                return bool(self.state["assets"].get("assets"))
            elif action == "check_quality":
                if not self.state.get("style"): return False
                checker = StyleChecker(self.state["style"])
                results = {}
                if self.state.get("story"): results["story"] = checker.check(self.state["story"], "故事")
                if self.state.get("script"): results["script"] = checker.check(self.state["script"], "脚本")
                if self.state.get("assets"): results["assets"] = checker.check(json.dumps(self.state["assets"],ensure_ascii=False), "资产")
                self.state["scores"] = results
                return True
        except Exception as e:
            logger.info("[ERROR] " + str(e)[:80])
            return False

    def _deliver(self):
        from src.chain.publisher import NFTPublisher
        from src.utils.reporter import generate_html_report
        from src.utils.visualizer import save_visual_assets
        ip = self.state["ip"]
        out = os.path.join(settings.OUTPUT_DIR, ip)
        os.makedirs(out, exist_ok=True)
        save_visual_assets(out, self.state.get("style",{}), self.state.get("assets",{}))
        generate_html_report(ip, self.state.get("story",""), self.state.get("script",""), self.state.get("assets",{}), out)
        pub = NFTPublisher(out)
        pub.prepare_metadata(ip, self.state.get("story",""), self.state.get("script",""), self.state.get("assets",{}))
        pub.generate_deploy_script()
        logger.info("[DONE] 交付: " + out)
        logger.info("[DONE] 衍生故事: output/" + ip + "/story.html")
        logger.info("[DONE] 动画脚本: output/" + ip + "/script.html")
        logger.info("[DONE] 周边资产: output/" + ip + "/assets.html")
        logger.info("[DONE] NFT合约: output/" + ip + "/nft/")
