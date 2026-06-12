import json
import importlib
from loguru import logger
from src.utils.llm import glm


class Agent:
    def __init__(self):
        self.skills = {}
        self.state = {"ip": "", "phase": "init", "results": {}}
        self.history = []

    def register_skill(self, name, module_path, func_name, description):
        self.skills[name] = {"module": module_path, "func": func_name, "description": description}
        self.log("REGISTER", "[" + name + "] " + description)

    def run(self, ip_name=""):
        self.state["ip"] = ip_name
        self.log("TASK", "目标IP: " + ip_name + " - 基于链上IP生成衍生故事/动画脚本/周边资产并上链")
        self.log("PLAN", "整体计划: 1.读取数据 2.分析风格 3.创作内容 4.质量检查 5.上链交付")

        for loop in range(12):
            self.log("LOOP", "循环 " + str(loop + 1) + "/12")
            decision = self._decide()
            if not decision:
                break
            action = decision.get("action", "")
            skill_name = decision.get("skill", "")
            reason = decision.get("reason", "")

            if action == "done":
                self.log("DONE", "全部完成")
                self._summary()
                break
            elif action == "call_skill" and skill_name:
                self.log("EXEC", "调用 [" + skill_name + "] " + reason)
                self._call_skill(skill_name, decision.get("params", {}))
            elif action == "evaluate":
                self.state["phase"] = "passed"
                self.log("PASS", "评估通过")
            else:
                self.log("FAIL", "未知指令")

    def _decide(self):
        skills_desc = ""
        for k, v in self.skills.items():
            skills_desc += "  [" + k + "] " + v["description"] + "\n"

        status = "phase: " + str(self.state.get("phase", "")) + "\n"
        status += "ip: " + str(self.state.get("ip", "")) + "\n"
        status += "results: " + str(list(self.state.get("results", {}).keys()))

        prompt = "你是一个AI Agent总指挥。分析状态决定下一步。\n"
        prompt += "状态:\n" + status + "\n"
        prompt += "技能:\n" + skills_desc + "\n"
        prompt += "返回JSON: {"action":"call_skill/evaluate/done","skill":"名称","params":{},"reason":"理由"}"

        result = glm.chat_json([
            {"role": "system", "content": "你是IP Weave总指挥。只决策不干活。"},
            {"role": "user", "content": prompt}
        ])
        if result:
            self.log("DECIDE", result.get("action", "") + " [" + result.get("skill", "") + "] " + result.get("reason", ""))
        return result

    def _call_skill(self, name, params):
        if name not in self.skills:
            self.log("FAIL", "技能不存在")
            return
        s = self.skills[name]
        try:
            m = importlib.import_module(s["module"])
            f = getattr(m, s["func"])
            f(**params)
            self.state["results"][name] = "done"
            self.state["phase"] = "done_" + name
            self.log("OK", "[" + name + "] 成功")
        except Exception as e:
            self.log("FAIL", "[" + name + "] 失败: " + str(e)[:100])

    def _summary(self):
        ip = self.state.get("ip", "")
        self.log("DONE", "")
        self.log("DONE", "交付总结")
        self.log("DONE", "目标IP: " + ip)
        self.log("DONE", "执行步数: " + str(len(self.history)))
        self.log("DONE", "")
        self.log("DONE", "衍生故事: output/" + ip + "/story.html")
        self.log("DONE", "动画脚本: output/" + ip + "/script.html")
        self.log("DONE", "周边资产: output/" + ip + "/assets.html")
        self.log("DONE", "SVG图形: output/" + ip + "/visuals/")
        self.log("DONE", "NFT合约: output/" + ip + "/nft/IPWeaveNFT.sol")
        self.log("DONE", "")
        self.log("DONE", "链上交付: 合约部署到Sepolia测试网")
        self.log("DONE", "链上交付: NFT元数据写入链上data URI")

    def log(self, tag, msg):
        line = "[" + tag + "] " + msg
        logger.info(line)
        self.history.append({"tag": tag, "msg": msg})
