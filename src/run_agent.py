import sys
import os
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
    print("  输入任意链上 IP")
    print("  例如: pepe, bayc, punk, azuki")
    print("  或者任意 ERC-721 合约地址")
    print()

    target = input("链上 IP 名称或合约地址: ").strip()

    if not target:
        print("请输入一个链上 IP 名称或合约地址")
        return

    if not settings.is_configured:
        print("请在 .env 中配置 ZHIPUAI_API_KEY")
        return

    print("测试 GLM-5.1 连接...")
    result = glm.chat([{"role": "user", "content": "连接成功"}])
    if not result:
        print("GLM-5.1 连接失败")
        return
    print("OK")
    print()

    agent = ReActAgent()
    if target.startswith("0x"):
        agent.run(contract=target)
    else:
        agent.run(ip_name=target)

    print()
    print("========================================")
    print("  完成")
    print("========================================")


if __name__ == "__main__":
    main()
