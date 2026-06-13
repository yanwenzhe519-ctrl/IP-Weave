import os, json
from loguru import logger
from src.config import settings
from src.utils.llm import glm
from src.chain.reader import OnChainIPReader
from src.utils.style import StyleAnalyzer, StyleChecker
from src.content.generators import StoryGenerator, ScriptGenerator, AssetDesigner


class Agent:
    def __init__(self):
        self.state = {"ip": "", "data": None, "style": None, "story": "", "script": "", "assets": {}, "scores": {}, "plan": []}
        self.run_record = {"task": "", "steps": [], "iterations": 0, "tools_called": [], "delivery": ""}
        self.tools = [
            {"name": "read_ip", "desc": "从以太坊主网读取指定IP的链上数据"},
            {"name": "analyze_style", "desc": "用GLM-5.1分析IP的风格指纹和文化背景"},
            {"name": "write_story", "desc": "用GLM-5.1创作衍生故事"},
            {"name": "write_script", "desc": "将故事转为动画分镜脚本"},
            {"name": "design_assets", "desc": "设计周边资产概念"},
            {"name": "render_3d", "desc": "用build123d为资产生成3D模型"},
            {"name": "check_quality", "desc": "评估内容与IP风格的一致性"},
            {"name": "deliver", "desc": "生成HTML报告和NFT合约"},
        ]

    def run(self, ip_name=""):
        self.state["ip"] = ip_name
        logger.info("[AGENT] 目标IP: " + ip_name)
        logger.info("[AGENT] 任务: 基于链上IP生成衍生故事/动画脚本/周边资产/3D模型并上链")
        self.run_record["task"] = f"为 {ip_name} 生成衍生故事/动画脚本/周边资产并上链"

        # 第一步: GLM-5.1 拆解任务
        logger.info("[PLAN] 任务拆解中...")
        plan = self._decompose_task()
        if not plan or "steps" not in plan:
            logger.info("[FAIL] 任务拆解失败,使用默认计划")
            plan_steps = ["read_ip", "analyze_style", "write_story", "write_script", "design_assets", "render_3d", "check_quality", "deliver"]
        else:
            plan_steps = plan["steps"]
            reasoning = plan.get("reasoning", "")
            logger.info("[PLAN] GLM-5.1 规划: " + reasoning[:100])

        self.state["plan"] = plan_steps
        logger.info("[PLAN] 执行计划: " + " -> ".join(plan_steps))
        self.run_record["steps"] = [{"step": s, "status": "pending"} for s in plan_steps]

        # 第二步: 按计划执行
        completed = set()
        for rnd in range(20):
            remaining = [s for s in plan_steps if s not in completed]
            if not remaining:
                logger.info("[DONE] 全部完成")
                self._deliver()
                return

            logger.info("[LOOP] 第" + str(rnd+1) + "轮 剩余" + str(len(remaining)) + "步")
            decision = self._think(completed)
            if not decision:
                break

            action = decision.get("action", "")
            reason = decision.get("reason", "")
            logger.info("[REASON] " + reason[:120])
            logger.info("[DECIDE] " + action)

            if action == "done" or action == "deliver":
                self._deliver()
                return

            ok = self._execute(action)
            if ok:
                logger.info("[OK] " + action)
                if action in plan_steps:
                    completed.add(action)
            else:
                logger.info("[FAIL] " + action)

        self._deliver()

    def _decompose_task(self):
        tools_desc = "\n".join(["  " + t["name"] + ": " + t["desc"] for t in self.tools])
        prompt = "你是一个AI Agent总指挥。任务: 为链上IP " + self.state["ip"]
        prompt += " 生成衍生故事、动画脚本、周边资产和3D模型并交付。\n\n可用工具:\n" + tools_desc
        prompt += "\n\n请将任务拆解为多个步骤,按合理顺序排列,返回JSON。"
        prompt += '\n{"steps":["step1","step2",...],"reasoning":"规划思路"}'
        return glm.chat_json([
            {"role": "system", "content": "你是IP Weave总指挥。将复杂任务拆解为可执行步骤。"},
            {"role": "user", "content": prompt}
        ])

    def _think(self, completed):
        status = "IP: " + self.state["ip"] + "\n"
        status += "data: " + ("OK" if self.state["data"] else "空") + "\n"
        status += "style: " + ("OK" if self.state["style"] else "空") + "\n"
        status += "story: " + str(len(self.state.get("story",""))) + "字\n"
        status += "script: " + str(len(self.state.get("script",""))) + "字\n"
        status += "assets: " + ("有" if self.state.get("assets",{}).get("assets") else "空") + "\n"
        status += "已完成: " + str(list(completed)) + "\n"
        status += "计划: " + " -> ".join(self.state.get("plan",[])) + "\n"
        prompt = "你是一个AI Agent。当前状态:\n" + status + "\n下一步做什么? "
        prompt += '返回JSON: {"action":"工具名或done","reason":"理由"}'
        return glm.chat_json([
            {"role": "system", "content": "你是一个自主AI Agent。根据状态决定下一步。"},
            {"role": "user", "content": prompt}
        ])

    def _execute(self, action):
        try:
            if action == "read_ip":
                self.state["data"] = OnChainIPReader().fetch(ip_name=self.state["ip"]); return True
            elif action == "analyze_style":
                if not self.state["data"]: return False
                self.state["style"] = StyleAnalyzer().extract(self.state["data"]); return bool(self.state["style"])
            elif action == "write_story":
                if not self.state.get("style"): return False
                style = self.state["style"]
                plan = glm.chat_json([{"role":"system","content":"策略师"},{"role":"user","content":"风格:"+json.dumps(style,ensure_ascii=False)+' 返回JSON:{"direction":"方向"}'}]) or {}
                text = StoryGenerator().generate(style, plan)
                if text and len(text) > 200: self.state["story"] = text; return True
                return False
            elif action == "write_script":
                if not self.state.get("story") or not self.state.get("style"): return False
                text = ScriptGenerator().generate(self.state["story"], self.state["style"])
                if text and len(text) > 100: self.state["script"] = text; return True
                return False
            elif action == "design_assets":
                if not self.state.get("style"): return False
                self.state["assets"] = AssetDesigner().generate(self.state["style"])
                return bool(self.state["assets"].get("assets"))
            elif action == "render_3d":
                from src.skills.render_3d import Render3D
                assets = self.state.get("assets",{}).get("assets",[])
                if assets:
                    r3d = Render3D()
                    for a in assets:
                        name = a.get("name","asset"); desc = a.get("description","")[:100]
                        r3d.generate(name, desc)
                return True
            elif action == "check_quality":
                if not self.state.get("style"): return False
                checker = StyleChecker(self.state["style"]); results = {}
                if self.state.get("story"): results["story"] = checker.check(self.state["story"],"故事")
                if self.state.get("script"): results["script"] = checker.check(self.state["script"],"脚本")
                if self.state.get("assets"): results["assets"] = checker.check(json.dumps(self.state["assets"],ensure_ascii=False),"资产")
                self.state["scores"] = results; return True
            elif action == "deliver":
                self._deliver(); return True
        except Exception as e:
            logger.info("[ERROR] " + str(e)[:80]); return False

    def _deliver(self):
        from src.chain.publisher import NFTPublisher
        from src.utils.reporter import generate_html_report
        from src.utils.visualizer import save_visual_assets
        ip = self.state["ip"]; out = os.path.join(settings.OUTPUT_DIR, ip)
        os.makedirs(out, exist_ok=True)
        save_visual_assets(out, self.state.get("style",{}), self.state.get("assets",{}))
        generate_html_report(ip, self.state.get("story",""), self.state.get("script",""), self.state.get("assets",{}), out)
        pub = NFTPublisher(out)
        pub.prepare_metadata(ip, self.state.get("story",""), self.state.get("script",""), self.state.get("assets",{}))
        pub.generate_deploy_script()
        self.run_record["delivery"] = f"output/{ip}/"
        import json as _json
        record_path = os.path.join(out, "run_record.json")
        with open(record_path, "w", encoding="utf-8") as _f:
            _json.dump(self.run_record, _f, ensure_ascii=False, indent=2)
        logger.info("[DONE] 交付: output/" + ip + "/")
        logger.info("[DONE] 运行记录: " + record_path)
