
from src.utils.style import StyleAnalyzer
analyzer = StyleAnalyzer()

def analyze_style(chain_data=None):
    return {"style_profile": analyzer.extract(chain_data)}
