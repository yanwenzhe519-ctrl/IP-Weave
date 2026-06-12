
from src.content.generators import ScriptGenerator
gen = ScriptGenerator()

def write_script(story="", style_profile=None):
    return {"script": gen.generate(story, style_profile)}
