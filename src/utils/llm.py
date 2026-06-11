"""GLM-5.1 API 调用封装"""

import json
import httpx
from loguru import logger
from src.config import settings


class GLMClient:
    def __init__(self):
        self.api_key = settings.ZHIPUAI_API_KEY
        self.base_url = settings.ZHIPUAI_BASE_URL.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def chat(self, messages: list, max_tokens: int = 4096,
             temperature: float = 0.7) -> str:
        for attempt in range(2):
            try:
                resp = httpx.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json={
                        "model": settings.LLM_MODEL,
                        "messages": messages,
                        "max_tokens": max_tokens,
                        "temperature": temperature,
                    },
                    timeout=300
                )
                if resp.status_code == 200:
                    return resp.json()["choices"][0]["message"].get("content", "")
                logger.error(f"GLM API 错误 [{resp.status_code}]")
                return ""
            except Exception as e:
                logger.warning(f"GLM 调用异常: {str(e)[:80]}")
                if attempt == 0:
                    logger.info("  正在重试...")
        return ""

    def chat_json(self, messages: list, max_tokens: int = 4096) -> dict:
        content = self.chat(messages, max_tokens)
        if not content:
            return {}
        content = content.strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[-1]
            content = content.rsplit("```", 1)[0]
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            import re
            match = re.search(r'\{.*\}', content, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except json.JSONDecodeError:
                    pass
            logger.warning("GLM 返回非合法 JSON")
            return {}

    def generate_image(self, prompt: str) -> str | None:
        try:
            resp = httpx.post(
                f"{self.base_url}/images/generations",
                headers=self.headers,
                json={"model": settings.IMAGE_MODEL, "prompt": prompt},
                timeout=120
            )
            if resp.status_code == 200:
                return resp.json()["data"][0]["url"]
            logger.warning(f"CogView 需额外充值 ({resp.status_code})")
            return None
        except Exception as e:
            logger.warning(f"图片生成异常: {str(e)[:60]}")
            return None


glm = GLMClient()
