import os, json, time, base64, httpx
from loguru import logger

API_KEY = "GMH0WpwoRpTu77tRfnhNp434Ypqc9SWL"
SUBMIT_URL = "https://tokenhub.tencentmaas.com/v1/api/3d/submit"
QUERY_URL = "https://tokenhub.tencentmaas.com/v1/api/3d/query"

def generate_3d_asset(asset_name="", description="", style="", prompt_override=""):
    """根据资产描述生成3D模型，返回模型URL和metadata"""
    if prompt_override:
        prompt = prompt_override
    else:
        prompt = f"3D model of {asset_name}, {description}, stylized collectible, {style}, game-ready asset, PBR texture, glb format"

    logger.info(f"  提交3D生成任务: {asset_name[:30]}")
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    try:
        resp = httpx.post(SUBMIT_URL, headers=headers,
            json={"model": "hy-3d-3.1", "prompt": prompt, "face_count": 50000, "result_format": "glb"},
            timeout=30)

        if resp.status_code != 200:
            logger.warning(f"  3D提交失败: {resp.status_code}")
            return None

        task_id = resp.json().get("data", {}).get("task_id", "")
        if not task_id:
            logger.warning("  未获取到任务ID")
            return None

        logger.info(f"  任务已提交: {task_id[:16]}...")

        for attempt in range(30):
            time.sleep(10)
            qr = httpx.post(QUERY_URL, headers=headers,
                json={"model": "hy-3d-3.1", "task_id": task_id}, timeout=30)
            if qr.status_code != 200:
                continue

            status = qr.json().get("data", {}).get("status", "")
            if status == "completed":
                model_url = qr.json().get("data", {}).get("model_url", "")
                logger.success(f"  3D模型生成完成")

                # 生成NFT元数据
                meta = {
                    "name": f"IP Weave 3D - {asset_name}",
                    "description": description[:200],
                    "image": model_url,
                    "animation_url": model_url,
                    "attributes": [
                        {"trait_type": "Format", "value": "GLB"},
                        {"trait_type": "Generator", "value": "Hunyuan 3D"},
                        {"trait_type": "Type", "value": "Digital Wearable"}
                    ]
                }
                meta_uri = f"data:application/json;base64,{base64.b64encode(json.dumps(meta, ensure_ascii=False).encode()).decode()}"

                return {"model_url": model_url, "metadata_uri": meta_uri, "metadata": meta}

            elif status == "failed":
                logger.warning("  3D生成失败")
                return None

        logger.warning("  3D生成超时")
    except Exception as e:
        logger.warning(f"  3D错误: {str(e)[:80]}")

    return None
