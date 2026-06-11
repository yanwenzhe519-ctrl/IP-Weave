"""链上 IP 数据读取 — 从链上实时读取任意 ERC-721"""

import json
from loguru import logger
from web3 import Web3

# 免费公开 RPC（主网用于读取，Sepolia 用于部署）
MAINNET_RPC = "https://ethereum-rpc.publicnode.com"

# ERC-721 ABI（只读方法）
ERC721_ABI = json.loads('[{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]')

# 知名 IP 的合约地址（用于名称查找）
KNOWN_IPS = {
    "pepe": "0x6982508145454Ce325dDbE47a25d4ec3d2311933",
    "bayc": "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D",
    "punk": "0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB",
    "azuki": "0xED5AF388653567Af2F388E6224dC7C4b3241C544",
}


class OnChainIPReader:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(MAINNET_RPC))
        if not self.w3.is_connected():
            logger.warning("无法连接主网 RPC，使用降级数据")

    def fetch(self, ip_name: str = "", contract: str = "", token_id: int = 1) -> dict:
        """从链上读取任意 IP 数据"""
        # 如果是名字，先查合约地址
        name_lower = ip_name.lower() if ip_name else ""
        if name_lower in KNOWN_IPS:
            contract = KNOWN_IPS[name_lower]
            logger.info(f"已知 IP: {ip_name} → {contract}")
        elif ip_name and not contract:
            # 未知名称，用 GLM-5.1 尝试解析
            logger.info(f"尝试解析 IP 名称: {ip_name}")
            try:
                from src.utils.llm import glm
                result = glm.chat_json([{"role": "user",
                    "content": f"以下哪个是以太坊上 '{ip_name}' NFT 项目的合约地址？只返回 JSON: {{\"contract\":\"0x...\"}}。如果你不知道，返回 {{\"contract\":\"\"}}。仅返回 JSON，不要其他内容。"}])
                if result and result.get("contract", "").startswith("0x"):
                    contract = result["contract"]
                    logger.info(f"解析到合约: {contract}")
            except Exception:
                pass

        if not contract:
            logger.warning("未提供合约地址，使用模拟数据")
            return self._mock(ip_name or "unknown")

        # 从链上读取
        logger.info(f"读取链上 IP: {contract} #{token_id}")
        try:
            return self._read_erc721(contract, token_id)
        except Exception as e:
            logger.warning(f"链上读取失败: {e}，使用降级数据")
            return self._mock(contract[:10], contract)

    def _read_erc721(self, contract_addr: str, token_id: int) -> dict:
        """读取真正的 ERC-721 链上数据"""
        c = self.w3.eth.contract(
            address=self.w3.to_checksum_address(contract_addr),
            abi=ERC721_ABI
        )

        name = c.functions.name().call()
        symbol = c.functions.symbol().call()
        uri = c.functions.tokenURI(token_id).call()

        # 解析 tokenURI
        metadata = self._resolve_uri(uri) if uri else {}

        # 构建属性列表
        attributes = []
        attrs = metadata.get("attributes", metadata.get("properties", []))
        if isinstance(attrs, list):
            for attr in attrs[:8]:
                if isinstance(attr, dict):
                    attributes.append({
                        "trait_type": attr.get("trait_type", attr.get("key", "属性")),
                        "value": attr.get("value", str(attr))
                    })

        return {
            "contract": contract_addr,
            "token_id": token_id,
            "name": name,
            "symbol": symbol,
            "source": "on-chain",
            "token_uri": uri,
            "metadata": {
                "name": metadata.get("name", f"{name} #{token_id}"),
                "description": metadata.get("description", ""),
                "image": metadata.get("image", ""),
                "attributes": attributes,
            }
        }

    def _resolve_uri(self, uri: str) -> dict:
        """解析 tokenURI"""
        if uri.startswith("ipfs://"):
            uri = uri.replace("ipfs://", "https://ipfs.io/ipfs/")
        try:
            import httpx
            resp = httpx.get(uri, timeout=10)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass
        return {}

    def _mock(self, name: str, contract: str = "") -> dict:
        """降级数据"""
        return {
            "contract": contract or "0xunknown",
            "token_id": 1,
            "name": name,
            "symbol": name[:4].upper(),
            "source": "fallback",
            "metadata": {
                "name": name,
                "description": f"链上 IP: {name}",
                "attributes": [
                    {"trait_type": "来源", "value": "Ethereum"},
                    {"trait_type": "状态", "value": "链上数据读取中"},
                ]
            }
        }
