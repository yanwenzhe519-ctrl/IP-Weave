import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import settings
from src.utils.llm import glm
from src.agent.react_agent import Agent

def main():
    print("========================================")
    print("  IP Weave")
    print("========================================")
    target = input("链上 IP: ").strip()
    if not target:
        print("请输入一个链上 IP")
        return
    if not settings.is_configured:
        print("请在 .env 中配置 ZHIPUAI_API_KEY")
        return
    r = glm.chat([{"role":"user","content":"ok"}])
    if not r:
        print("GLM-5.1 连接失败")
        return
    agent = Agent()
    agent.run(ip_name=target)
    print("完成")

if __name__ == "__main__":
    main()
