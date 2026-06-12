
from src.content.generators import AssetDesigner
gen = AssetDesigner()

def design_assets(style_profile=None):
    return {"assets": gen.generate(style_profile)}
