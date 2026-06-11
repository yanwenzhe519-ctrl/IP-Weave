import sys
import os
from loguru import logger
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import settings
from src.utils.llm import glm
from src.agent.react_agent import ReActAgent


def main():
    print()
    print("========================================")
    print("  IP Weave - 链上衍生宇宙")
    print("  基于 GLM-5.1 的自治创作 Agent")
    print("========================================")
    print()

    target = input("输入链上 IP 合约地址（回车使用 Pepe）: ").strip()

    if not settings.is_configured:
        print("请在 .env 中配置 ZHIPUAI_API_KEY")
        return

    print("测试 GLM-5.1 连接...")
    result = glm.chat([{"role": "user", "content": "连接成功"}])
    if not result:
        print("GLM-5.1 连接失败")
        return
    print(f"OK")
    print()

    agent = ReActAgent()
    agent.run(contract=target)

    print()
    print("========================================")
    print("  完成！成果在 output/ 目录下")
    print("========================================")


if __name__ == "__main__":
    main()
