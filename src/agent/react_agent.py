import json
import os
from loguru import logger
from src.config import settings
from src.utils.llm import glm


class ReActAgent:
    """真正的自主 Agent：GLM-5.1 自己决定做什么、怎么做、用什么工具"""

    def __init__(self):
        self.logs = []
        self.chain_data = None
        self.results = {}

    def run(self, ip_name: str = "", contract: str = ""):
        self.contract = contract
        self.ip_name = ip_name
        target = contract if contract else ip_name
        self.log("AGENT", f"目标: {target}")
        self.log("AGENT", f"任务: 基于链上 IP 生成衍生故事、动画脚本、周边资产并上链")

        # 让 GLM-5.1 自主规划和执行
        prompt = f"""你是一个全能的 AI Agent，可以执行任何 Python 代码来完成用户的任务。

用户任务：基于链上 IP "{target}"，生成衍生故事、动画脚本、周边资产，并部署上链。

你可以使用以下工具：
1. 读取链上数据
2. 分析 IP 风格
3. 调用 GLM-5.1 生成文本
4. 生成图片
5. 部署合约到 Sepolia
6. 创建和写入文件

请按以下格式思考和执行：
THOUGHT: 分析当前状态和下一步做什么
ACTION: python代码
OBSERVATION: 执行结果

每次只执行一个动作，完成后告诉我结果，然后决定下一步。

首先，读取链上 IP "{target}" 的数据。"""

        messages = [
            {"role": "system", "content": "你是一个自主 AI Agent。你可以执行 Python 代码来完成复杂任务。每次只做一件事，做完告诉我结果，然后继续下一步。"},
            {"role": "user", "content": prompt}
        ]

        max_rounds = 20
        for r in range(max_rounds):
            self.log("STEP", f"轮次 {r+1}/{max_rounds}")
            resp = glm.chat(messages, max_tokens=4096, temperature=0.3)
            if not resp:
                self.log("FAIL", "GLM-5.1 无响应")
                break
            self.log("THINK", resp[:200])
            messages.append({"role": "assistant", "content": resp})

            # 检查是否完成
            if "DONE" in resp or "完成" in resp:
                self.log("DONE", "Agent 自主完成")
                break

            # 如果有 PYTHON 代码块则执行
            import re
            code_blocks = re.findall(r"```python\n(.*?)```", resp, re.DOTALL)
            for code in code_blocks:
                try:
                    exec(code, globals())
                    self.log("EXEC", "代码执行成功")
                except Exception as e:
                    self.log("EXEC", f"执行错误: {str(e)[:100]}")
                    messages.append({"role": "user", "content": f"执行出错: {str(e)[:200]}"})
            
            # 如果有 SHELL 代码块则执行
            shell_blocks = re.findall(r"```(?:bash|shell)\n(.*?)```", resp, re.DOTALL)
            import subprocess
            for code in shell_blocks:
                try:
                    result = subprocess.run(code, shell=True, capture_output=True, text=True, timeout=30)
                    self.log("SHELL", result.stdout[:200] if result.stdout else result.stderr[:200])
                except Exception as e:
                    self.log("SHELL", f"失败: {str(e)[:100]}")

    def log(self, tag, msg):
        line = f"[{tag}] {msg}"
        logger.info(line)
        self.logs.append(line)
