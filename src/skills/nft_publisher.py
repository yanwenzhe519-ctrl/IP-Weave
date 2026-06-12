from src.chain.publisher import NFTPublisher
import os

def deploy_nft(output_dir, ip_name, story_text, script_text, assets):
    """准备 NFT 并返回部署信息"""
    publisher = NFTPublisher(output_dir)
    meta = publisher.prepare_metadata(ip_name, story_text, script_text, assets)
    publisher.generate_deploy_script()
    return {"status": "ready", "metadata": meta}
