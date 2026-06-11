"""IP Weave 全局配置"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    ZHIPUAI_API_KEY: str = os.getenv("ZHIPUAI_API_KEY", "")
    ZHIPUAI_BASE_URL: str = os.getenv(
        "ZHIPUAI_BASE_URL",
        "https://api.z.ai/api/coding/paas/v4"
    )
    MAX_ITERATIONS: int = int(os.getenv("MAX_ITERATIONS", "3"))
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "./output")

    LLM_MODEL: str = "glm-5.1"
    IMAGE_MODEL: str = "cogview-3"

    @property
    def is_configured(self) -> bool:
        return bool(self.ZHIPUAI_API_KEY)


settings = Settings()
