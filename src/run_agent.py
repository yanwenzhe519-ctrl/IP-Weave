#!/usr/bin/env python3
"""
IP Weave — ReAct Agent 入口
GLM-5.1 自主决策的 Agent 循环

用法：
    python src/run_agent.py                    # Pepe
    python src/run_agent.py --ip bayc          # BAYC
    python src/run_agent.py --ip pepe          # Pepe
"""

import sys
import argparse
from loguru import logger


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="pepe", help="IP 名称: pepe/bayc/punk/azuki")
    args = parser.parse_args()

    from src.config import settings
    if not settings.is_configured:
        print("❌ 请在 .env 中配置 ZHIPUAI_API_KEY")
        sys.exit(1)

    # 测试 GLM-5.1
    from src.utils.llm import glm
    print("🧪 测试 GLM-5.1 连接...")
    result = glm.chat([{"role": "user", "content": "回复'连接成功'四个字"}])
    if not result:
        print("❌ GLM-5.1 连接失败")
        sys.exit(1)
    print(f"✅ {result[:50]}")
    print()

    # 启动 ReAct Agent
    logger.remove()
    logger.add(sys.stdout, format="<level>{message}</level>", level="INFO")
    from src.agent.react_agent import ReActAgent

    print("=" * 60)
    print("  🧬 IP Weave — ReAct Agent")
    print("  GLM-5.1 自主决策 · 多步骤规划 · 迭代修复")
    print("=" * 60)
    print()
    print(f"  目标 IP: {args.ip}")
    print(f"  任务: 基于链上 IP 自主生成衍生故事、动画脚本、周边资产")
    print()

    agent = ReActAgent()
    agent.run(ip_name=args.ip)


if __name__ == "__main__":
    main()
