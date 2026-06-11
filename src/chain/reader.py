"""链上 IP 数据读取 — 支持任意链上 IP"""

from loguru import logger


# 内置预设 IP 数据集（方便无 RPC 时 Demo）
PRESET_IPS = {
    "pepe": {
        "contract": "0x6982508145454Ce325dDbE47a25d4ec3d2311933",
        "name": "Pepe the Frog",
        "symbol": "PEPE",
        "description": "Matt Furie 创作的经典青蛙角色。绿色皮肤、突出的大眼睛、标志性的半圆嘴巴。互联网 Meme 文化的图腾级 IP，从 4chan 走向世界的文化符号。",
        "attributes": [
            {"trait_type": "世界观", "value": "互联网 Meme 宇宙 · Boy's Club"},
            {"trait_type": "角色类型", "value": "拟人化青蛙"},
            {"trait_type": "特征", "value": "绿色皮肤 · 突出大眼睛 · 半圆嘴"},
            {"trait_type": "色调", "value": "蛙绿 #4ade80 + 忧郁紫"},
            {"trait_type": "阵营", "value": "混沌善良"},
            {"trait_type": "创作者", "value": "Matt Furie"},
        ]
    },
    "bayc": {
        "contract": "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D",
        "name": "Bored Ape Yacht Club",
        "symbol": "BAYC",
        "description": "以太坊上最知名的 NFT 系列之一。一只无聊的猿，游艇俱乐部的会员。",
        "attributes": [
            {"trait_type": "世界观", "value": "Web3 贵族 · Yacht Club"},
            {"trait_type": "色调", "value": "复古撞色"},
            {"trait_type": "阵营", "value": "金钱自由"},
            {"trait_type": "标志特征", "value": "无聊表情 · 金链子 · 游艇"},
        ]
    },
    "punk": {
        "contract": "0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB",
        "name": "CryptoPunks",
        "symbol": "PUNK",
        "description": "NFT 的始祖。24x24 像素的朋克头像，加密艺术的起源。",
        "attributes": [
            {"trait_type": "世界观", "value": "加密朋克 · 赛博街头"},
            {"trait_type": "色调", "value": "复古 8-bit 像素"},
            {"trait_type": "阵营", "value": "密码朋克"},
            {"trait_type": "标志特征", "value": "像素头像 · 朋克精神 · 数字身份"},
        ]
    },
    "azuki": {
        "contract": "0xED5AF388653567Af2F388E6224dC7C4b3241C544",
        "name": "Azuki",
        "symbol": "AZUKI",
        "description": "一个由 10,000 个像素风格动漫角色组成的 NFT 系列。日式街头风格，Web3 动漫文化。",
        "attributes": [
            {"trait_type": "世界观", "value": "日式街头 · 动漫次元"},
            {"trait_type": "色调", "value": "柔和粉蓝 + 红白"},
            {"trait_type": "阵营", "value": "艺术追求"},
            {"trait_type": "标志特征", "value": "日式画风 · 发色 · 街头服饰"},
        ]
    },
}


class OnChainIPReader:
    """读取任意链上 IP 数据"""

    def __init__(self):
        self.presets = PRESET_IPS

    def fetch(self, ip_name: str = "", contract: str = "", token_id: int = 1) -> dict:
        """
        读取 IP 数据
        优先级: 合约地址 > 预设名称 > 默认
        """
        if contract:
            logger.info(f"读取链上 IP: {contract} #{token_id}")
            # 这里可以接入 web3.py 读真实 ERC-721
            # 目前先用通用数据
            return self._generic_onchain(contract, token_id)

        if ip_name and ip_name in self.presets:
            logger.info(f"使用预设 IP: {ip_name}")
            return self._preset(ip_name)

        logger.info("使用默认 IP 数据")
        return self._preset("pepe")

    def _preset(self, name: str) -> dict:
        data = self.presets[name]
        return {
            "contract": data["contract"],
            "token_id": 1,
            "name": data["name"],
            "symbol": data["symbol"],
            "source": "preset",
            "metadata": {
                "name": data["name"],
                "description": data["description"],
                "attributes": data["attributes"],
            }
        }

    def _generic_onchain(self, contract: str, token_id: int) -> dict:
        """通用链上数据（可用于任意 ERC-721）"""
        return {
            "contract": contract,
            "token_id": token_id,
            "name": f"OnChain IP #{token_id}",
            "symbol": "NFT",
            "source": "onchain",
            "metadata": {
                "name": f"链上 IP #{token_id}",
                "description": f"以太坊上的数字藏品，合约 {contract[:10]}...",
                "attributes": [
                    {"trait_type": "来源", "value": "Ethereum"},
                    {"trait_type": "类型", "value": "ERC-721"},
                    {"trait_type": "合约", "value": f"{contract[:10]}..."},
                ]
            }
        }
