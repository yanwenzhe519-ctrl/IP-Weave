import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import settings
from src.utils.llm import glm
from src.agent.react_agent import Agent


def main():
    print()
    print("========================================")
    print("  IP Weave")
    print("========================================")
    print()
    print("  输入任意链上 IP 名称或合约地址")
    print()

    target = input("链上 IP: ").strip()
    if not target:
        print("请输入一个链上 IP")
        return

    if not settings.is_configured:
        print("请在 .env 中配置 ZHIPUAI_API_KEY")
        return

    print("连接 GLM-5.1...")
    r = glm.chat([{"role": "user", "content": "ok"}])
    if not r:
        print("GLM-5.1 连接失败")
        return
    print("OK")
    print()

    # 创建 Agent 总指挥
    agent = Agent()
    
    # 注册技能
    agent.register_skill("ip_reader",
        "src.skills.ip_reader", "read_ip_data",
        "从以太坊主网读取指定 IP 的链上数据（名称、属性、元数据）")

    agent.register_skill("style_analyzer",
        "src.skills.content_creator", "analyze_style",
        "用 GLM-5.1 分析 IP 的风格指纹、视觉特征、叙事基调")

    agent.register_skill("content_creator",
        "src.skills.content_creator", "create_story",
        "用 GLM-5.1 创作衍生故事（2000-4000字完整叙事）")

    agent.register_skill("script_creator",
        "src.skills.content_creator", "create_script",
        "将故事转为动画分镜脚本（6-8个分镜，含镜头、对白、时长）")

    agent.register_skill("asset_designer",
        "src.skills.content_creator", "create_assets",
        "设计周边资产概念（2款，含设计描述和NFT元数据）")

    agent.register_skill("nft_publisher",
        "src.skills.nft_publisher", "deploy_nft",
        "打包 NFT 元数据，生成 Solidity 合约，准备部署到 Sepolia 测试网")

    # 启动
    if target.startswith("0x"):
        agent.run(contract=target)
    else:
        agent.run(ip_name=target)


if __name__ == "__main__":
    main()
