import os
import json
import logging
logger = logging.getLogger(__name__)


class NFTPublisher:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.nft_dir = os.path.join(output_dir, "nft")
        os.makedirs(self.nft_dir, exist_ok=True)

    def prepare_metadata(self, ip_name, story_text, script_text, assets):
        logger.info("打包 NFT 元数据")
        metadata = {
            "name": f"IP Weave - {ip_name}",
            "description": f"IP Weave Agent 基于 {ip_name} 链上 IP 自主生成的衍生内容 NFT",
            "image": "ipfs://QmPlaceholder/image.png",
            "attributes": [
                {"trait_type": "IP", "value": ip_name},
                {"trait_type": "生成引擎", "value": "GLM-5.1"},
                {"trait_type": "内容", "value": "衍生故事 + 动画脚本 + 周边资产"}
            ]
        }
        path = os.path.join(self.nft_dir, "metadata.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        return metadata

    def generate_deploy_script(self):
        logger.info("生成部署合约")
        code = '''contract IPWeaveNFT {
    string public name = "IP Weave";
    string public symbol = "IPW";
    mapping(uint256 => address) private _owners;
    uint256 private _total;
    address public owner;

    constructor() { owner = msg.sender; }

    function mint(address to) public returns (uint256) {
        require(msg.sender == owner);
        _total++;
        _owners[_total] = to;
        return _total;
    }

    function ownerOf(uint256 id) public view returns (address) {
        return _owners[id];
    }

    function totalSupply() public view returns (uint256) {
        return _total;
    }
}'''
        path = os.path.join(self.nft_dir, "IPWeaveNFT.sol")
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)

        guide = """部署步骤:
1. 安装 Foundry: curl -L https://foundry.paradigm.xyz | bash
2. forge install OpenZeppelin/openzeppelin-contracts
3. forge script Deploy.s.sol --rpc-url $RPC_URL --private-key $KEY --broadcast
"""
        guide_path = os.path.join(self.nft_dir, "DEPLOY_README.md")
        with open(guide_path, "w") as f:
            f.write(guide)
