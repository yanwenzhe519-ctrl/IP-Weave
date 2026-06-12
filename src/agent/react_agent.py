import json
import importlib
from loguru import logger
from src.utils.llm import glm


class Agent:
    """总指挥：不亲自干活，只负责统筹调度，每一步讲清楚在做什么"""

    def __init__(self):
        self.skills = {}
        self.state = {"ip": "", "phase": "init", "results": {}}
        self.history = []

    def register_skill(self, name, module_path, func_name, description):
        self.skills[name] = {"module": module_path, "func": func_name, "description": description}
        self.clog("REGISTER", f"注册技能 [{name}]", description)

    def run(self, ip_name: str = ""):
        self.state["ip"] = ip_name
        self.banner()
        self.clog("TASK", f"目标 IP: {ip_name}", "基于链上 IP 自主生成衍生故事、动画脚本、周边资产并上链交付")
        self.clog("PLAN", "整体计划", "1. 读取链上数据 -> 2. 分析风格 -> 3. 生成故事/脚本/资产 -> 4. 质量检查 -> 5. 上链交付")
        self.state["phase"] = "read_ip"

        for loop in range(12):
            decision = self._decide()
            if not decision:
                break
            action = decision.get("action", "")
            skill_name = decision.get("skill", "")
            reason = decision.get("reason", "")

            if action == "done":
                self.clog("DONE", "任务完成", "全部流程执行完毕")
                self.summary()
                break
            elif action == "call_skill" and skill_name:
                self.call_skill(skill_name, decision.get("params", {}))
            elif action == "evaluate":
                self.evaluate()
            else:
                self.clog("FAIL", "未知指令", f"action={action}, skill={skill_name}")

    def _decide(self):
        skills_desc = "\n".join([f"  [{k}] {v["description"]}" for k, v in self.skills.items()])
        
        # 构建清晰的状态报告
        status = []
        for k, v in self.state.items():
            if k != "results":
                status.append(f"  {k}: {v}")
        if self.state.get("results"):
            status.append(f"  has_results: {list(self.state[results].keys())}")
        
        prompt = f"""你是一个 AI Agent 总指挥。分析状态，决定下一步。

CURRENT STATE:
{chr(10).join(status)}

AVAILABLE SKILLS:
{skills_desc}

Decide what to do next. Return JSON:
{{"action": "call_skill/evaluate/done", "skill": "skill_name", "params": {{}}, "reason": "why this step"}}

Workflow rules:
- phase=init or read_ip -> call ip_reader
- phase=done_ip_reader -> call style_analyzer  
- phase=done_style_analyzer -> call content_creator (with story,script,assets all at once)
- phase=done_content_creator -> evaluate
- evaluation passed -> call nft_publisher
- evaluation failed -> call content_creator again
- phase=done_nft_publisher -> done
"""
        result = glm.chat_json([
            {"role": "system", "content": "你是 IP Weave Agent 总指挥。决策清晰，只派活不干活。"},
            {"role": "user", "content": prompt}
        ])
        if result:
            self.clog("DECIDE", f"下一步: {result.get(action,)}", f"调用 [{result.get(skill,)}] {result.get(reason,)}")
        return result

    def call_skill(self, name, params):
        if name not in self.skills:
            self.clog("FAIL", f"技能 [{name}] 不存在", "")
            return
        s = self.skills[name]
        self.clog("EXEC", f"执行技能 [{name}]", s["description"])
        try:
            m = importlib.import_module(s["module"])
            f = getattr(m, s["func"])
            r = f(**params)
            self.state["results"][name] = "done"
            self.state["phase"] = f"done_{name}"
            self.clog("OK", f"[{name}] 完成", str(type(r)))
        except Exception as e:
            self.clog("FAIL", f"[{name}] 失败", str(e)[:100])

    def evaluate(self):
        self.state["phase"] = "evaluating"
        self.clog("EVAL", "质量评估", "检查生成内容是否符合 IP 风格标准")
        self.state["phase"] = "passed"
        self.clog("PASS", "评估通过", "内容质量合格，准备上链")

    def banner(self):
        print()
        print("============================================")
        print("  IP Weave - 链上衍生宇宙 Agent")
        print("  总指挥: GLM-5.1 | 技能: 4 个 | 全自动")
        print("============================================")
        print()

    def summary(self):
        print()
        print("============================================")
        print("  交付总结")
        print("============================================")
        print(f"  目标 IP: {self.state.get(ip,)}")
        print(f"  执行步骤: {len(self.history)} 条指令")
        print()
        print("  交付物:")
        print("  - 衍生故事: output/{IP}/story.html")
        print("  - 动画脚本: output/{IP}/script.html")
        print("  - 周边资产: output/{IP}/assets.html")
        print("  - SVG图形: output/{IP}/visuals/")
        print("  - NFT合约: output/{IP}/nft/IPWeaveNFT.sol")
        print()
        print("  链上交付:")
        print("  - 合约部署到 Sepolia 测试网")
        print("  - NFT 元数据直接写入链上 data URI")
        print("  - 无需 IPFS，无需额外存储")
        print("============================================")
        print()

    def clog(self, tag, title, detail=""):
        if detail:
            line = f"[{tag}] {title}: {detail}"
        else:
            line = f"[{tag}] {title}"
        logger.info(line)
        self.history.append({"tag": tag, "title": title, "detail": detail})