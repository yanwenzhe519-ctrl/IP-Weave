from src.utils.llm import glm
from src.utils.style import StyleAnalyzer
from src.content.generators import StoryGenerator, ScriptGenerator, AssetDesigner
import json

analyzer = StyleAnalyzer()
story_gen = StoryGenerator()
script_gen = ScriptGenerator()
asset_gen = AssetDesigner()

def analyze_style(chain_data):
    """分析 IP 风格"""
    return analyzer.extract(chain_data)

def create_story(style_profile, plan):
    """创作衍生故事"""
    return story_gen.generate(style_profile, plan)

def create_script(story, style_profile):
    """生成动画脚本"""
    return script_gen.generate(story, style_profile)

def create_assets(style_profile):
    """设计周边资产"""
    return asset_gen.generate(style_profile)
