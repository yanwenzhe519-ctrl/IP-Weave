
from src.content.generators import StoryGenerator
gen = StoryGenerator()

def write_story(style_profile=None, plan=None):
    return {"story": gen.generate(style_profile, plan)}
