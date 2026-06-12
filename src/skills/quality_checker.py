
from src.utils.style import StyleChecker
import json

def check_quality(style_profile=None, story="", script="", assets=None):
    checker = StyleChecker(style_profile)
    results = {}
    if story:
        results["story"] = checker.check(story, "故事")
    if script:
        results["script"] = checker.check(script, "脚本")
    if assets:
        results["assets"] = checker.check(json.dumps(assets), "资产")
    return {"scores": results}
