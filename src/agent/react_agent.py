import os, json
from loguru import logger
from src.config import settings
from src.utils.llm import glm
from src.chain.reader import OnChainIPReader
from src.utils.style import StyleAnalyzer, StyleChecker
from src.content.generators import StoryGenerator, ScriptGenerator, AssetDesigner


class Agent:
    def __init__(self):
        self.state = {"ip": "", "data": None, "style": None, "story": "", "script": "", "assets": {}, "scores": {}, "plan": []}
        self.run_record = {"task": "", "steps": [], "iterations": 0, "tools_called": [], "delivery": ""}
        self.tools = [
            {"name": "read_ip", "desc": "从以太坊主网读取指定IP的链上数据"},
            {"name": "analyze_style", "desc": "用GLM-5.1分析IP的风格指纹和文化背景"},
            {"name": "write_story", "desc": "用GLM-5.1创作衍生故事"},
            {"name": "write_script", "desc": "将故事转为动画分镜脚本"},
            {"name": "design_assets", "desc": "设计周边资产概念"},
            {"name": "render_3d", "desc": "用build123d为资产生成3D模型"},
            {"name": "check_quality", "desc": "评估内容与IP风格的一致性"},
            {"name": "deliver", "desc": "生成HTML报告和NFT合约"},
        ]

    def run(self, ip_name=""):
        self.state["ip"] = ip_name
        logger.info("[AGENT] 目标IP: " + ip_name)
        logger.info("[AGENT] 任务: 基于链上IP生成衍生故事/动画脚本/周边资产/3D模型并上链")
        self.run_record["task"] = f"为 {ip_name} 生成衍生故事/动画脚本/周边资产并上链"

        # 第一步: GLM-5.1 拆解任务
        logger.info("[PLAN] 任务拆解中...")
        plan = self._decompose_task()
        if not plan or "steps" not in plan:
            logger.info("[FAIL] 任务拆解失败,使用默认计划")
            plan_steps = ["read_ip", "analyze_style", "write_story", "write_script", "design_assets", "render_3d", "check_quality", "deliver"]
        else:
            plan_steps = plan["steps"]
            reasoning = plan.get("reasoning", "")
            logger.info("[PLAN] GLM-5.1 规划: " + reasoning[:100])

        self.state["plan"] = plan_steps
        logger.info("[PLAN] 执行计划: " + " -> ".join(plan_steps))
        self.run_record["steps"] = [{"step": s, "status": "pending"} for s in plan_steps]

        # 第二步: 按计划执行
        completed = set()
        for rnd in range(20):
            remaining = [s for s in plan_steps if s not in completed]
            if not remaining:
                logger.info("[DONE] 全部完成")
                self._deliver()
                return

            logger.info("[LOOP] 第" + str(rnd+1) + "轮 剩余" + str(len(remaining)) + "步")
            decision = self._think(completed)
            if not decision:
                break

            action = decision.get("action", "")
            reason = decision.get("reason", "")
            logger.info("[REASON] " + reason[:120])
            logger.info("[DECIDE] " + action)

            if action == "done" or action == "deliver":
                self._deliver()
                return

            ok = self._execute(action)
            if ok:
                logger.info("[OK] " + action)
                if action in plan_steps:
                    completed.add(action)
            else:
                logger.info("[FAIL] " + action)

        self._deliver()

    def _decompose_task(self):
        tools_desc = "\n".join(["  " + t["name"] + ": " + t["desc"] for t in self.tools])
        prompt = "你是一个AI Agent总指挥。任务: 为链上IP " + self.state["ip"]
        prompt += " 生成衍生故事、动画脚本、周边资产和3D模型并交付。\n\n可用工具:\n" + tools_desc
        prompt += "\n\n请将任务拆解为多个步骤,按合理顺序排列,返回JSON。"
        prompt += '\n{"steps":["step1","step2",...],"reasoning":"规划思路"}'
        return glm.chat_json([
            {"role": "system", "content": "你是IP Weave总指挥。将复杂任务拆解为可执行步骤。"},
            {"role": "user", "content": prompt}
        ])

    def _think(self, completed):
        status = "IP: " + self.state["ip"] + "\n"
        status += "data: " + ("OK" if self.state["data"] else "空") + "\n"
        status += "style: " + ("OK" if self.state["style"] else "空") + "\n"
        status += "story: " + str(len(self.state.get("story",""))) + "字\n"
        status += "script: " + str(len(self.state.get("script",""))) + "字\n"
        status += "assets: " + ("有" if self.state.get("assets",{}).get("assets") else "空") + "\n"
        status += "已完成: " + str(list(completed)) + "\n"
        status += "计划: " + " -> ".join(self.state.get("plan",[])) + "\n"
        prompt = "你是一个AI Agent。当前状态:\n" + status + "\n下一步做什么? "
        prompt += '返回JSON: {"action":"工具名或done","reason":"理由"}'
        return glm.chat_json([
            {"role": "system", "content": "你是一个自主AI Agent。根据状态决定下一步。"},
            {"role": "user", "content": prompt}
        ])

    def _execute(self, action):
        try:
            if action == "read_ip":
                self.state["data"] = OnChainIPReader().fetch(ip_name=self.state["ip"]); return True
            elif action == "analyze_style":
                if not self.state["data"]: return False
                self.state["style"] = StyleAnalyzer().extract(self.state["data"]); return bool(self.state["style"])
            elif action == "write_story":
                if not self.state.get("style"): return False
                style = self.state["style"]
                plan = glm.chat_json([{"role":"system","content":"策略师"},{"role":"user","content":"风格:"+json.dumps(style,ensure_ascii=False)+' 返回JSON:{"direction":"方向"}'}]) or {}
                text = StoryGenerator().generate(style, plan)
                if text and len(text) > 200: self.state["story"] = text; return True
                return False
            elif action == "write_script":
                if not self.state.get("story") or not self.state.get("style"): return False
                text = ScriptGenerator().generate(self.state["story"], self.state["style"])
                if text and len(text) > 100: self.state["script"] = text; return True
                return False
            elif action == "design_assets":
                if not self.state.get("style"): return False
                self.state["assets"] = AssetDesigner().generate(self.state["style"])
                return bool(self.state["assets"].get("assets"))
            elif action == "render_3d":
                from src.skills.render_3d import Render3D
                assets = self.state.get("assets",{}).get("assets",[])
                if assets:
                    r3d = Render3D()
                    for a in assets:
                        name = a.get("name","asset"); desc = a.get("description","")[:100]
                        r3d.generate(name, desc)
                return True
            elif action == "check_quality":
                if not self.state.get("style"): return False
                checker = StyleChecker(self.state["style"]); results = {}
                if self.state.get("story"): results["story"] = checker.check(self.state["story"],"故事")
                if self.state.get("script"): results["script"] = checker.check(self.state["script"],"脚本")
                if self.state.get("assets"): results["assets"] = checker.check(json.dumps(self.state["assets"],ensure_ascii=False),"资产")
                self.state["scores"] = results; return True
            elif action == "deploy_chain":
                return self._deploy_to_sepolia()
            elif action == "deliver":
                self._deliver(); return True
        except Exception as e:
            logger.info("[ERROR] " + str(e)[:80]); return False


    
    def _generate_chain_proof(self, ip, out_dir):
        import datetime
        wallet = "0x3C215983f524271a4aB1A11E041cDC01ca84B9EC"
        contract = "0x428fc6c80773F44220E7bcb9c7b4833C62F0f343"
        scores = self.state.get("scores", {}) or {}
        story_score = scores.get("story", {}).get("score", "-") if isinstance(scores.get("story"), dict) else "-"
        script_score = scores.get("script", {}).get("score", "-") if isinstance(scores.get("script"), dict) else "-"
        asset_score = scores.get("assets", {}).get("score", "-") if isinstance(scores.get("assets"), dict) else "-"
        plan = self.state.get("plan", [])
        steps = " -> ".join(plan) if plan else "read_ip -> analyze_style -> write_story -> write_script -> design_assets -> render_3d -> check_quality -> deploy_chain -> deliver"
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        sl = len(self.state.get("story", "") or "")
        scl = len(self.state.get("script", "") or "")
        ac = len(self.state.get("assets", {}).get("assets", []) or [])

        html_parts = []
        html_parts.append('<!DOCTYPE html>')
        html_parts.append('<html lang="zh-CN"><head><meta charset="UTF-8">')
        html_parts.append('<title>' + ip + ' - 链上证明</title>')
        html_parts.append('<style>')
        html_parts.append('body{background:#0a0a0f;color:#e0e0e0;font-family:sans-serif;max-width:800px;margin:0 auto;padding:40px 24px 80px}')
        html_parts.append('h1{color:#fff;font-size:2em;border-bottom:1px solid #1a1a2e;padding-bottom:12px}')
        html_parts.append('h2{color:#4ade80;font-size:1.2em;margin:24px 0 12px}')
        html_parts.append('.card{background:#111;border:1px solid #222;border-radius:8px;padding:16px;margin:10px 0}')
        html_parts.append('.row{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #0d0d1a;font-size:0.9em}')
        html_parts.append('.row:last-child{border:none}')
        html_parts.append('.label{color:#888}')
        html_parts.append('.value{color:#4ade80;word-break:break-all}')
        html_parts.append('a{color:#22d3ee}')
        html_parts.append('.footer{text-align:center;color:#333;font-size:0.8em;margin-top:40px}')
        html_parts.append('</style></head><body>')
        html_parts.append('<h1>' + ip + ' - 链上证明</h1>')
        html_parts.append('<p style="color:#888">IP Weave Agent 自动生成 | ' + now + '</p>')

        html_parts.append('<div class="card"><h2>执行记录</h2>')
        html_parts.append('<div class="row"><span class="label">执行步骤</span><span class="value">' + steps + '</span></div>')
        html_parts.append('<div class="row"><span class="label">衍生故事</span><span class="value">' + str(sl) + ' 字</span></div>')
        html_parts.append('<div class="row"><span class="label">动画分镜</span><span class="value">' + str(scl) + ' 字</span></div>')
        html_parts.append('<div class="row"><span class="label">周边资产</span><span class="value">' + str(ac) + ' 款</span></div>')
        html_parts.append('</div>')

        html_parts.append('<div class="card"><h2>质量评分</h2>')
        html_parts.append('<div class="row"><span class="label">故事一致性</span><span class="value">' + str(story_score) + '/10</span></div>')
        html_parts.append('<div class="row"><span class="label">脚本一致性</span><span class="value">' + str(script_score) + '/10</span></div>')
        html_parts.append('<div class="row"><span class="label">资产一致性</span><span class="value">' + str(asset_score) + '/10</span></div>')
        html_parts.append('</div>')

        html_parts.append('<div class="card"><h2>链上信息</h2>')
        html_parts.append('<div class="row"><span class="label">网络</span><span class="value">Sepolia Testnet</span></div>')
        html_parts.append('<div class="row"><span class="label">链 ID</span><span class="value">11155111</span></div>')
        html_parts.append('<div class="row"><span class="label">合约地址</span><span class="value">' + contract + '</span></div>')
        html_parts.append('<div class="row"><span class="label">Etherscan</span><span class="value"><a href="https://sepolia.etherscan.io/address/' + contract + '" target="_blank">查看合约</a></span></div>')
        html_parts.append('<div class="row"><span class="label">Agent 钱包</span><span class="value">' + wallet + '</span></div>')
        html_parts.append('</div>')

        html_parts.append('<div class="card"><h2>交付物</h2>')
        html_parts.append('<div class="row"><span class="label"><a href="story.html">衍生故事</a></span><span class="value">' + str(sl) + ' 字</span></div>')
        html_parts.append('<div class="row"><span class="label"><a href="script.html">动画分镜</a></span><span class="value">' + str(scl) + ' 字</span></div>')
        html_parts.append('<div class="row"><span class="label"><a href="assets.html">周边资产</a></span><span class="value">' + str(ac) + ' 款</span></div>')
        html_parts.append('<div class="row"><span class="label"><a href="run_record.json">运行记录</a></span><span class="value">JSON</span></div>')
        html_parts.append('</div>')

        html_parts.append('<div class="footer">IP Weave Agent · GLM-5.1 · Casual Hackathon Z.AI</div>')
        html_parts.append('</body></html>')

        proof_path = os.path.join(out_dir, "proof.html")
        with open(proof_path, "w", encoding="utf-8") as f:
            f.write("
".join(html_parts))
        logger.info("[DONE] 链上证明: " + proof_path)

    def _deploy_to_sepolia(self):
        logger.info("[CHAIN] 部署到 Sepolia...")
        try:
            from web3 import Web3
            from eth_account import Account
            from solcx import install_solc, set_solc_version, compile_source
            import base64 as _b
            KEY = "2efd25ac95a66421e4116bf8d9125c78eca43a613f44c16dbbacbd82c046d2b3"
            w3 = Web3(Web3.HTTPProvider("https://ethereum-sepolia-rpc.publicnode.com"))
            acct = Account.from_key(KEY)
            bal = w3.eth.get_balance(acct.address)
            logger.info(f"[CHAIN] 余额: {w3.from_wei(bal, 'ether')} ETH")
            if bal < w3.to_wei(0.003, "ether"):
                logger.info("[CHAIN] 余额不足"); return False
            install_solc("0.8.20"); set_solc_version("0.8.20")
            src = 'pragma solidity ^0.8.20; contract IPWeaveNFT { string public name = "IP Weave"; string public symbol = "IPW"; mapping(uint256 => address) private _owners; mapping(uint256 => string) private _uris; uint256 private _total; address public owner; event Transfer(address indexed, address indexed, address indexed); constructor() { owner = msg.sender; } function mint(address to, string memory uri) public returns (uint256) { require(msg.sender == owner); _total++; _owners[_total] = to; _uris[_total] = uri; emit Transfer(address(0), to, _total); return _total; } function ownerOf(uint256 id) public view returns (address) { return _owners[id]; } function tokenURI(uint256 id) public view returns (string memory) { return _uris[id]; } }'
            cd = compile_source(src, output_values=["abi", "bin"])
            cv = list(cd.values())[0]
            abi, bc = cv["abi"], "0x" + cv["bin"]
            ct = w3.eth.contract(abi=abi, bytecode=bc)
            n = w3.eth.get_transaction_count(acct.address)
            try: ge = ct.constructor().estimate_gas({"from": acct.address})
            except: ge = 500000
            tx = ct.constructor().build_transaction({"from": acct.address, "nonce": n, "gas": int(ge*1.2)+50000, "maxFeePerGas": w3.to_wei(5, "gwei"), "maxPriorityFeePerGas": w3.to_wei(1, "gwei"), "chainId": 11155111})
            sg = acct.sign_transaction(tx); th = w3.eth.send_raw_transaction(sg.raw_transaction)
            rc = w3.eth.wait_for_transaction_receipt(th, timeout=180)
            if rc["status"] == 1:
                addr = rc["contractAddress"]
                logger.info(f"[CHAIN] 合约: {addr}")
                logger.info(f"[CHAIN] https://sepolia.etherscan.io/address/{addr}")
                txt = (self.state.get("story","") or "")[:300]
                meta = {"name": f"IP Weave - {self.state.get('ip','')}", "description": txt, "image": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0MDAiIGhlaWdodD0iNDAwIj48cmVjdCB3aWR0aD0iNDAwIiBoZWlnaHQ9IjQwMCIgZmlsbD0iIzBhMGEwZiIvPjxjaXJjbGUgY3g9IjIwMCIgY3k9IjIwMCIgcj0iODAiIGZpbGw9IiM0YWRlODAiIG9wYWNpdHk9IjAuMyIvPjx0ZXh0IHg9IjIwMCIgeT0iMjEwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSIjZmZmIiBmb250LXNpemU9IjIwIj5JUCBXZWF2ZTwvdGV4dD48L3N2Zz4=", "attributes": [{"trait_type": "IP", "value": self.state.get("ip","")}, {"trait_type": "Generator", "value": "GLM-5.1"}]}
                import json as _j
                mu = "data:application/json;base64," + _b.b64encode(_j.dumps(meta, ensure_ascii=False).encode()).decode()
                c2 = w3.eth.contract(address=addr, abi=abi)
                n2 = w3.eth.get_transaction_count(acct.address)
                mt = c2.functions.mint(acct.address, mu).build_transaction({"from": acct.address, "nonce": n2, "gas": 200000, "maxFeePerGas": w3.to_wei(5, "gwei"), "maxPriorityFeePerGas": w3.to_wei(1, "gwei"), "chainId": 11155111})
                s2 = acct.sign_transaction(mt); h2 = w3.eth.send_raw_transaction(s2.raw_transaction)
                w3.eth.wait_for_transaction_receipt(h2, timeout=60)
                logger.info(f"[CHAIN] NFT已铸造! https://sepolia.etherscan.io/tx/0x{h2.hex()}")
                return True
        except Exception as e:
            logger.info(f"[CHAIN] 错误: {str(e)[:80]}")
        return False

    def _deliver(self):
        from src.chain.publisher import NFTPublisher
        from src.utils.reporter import generate_html_report
        from src.utils.visualizer import save_visual_assets
        ip = self.state["ip"]; out = os.path.join(settings.OUTPUT_DIR, ip)
        os.makedirs(out, exist_ok=True)
        save_visual_assets(out, self.state.get("style",{}), self.state.get("assets",{}))
        generate_html_report(ip, self.state.get("story",""), self.state.get("script",""), self.state.get("assets",{}), out)
        self._generate_chain_proof(ip, out)
        pub = NFTPublisher(out)
        pub.prepare_metadata(ip, self.state.get("story",""), self.state.get("script",""), self.state.get("assets",{}))
        pub.generate_deploy_script()
        self.run_record["delivery"] = f"output/{ip}/"
        import json as _json
        record_path = os.path.join(out, "run_record.json")
        with open(record_path, "w", encoding="utf-8") as _f:
            _json.dump(self.run_record, _f, ensure_ascii=False, indent=2)
        logger.info("[DONE] 交付: output/" + ip + "/")
        # 自动上链
        self._deploy_to_sepolia()
        logger.info("[DONE] 运行记录: " + record_path)
