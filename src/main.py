#!/usr/bin/env python3
"""
IP Weave — 链上衍生宇宙
基于 GLM-5.1 的自治 IP 衍生内容 Agent

用法：
    python src/main.py                              ← 使用默认模拟 IP
    python src/main.py --ip pepe                    ← PEPE
    python src/main.py --ip bayc --token 1234       ← BAYC #1234
    python src/main.py --contract 0x... --token 1   ← 任意 ERC-721
"""

import sys
import argparse
from loguru import logger


def main():
    parser = argparse.ArgumentParser(description="IP Weave — 链上衍生宇宙 Agent")
    parser.add_argument("--ip", type=str, default="",
                        help="预设 IP 名称: pepe, bayc, punk, azuki 等")
    parser.add_argument("--contract", type=str, default="",
                        help="ERC-721 合约地址")
    parser.add_argument("--token", type=int, default=1,
                        help="Token ID (默认: 1)")
    args = parser.parse_args()

    from src.config import settings
    if not settings.is_configured:
        print("❌ 请在 .env 中配置 ZHIPUAI_API_KEY")
        sys.exit(1)

    # 测试 GLM-5.1 连接
    from src.utils.llm import glm
    print("🧪 测试 GLM-5.1 连接...")
    result = glm.chat([{"role": "user", "content": "回复'连接成功'四个字"}])
    if not result:
        print("❌ GLM-5.1 连接失败，请检查 API Key 和网络")
        sys.exit(1)
    print(f"✅ {result[:50]}")
    print()

    # 确定目标 IP
    ip_name = args.ip.lower() if args.ip else ""
    contract = args.contract
    token_id = args.token

    # 运行 Agent
    logger.remove()
    logger.add(sys.stdout, format="<level>{message}</level>", level="INFO")
    from src.agent.core import IPWeaveAgent
    agent = IPWeaveAgent()
    agent.run(ip_name=ip_name, contract=contract, token_id=token_id)


if __name__ == "__main__":
    main()
