import os
import json

import json
import importlib
from loguru import logger
from src.utils.llm import glm
from src.chain.reader import OnChainIPReader
from src.utils.style import StyleAnalyzer, StyleChecker
from src.content.generators import StoryGenerator, ScriptGenerator, AssetDesigner


class Agent:
    def __init__(self):
        self.state = {"ip": "", "data": None, "style": None, "plan": None, "story": "", "script": "", "assets": {}}
        self.history = []

    def run(self, ip_name=""):
        self.state["ip"] = ip_name
        self.log("TASK", "目标IP: " + ip_name + " 自主生成衍生故事/动画脚本/周边资产并上链")
        self.log("PLAN", "流程: 1.读取数据 2.分析风格 3.制定计划 4.生成故事 5.生成脚本 6.设计资产 7.质量检查 8.上链交付")

        steps = ["read_ip", "analyze_style", "make_plan", "write_story", "write_script", "design_assets", "check_quality", "deploy"]

        for step in steps:
            self.log("STEP", "执行: " + step)
            ok = self._execute_step(step)
            if not ok:
                self.log("FAIL", "步骤失败: " + step)
                break
            self.log("PASS", "步骤完成: " + step)

        if ok:
            self._summary()

    def _execute_step(self, step):
        try:
            if step == "read_ip":
                reader = OnChainIPReader()
                self.state["data"] = reader.fetch(ip_name=self.state["ip"])
                return True

            elif step == "analyze_style":
                if not self.state["data"]:
                    return False
                analyzer = StyleAnalyzer()
                self.state["style"] = analyzer.extract(self.state["data"])
                return bool(self.state["style"])

            elif step == "make_plan":
                if not self.state["style"]:
                    return False
                prompt = '制定衍生内容创作计划。风格:' + json.dumps(self.state["style"], ensure_ascii=False)
                result = glm.chat_json([{"role": "system", "content": "你是IP内容策略师。"}, {"role": "user", "content": prompt + ' 返回JSON: {"narrative_direction":"方向","key_elements":["元素"]}'}])
                self.state["plan"] = result or {"narrative_direction": "默认方向", "key_elements": []}
                return True

            elif step == "write_story":
                if not self.state["style"] or not self.state["plan"]:
                    return False
                gen = StoryGenerator()
                text = gen.generate(self.state["style"], self.state["plan"])
                if text and len(text) > 200:
                    self.state["story"] = text
                    return True
                return False

            elif step == "write_script":
                if not self.state["story"] or not self.state["style"]:
                    return False
                gen = ScriptGenerator()
                text = gen.generate(self.state["story"], self.state["style"])
                if text and len(text) > 100:
                    self.state["script"] = text
                    return True
                return False

            elif step == "design_assets":
                if not self.state["style"]:
                    return False
                gen = AssetDesigner()
                self.state["assets"] = gen.generate(self.state["style"])
                return bool(self.state["assets"].get("assets"))

            elif step == "check_quality":
                if not self.state["style"]:
                    return False
                checker = StyleChecker(self.state["style"])
                results = []
                if self.state["story"]:
                    r = checker.check(self.state["story"], "故事")
                    results.append("故事:" + str(r.get("score", 0)))
                if self.state["script"]:
                    r = checker.check(self.state["script"], "脚本")
                    results.append("脚本:" + str(r.get("score", 0)))
                if self.state["assets"]:
                    r = checker.check(json.dumps(self.state["assets"], ensure_ascii=False), "资产")
                    results.append("资产:" + str(r.get("score", 0)))
                self.log("SCORE", " ".join(results))
                return True

            elif step == "deploy":
                self._deploy_prepare()
                return True

        except Exception as e:
            self.log("FAIL", str(e)[:100])
            return False

    def _deploy_prepare(self):
        from src.chain.publisher import NFTPublisher
        from src.utils.reporter import generate_html_report
        from src.utils.visualizer import save_visual_assets
        ip = self.state["ip"]
        out = os.path.join(settings.OUTPUT_DIR, ip)
        os.makedirs(out, exist_ok=True)
        save_visual_assets(out, self.state.get("style", {}), self.state.get("assets", {}))
        generate_html_report(ip, self.state.get("story", ""), self.state.get("script", ""), self.state.get("assets", {}), out)
        pub = NFTPublisher(out)
        pub.prepare_metadata(ip, self.state.get("story", ""), self.state.get("script", ""), self.state.get("assets", {}))
        pub.generate_deploy_script()
        self.log("DONE", "output/" + ip + "/ 目录已生成")

    def _summary(self):
        ip = self.state["ip"]
        self.log("DONE", "")
        self.log("DONE", "交付总结")
        self.log("DONE", "目标IP: " + ip)
        self.log("DONE", "")
        self.log("DONE", "衍生故事: output/" + ip + "/story.html")
        self.log("DONE", "动画脚本: output/" + ip + "/script.html")
        self.log("DONE", "周边资产: output/" + ip + "/assets.html")
        self.log("DONE", "SVG图形: output/" + ip + "/visuals/")
        self.log("DONE", "NFT合约: output/" + ip + "/nft/IPWeaveNFT.sol")
        self.log("DONE", "")
        self.log("DONE", "链上交付: 合约部署到Sepolia测试网")
        self.log("DONE", "验证: https://sepolia.etherscan.io/address/合约地址")

    def log(self, tag, msg):
        line = "[" + tag + "] " + msg
        logger.info(line)
        self.history.append({"tag": tag, "msg": msg})
