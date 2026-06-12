import os
import json
import importlib
from loguru import logger
from src.config import settings
from src.utils.llm import glm


class Agent:
    def __init__(self):
        self.state = {"ip": "", "data": {}, "results": {}}
        self.skills = {}
        self.history = []

    def register_skill(self, name, module, func, desc, params_desc=""):
        self.skills[name] = {"module": module, "func": func, "desc": desc, "params": params_desc}
        self.log("SKILL", "注册技能: " + name + " - " + desc)

    def run(self, ip_name=""):
        self.state["ip"] = ip_name
        self.log("START", "目标: " + ip_name + " 生成衍生故事/动画脚本/周边资产")

        for rnd in range(20):
            self.log("LOOP", "思考循环 " + str(rnd+1))

            # GLM-5.1 思考下一步
            thought = self._think()
            if not thought:
                break

            action = thought.get("action", "")
            skill = thought.get("skill", "")
            reason = thought.get("reason", "")
            params = thought.get("params", {})

            self.log("THINK", "分析: " + reason[:100])
            self.log("DECIDE", "决策: " + action + (" -> 技能:" + skill if skill else ""))

            if action == "done":
                self.log("DONE", "任务完成")
                break

            if action == "call_skill" and skill in self.skills:
                self._call_skill(skill, params)
            elif action == "evaluate":
                self._evaluate()
            else:
                self.log("FAIL", "未知决策: " + action)

    def _think(self):
        desc = "\n".join([f"  [{k}] {v['desc']}" for k, v in self.skills.items()])
        params = "\n".join([f"  [{k}] 参数: {v['params']}" for k, v in self.skills.items()])
        status = "\n".join([f"  {k}: {v}" for k, v in self.state.items() if k != "results"])
        if self.state.get("results"):
            status += "\n  已完成: " + str(list(self.state["results"].keys()))

        prompt = "你是IP Weave Agent总指挥。你的任务是: 基于链上IP " + self.state["ip"]
        prompt += " 生成衍生故事、动画脚本和周边资产。\n\n"
        prompt += "当前状态:\n" + status + "\n\n"
        prompt += "可用技能:\n" + desc + "\n\n"
        prompt += "技能参数:\n" + params + "\n\n"
        prompt += "返回JSON: {\"action\": \"call_skill/evaluate/done\", \"skill\": \"技能名\", \"params\": {}, \"reason\": \"为什么这么决策\"}\n\n"
        prompt += "决策规则：\n"
        prompt += "- 先读取IP数据，再分析风格，然后创作内容，最后检查质量\n"
        prompt += "- 如果某技能调用失败，尝试其他方案或重试\n"
        prompt += "- 所有内容生成完毕后执行evaluate\n"
        prompt += "- evaluate通过后执行done"
        return glm.chat_json([
            {"role": "system", "content": "你是IP Weave Agent总指挥。你擅长分析状态、制定策略、调用合适的技能完成任务。你的决策基于当前实际情况，不是固定流程。"},
            {"role": "user", "content": prompt}
        ])

    def _call_skill(self, name, params):
        s = self.skills[name]
        self.log("EXEC", "调用技能: " + name)
        try:
            mod = importlib.import_module(s["module"])
            func = getattr(mod, s["func"])
            result = func(**params)
            self.state["results"][name] = "ok"
            if hasattr(result, 'get'):
                self.state["data"].update(result)
            self.log("OK", name + " 成功")
        except Exception as e:
            self.log("FAIL", name + " 失败: " + str(e)[:100])

    def _evaluate(self):
        scores = self.state.get("data", {}).get("scores", {})
        if scores:
            all_pass = all(s.get("passed", False) for s in scores.values() if isinstance(s, dict))
            self.log("EVAL", "质量评估: " + ("通过" if all_pass else "需改进"))
        else:
            self.log("EVAL", "暂无评分数据")

    def log(self, tag, msg):
        logger.info("[" + tag + "] " + msg)
        self.history.append({"tag": tag, "msg": msg})
