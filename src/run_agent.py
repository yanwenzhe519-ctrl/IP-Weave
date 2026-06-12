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
    agent.register_skill("ip_reader", "src.skills.ip_reader", "read_ip", "读取链上IP数据", "ip_name: IP名称")
    agent.register_skill("style_analyzer", "src.skills.style_analyzer", "analyze_style", "分析IP风格", "chain_data: 链上数据")
    agent.register_skill("story_writer", "src.skills.story_writer", "write_story", "创作衍生故事", "style_profile: 风格画像, plan: 计划")
    agent.register_skill("script_writer", "src.skills.script_writer", "write_script", "生成动画分镜", "story: 故事文本, style_profile: 风格")
    agent.register_skill("asset_designer", "src.skills.asset_designer", "design_assets", "设计周边资产", "style_profile: 风格")
    agent.register_skill("quality_checker", "src.skills.quality_checker", "check_quality", "检查风格一致性", "style_profile,story,script,assets")
    agent.run(ip_name=target)

if __name__ == "__main__":
    main()
