import json
import importlib
from loguru import logger
from src.utils.llm import glm


class Agent:
    """总指挥：不亲自干活，只负责统筹调度"""

    def __init__(self):
        self.skills = {}  # 注册可用的技能
        self.state = {}   # 当前状态
        self.history = [] # 执行历史

    def register_skill(self, name, module_path, func_name, description):
        """注册一个技能"""
        self.skills[name] = {
            "module": module_path,
            "func": func_name,
            "description": description
        }
        self.log("REGISTER", f"技能 [{name}]: {description}")

    def run(self, ip_name: str = ""):
        """启动指挥循环"""
        self.state["ip"] = ip_name
        self.state["phase"] = "planning"
        self.log("START", f"目标 IP: {ip_name}")
        self.log("PLAN", f"任务拆解: 1.读取数据 2.分析风格 3.生成内容 4.检查质量 5.上链交付")

        max_loops = 10
        for loop in range(max_loops):
            self.log("LOOP", f"指挥循环 {loop+1}/{max_loops}，当前阶段: {self.state.get(phase,)}")

            # GLM-5.1 决定下一步
            decision = self._decide()
            if not decision:
                break

            action = decision.get("action", "")
            skill = decision.get("skill", "")
            params = decision.get("params", {})

            if action == "done":
                self.log("DONE", "所有任务完成")
                break

            if action == "call_skill":
                self._call_skill(skill, params)
            elif action == "evaluate":
                self._evaluate()
            elif action == "wait_user":
                self.log("WAIT", decision.get("reason", "需要用户确认"))
                break
            else:
                self.log("FAIL", f"未知动作: {action}")

    def _decide(self):
        """GLM-5.1 分析当前状态，决定下一步"""
        skills_desc = "\n".join([f"  {k}: {v[description]}" for k, v in self.skills.items()])
        prompt = f"""你是 IP Weave Agent 的总指挥。分析当前状态，决定下一步动作。

当前状态：
{json.dumps(self.state, ensure_ascii=False, indent=2)}

可用技能：
{skills_desc}

返回 JSON（决定下一步做什么）：
{{"action": "call_skill/evaluate/done/wait_user", "skill": "技能名", "params": {{"param1": "value"}}, "reason": "为什么这么决定"}}

规则：
- 还没读链上数据 → 调 ip_reader
- 有数据没分析风格 → 调 style_analyzer
- 有风格没生成内容 → 调 content_creator
- 内容生成了 → evaluate 检查质量
- 质量合格 → 调 nft_publisher 上链
- 全部完成 → done
"""
        result = glm.chat_json([
            {"role": "system", "content": "你是一个冷静的 AI Agent 总指挥。你只负责决策和派活，不亲自干活。"},
            {"role": "user", "content": prompt}
        ])
        if result:
            self.log("DECIDE", f"{result.get(action,)} | {result.get(reason,)}")
        return result

    def _call_skill(self, name, params):
        """调用技能干活"""
        if name not in self.skills:
            self.log("FAIL", f"技能 [{name}] 不存在")
            return

        skill = self.skills[name]
        self.log("CALL", f"调用技能 [{name}]")

        try:
            module = importlib.import_module(skill["module"])
            func = getattr(module, skill["func"])
            result = func(**params)
            self.state[f"{name}_result"] = result
            self.state["phase"] = f"done_{name}"
            self.log("RESULT", f"[{name}] 执行成功")
        except Exception as e:
            self.log("FAIL", f"[{name}] 执行失败: {str(e)[:100]}")
            self.state[f"{name}_error"] = str(e)

    def _evaluate(self):
        """评估当前成果"""
        self.state["phase"] = "evaluating"
        self.log("EVAL", "评估当前成果质量")

    def log(self, tag, msg):
        line = f"[{tag}] {msg}"
        logger.info(line)
        self.history.append(line)
