import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import settings
from src.utils.llm import glm
from src.agent.react_agent import ReActAgent


def main():
    print()
    print('========================================')
    print('  IP Weave')
    print('  基于 GLM-5.1 的链上 IP 衍生内容 Agent')
    print('========================================')
    print()
    print('  输入任意链上 IP')
    print('  名称或合约地址均可')
    print()

    target = input('链上 IP: ').strip()

    if not target:
        print('请输入一个链上 IP')
        return

    if not settings.is_configured:
        print('请在 .env 中配置 ZHIPUAI_API_KEY')
        return

    print('测试 GLM-5.1 连接...')
    result = glm.chat([{'role': 'user', 'content': 'ok'}])
    if not result:
        print('GLM-5.1 连接失败')
        return
    print('OK')
    print()

    agent = ReActAgent()
    if target.startswith('0x'):
        agent.run(contract=target)
    else:
        agent.run(ip_name=target)


if __name__ == '__main__':
    main()
