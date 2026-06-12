import httpx, json, base64, time
from loguru import logger

API_KEY = "GMH0WpwoRpTu77tRfnhNp434Ypqc9SWL"
SUBMIT_URL = "https://tokenhub.tencentmaas.com/v1/api/3d/submit"
QUERY_URL = "https://tokenhub.tencentmaas.com/v1/api/3d/query"

def generate_3d(prompt, model="hy-3d-3.1", face_count=50000):
    headers = {"Authorization": "Bearer " + API_KEY, "Content-Type": "application/json"}
    data = {"model": model, "prompt": prompt, "face_count": face_count, "result_format": "glb"}
    logger.info("  提交3D生成任务...")
    resp = httpx.post(SUBMIT_URL, headers=headers, json=data, timeout=30)
    if resp.status_code != 200:
        logger.warning("  3D提交失败")
        return None
    task_id = resp.json().get("data", {}).get("task_id", "")
    if not task_id:
        return None
    logger.info("  任务ID: " + task_id)
    for i in range(30):
        time.sleep(10)
        qr = httpx.post(QUERY_URL, headers=headers, json={"model": model, "task_id": task_id}, timeout=30)
        if qr.status_code != 200: continue
        s = qr.json().get("data", {}).get("status", "")
        if s == "completed":
            url = qr.json().get("data", {}).get("model_url", "")
            logger.success("  3D模型生成完成: " + url)
            return url
        elif s == "failed":
            logger.warning("  3D生成失败")
            return None
    logger.warning("  超时")
    return None

def upload_3d_to_ipfs(model_url, asset_name):
    if not model_url: return None
    resp = httpx.get(model_url, timeout=120)
    if resp.status_code != 200: return None
    meta = {"name": asset_name, "description": "IP Weave 3D Asset - " + asset_name,
        "image": model_url, "animation_url": model_url,
        "attributes": [{"trait_type": "Format", "value": "GLB"}, {"trait_type": "Generator", "value": "Hunyuan 3D"}]}
    return {"model_url": model_url, "metadata": meta,
        "metadata_uri": "data:application/json;base64," + base64.b64encode(json.dumps(meta, ensure_ascii=False).encode()).decode()}
