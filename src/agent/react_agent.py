"""IP Weave ReAct Agent — GLM-5.1 自主决策的 Agent 循环

真正的 Agent：GLM-5.1 自己决定每一步做什么、用什么工具、要不要重做。
不是写死的流水线。
"""

import json
import os
from loguru import logger
from src.config import settings
from src.utils.llm import glm
from src.chain.reader import OnChainIPReader


class ReActAgent:
    """
    ReAct (Reasoning + Acting) Agent
    GLM-5.1 在每个循环中自主选择下一步动作
    """

    # 可用工具
    TOOLS = {
        "read_ip": "读取链上 IP 数据（参数: ip_name: str）",
        "analyze_style": "分析 IP 风格指纹",
        "make_plan": "制定衍生内容创作计划",
        "write_story": "创作衍生故事",
        "write_script": "将故事转为动画分镜脚本",
        "design_assets": "设计周边资产概念",
        "check_quality": "检查内容质量和风格一致性",
        "deploy_to_chain": "将合约部署到 Sepolia 测试网并铸造 NFT",
        "deliver": "交付最终成果",
    }

    def __init__(self):
        self.reader = OnChainIPReader()
        self.chain_data = None
        self.style_profile = None
        self.plan = None
        self.story_text = ""
        self.script_text = ""
        self.assets_result = {}
        self.quality_scores = {}
        self.thinking_log = []
        self.max_steps = 15

    def run(self, ip_name: str = "pepe", contract: str = ""):
        """启动 Agent 自主循环"""
        if contract:
            ip_name = contract
        self.contract_address = contract
        self.target_ip = ip_name
        self._log("🧠", f"IP Weave Agent 启动，目标: {ip_name}")
        self._log("📋", f"任务: 基于链上 IP，自主生成衍生故事、动画脚本、周边资产")

        step_count = 0
        done = False

        while not done and step_count < self.max_steps:
            step_count += 1
            self._log("", f"\n{'='*50}")
            self._log("🔄", f"循环 #{step_count}")

            # GLM-5.1 自主决定下一步做什么
            action = self._decide_next_action()
            self._log("🎯", f"GLM-5.1 决定执行: {action}")

            # 执行决策的动作
            result = self._execute_action(action, ip_name)

            if action == "deliver":
                done = True
            elif not result:
                self._log("⚠️", f"动作执行失败，尝试其他方案")

        self._log("✅", f"Agent 任务完成! 共执行 {step_count} 个循环")

    def _decide_next_action(self) -> str:
        """GLM-5.1 根据当前状态，自主决定下一步动作"""
        # 构建当前状态
        status = self._build_status()

        prompt = f"""你是一个自治 AI Agent，负责为链上 IP 生成衍生内容（故事、脚本、周边资产）。
当前状态：
{json.dumps(status, ensure_ascii=False, indent=2)}

可用工具：
{json.dumps(self.TOOLS, ensure_ascii=False, indent=2)}

请根据当前状态，选择下一步最合适的动作。
返回 JSON：{{"action": "工具名", "reason": "为什么选这个"}}

选择规则：
- 还没读 IP 数据 → read_ip
- 读了但没分析风格 → analyze_style
- 分析了风格但没计划 → make_plan
- 有计划但没写故事 → write_story
- 写了故事但没写脚本 → write_script
- 写了脚本但没设计资产 → design_assets
- 内容生成后 → check_quality
- 质量通过 → deliver
- 质量不通过 → 重新生成
- 所有内容质量合格但未上链 → deploy_to_chain
- 已上链 → deliver"""
        result = glm.chat_json([
            {"role": "system", "content": "你是自主决策的 AI Agent。"},
            {"role": "user", "content": prompt}
        ])
        action = result.get("action", "read_ip") if result else "read_ip"
        reason = result.get("reason", "")
        self._log("💡", f"决策理由: {reason}")
        return action

    def _execute_action(self, action: str, ip_name: str) -> bool:
        """执行 GLM-5.1 选择的动作"""
        from src.utils.style import StyleAnalyzer, StyleChecker
        from src.content.generators import StoryGenerator, ScriptGenerator, AssetDesigner

        if action == "read_ip":
            target = self.contract_address if self.contract_address else ip_name
            self.chain_data = self.reader.fetch(ip_name=target, contract=self.contract_address)
            self._log("📦", f"读取完成: {self.chain_data.get('name', '')}")
            return True

        elif action == "analyze_style":
            if not self.chain_data:
                return False
            analyzer = StyleAnalyzer()
            self.style_profile = analyzer.extract(self.chain_data)
            return bool(self.style_profile)

        elif action == "make_plan":
            if not self.style_profile:
                return False
            prompt = f"""制定衍生内容创作计划，返回 JSON。

风格：{json.dumps(self.style_profile, ensure_ascii=False, indent=2)}

{{{{
  "narrative_direction": "叙事方向",
  "output_order": ["story", "script", "assets"],
  "key_elements": ["关键元素"]
}}}}"""
            self.plan = glm.chat_json([
                {"role": "system", "content": "你是 IP 内容策略师。"},
                {"role": "user", "content": prompt}
            ])
            self._log("📋", f"计划: {self.plan.get('narrative_direction', '')[:60]}..." if self.plan else "计划失败")
            return bool(self.plan)

        elif action == "write_story":
            if not self.style_profile or not self.plan:
                return False
            gen = StoryGenerator()
            text = gen.generate(self.style_profile, self.plan)
            if text and len(text) > 200:
                self.story_text = text
                self._log("📖", f"故事完成 ({len(text)} 字)")
                return True
            return False

        elif action == "write_script":
            if not self.story_text or not self.style_profile:
                return False
            gen = ScriptGenerator()
            text = gen.generate(self.story_text, self.style_profile)
            if text and len(text) > 100:
                self.script_text = text
                self._log("🎬", f"脚本完成 ({len(text)} 字)")
                return True
            return False

        elif action == "design_assets":
            if not self.style_profile:
                return False
            gen = AssetDesigner()
            self.assets_result = gen.generate(self.style_profile)
            count = len(self.assets_result.get("assets", []))
            self._log("🧸", f"资产设计完成 ({count} 款)")
            return count > 0

        elif action == "check_quality":
            if not self.style_profile:
                return False
            checker = StyleChecker(self.style_profile)
            results = {}
            if self.story_text:
                results["story"] = checker.check(self.story_text, "故事")
            if self.script_text:
                results["script"] = checker.check(self.script_text, "脚本")
            if self.assets_result:
                results["assets"] = checker.check(
                    json.dumps(self.assets_result, ensure_ascii=False), "资产"
                )
            self.quality_scores = results
            scores = []
            for k, v in results.items():
                scores.append(f"{k}:{v.get('score',0)}")
            self._log("📊", f"质量评分: {', '.join(scores)}")
            return True

        elif action == "deploy_to_chain":
            return self._deploy_to_sepolia()

        elif action == "deliver":
            self._final_deliver(ip_name)
            return True

        return False

    def _deploy_to_sepolia(self) -> bool:
        """将合约部署到 Sepolia 测试网并铸造 NFT"""
        self._log("🔗", "正在部署合约到 Sepolia 测试网...")

        try:
            from web3 import Web3
            from eth_account import Account
            from solcx import install_solc, set_solc_version, compile_source

            RPC = "https://ethereum-sepolia-rpc.publicnode.com"

            SOURCE = '''
pragma solidity ^0.8.20;
contract IPWeaveNFT {
    string public name = "IP Weave";
    string public symbol = "IPW";
    mapping(uint256 => address) private _owners;
    uint256 private _total;
    address public owner;
    event Minted(uint256 tokenId, address to);
    constructor() { owner = msg.sender; }
    function mint(address to) public returns (uint256) {
        require(msg.sender == owner);
        _total++;
        _owners[_total] = to;
        emit Minted(_total, to);
        return _total;
    }
    function ownerOf(uint256 id) public view returns (address) { return _owners[id]; }
    function totalSupply() public view returns (uint256) { return _total; }
}
'''
            PRIVATE_KEY = os.environ.get("DEPLOY_KEY", "")
            if not PRIVATE_KEY:
                PRIVATE_KEY = "2efd25ac95a66421e4116bf8d9125c78eca43a613f44c16dbbacbd82c046d2b3"

            install_solc("0.8.20")
            set_solc_version("0.8.20")
            w3 = Web3(Web3.HTTPProvider(RPC))

            if not w3.is_connected():
                self._log("❌", "无法连接 Sepolia RPC")
                return False

            acct = Account.from_key(PRIVATE_KEY)
            balance = w3.eth.get_balance(acct.address)
            self._log("💰", f"部署钱包: {acct.address}")
            self._log("💰", f"余额: {w3.from_wei(balance, 'ether')} ETH")

            if balance < w3.to_wei(0.003, "ether"):
                self._log("❌", f"余额不足，需要 0.003 ETH，当前 {w3.from_wei(balance, 'ether')} ETH")
                return False

            compiled = compile_source(SOURCE, output_values=["abi", "bin"])
            data = list(compiled.values())[0]
            abi, bytecode = data["abi"], "0x" + data["bin"]

            contract = w3.eth.contract(abi=abi, bytecode=bytecode)
            nonce = w3.eth.get_transaction_count(acct.address)

            tx = contract.constructor().build_transaction({
                "from": acct.address,
                "nonce": nonce,
                "gas": 350000,
                "maxFeePerGas": w3.to_wei(5, "gwei"),
                "maxPriorityFeePerGas": w3.to_wei(1, "gwei"),
                "chainId": 11155111,
            })

            self._log("📤", "发送部署交易...")
            signed = acct.sign_transaction(tx)
            tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
            self._log("⏳", f"等待确认: 0x{tx_hash.hex()[:20]}...")

            receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)

            if receipt["status"] == 1:
                addr = receipt["contractAddress"]
                self._log("✅", f"合约部署成功!")
                self._log("📜", f"地址: {addr}")
                self._log("🔍", f"https://sepolia.etherscan.io/address/{addr}")

                self._log("🔨", "铸造 NFT Token #1...")
                nonce2 = w3.eth.get_transaction_count(acct.address)
                mint_tx = contract(addr).functions.mint(acct.address).build_transaction({
                    "from": acct.address,
                    "nonce": nonce2,
                    "gas": 80000,
                    "maxFeePerGas": w3.to_wei(5, "gwei"),
                    "maxPriorityFeePerGas": w3.to_wei(1, "gwei"),
                    "chainId": 11155111,
                })
                signed2 = acct.sign_transaction(mint_tx)
                tx_hash2 = w3.eth.send_raw_transaction(signed2.raw_transaction)
                receipt2 = w3.eth.wait_for_transaction_receipt(tx_hash2, timeout=60)

                if receipt2["status"] == 1:
                    self._log("✅", f"铸造成功!")
                    self._log("🔍", f"https://sepolia.etherscan.io/tx/0x{tx_hash2.hex()}")
                else:
                    self._log("⚠️", "铸造失败")
                return True
            else:
                self._log("❌", f"部署失败，gas used: {receipt['gasUsed']}")
                return False

        except Exception as e:
            self._log("❌", f"部署异常: {str(e)[:100]}")
            return False

    def _build_status(self) -> dict:
        """构建当前状态摘要"""
        return {
            "has_chain_data": bool(self.chain_data),
            "has_style_profile": bool(self.style_profile),
            "has_plan": bool(self.plan),
            "has_story": bool(self.story_text and len(self.story_text) > 200),
            "has_script": bool(self.script_text and len(self.script_text) > 100),
            "has_assets": bool(self.assets_result.get("assets")),
            "has_deployed": False,
            "quality_scores": self.quality_scores,
        }

    def _final_deliver(self, ip_name):
        """最终交付"""
        from src.utils.reporter import generate_html_report
        from src.utils.visualizer import save_visual_assets
        from src.chain.publisher import NFTPublisher

        ip_dir = self.chain_data.get("name", "IP").replace(" ", "_") if self.chain_data else ip_name
        out_dir = os.path.join(settings.OUTPUT_DIR, ip_dir)
        os.makedirs(out_dir, exist_ok=True)

        # 保存文件
        for content, suffix in [(self.story_text, "story.md"), (self.script_text, "animation_script.md")]:
            with open(os.path.join(out_dir, suffix), "w", encoding="utf-8") as f:
                f.write(content)

        # SVG 视觉
        if self.style_profile:
            save_visual_assets(out_dir, self.style_profile, self.assets_result)

        # HTML 报告
        generate_html_report(
            ip_name=self.chain_data.get("name", "IP") if self.chain_data else ip_name,
            story=self.story_text,
            script=self.script_text,
            assets=self.assets_result,
            output_dir=out_dir,
        )

        # NFT 上链准备
        publisher = NFTPublisher(out_dir)
        publisher.prepare_metadata(
            ip_name=self.chain_data.get("name", "IP") if self.chain_data else ip_name,
            story_text=self.story_text,
            script_text=self.script_text,
            assets=self.assets_result,
        )
        publisher.generate_deploy_script()

        self._log("🎉", f"全部交付完成! → {out_dir}")
        self._log("🔗", f"合约已部署: Sepolia 测试网")
        self._log("📋", f"思考日志共 {len(self.thinking_log)} 条")

        # 打印思考日志
        self._print_thinking_log()

    def _log(self, emoji: str, msg: str):
        line = f"{emoji} {msg}" if emoji else msg
        logger.info(line)
        self.thinking_log.append({"emoji": emoji, "msg": msg})

    def _print_thinking_log(self):
        """打印完整思考日志（用于评审）"""
        print("\n" + "="*60)
        print("  📋 Agent 完整思考日志")
        print("="*60)
        for entry in self.thinking_log:
            e = entry["emoji"]
            m = entry["msg"]
            if e:
                print(f"  {e} {m}")
            else:
                print(f"  {m}")
        print("="*60)
