#!/usr/bin/env python3
"""IP Weave Web UI — 在浏览器里运行 Agent"""

import os
import sys
import json
import threading
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from src.agent.core import IPWeaveAgent
from src.utils.visualizer import save_visual_assets

HOST = "127.0.0.1"
PORT = 8080
OUTPUT_DIR = os.path.abspath("./output")


class WebUIHandler(BaseHTTPRequestHandler):
    """HTTP 请求处理"""

    def do_GET(self):
        if self.path == "/":
            self._serve_file("src/webui_index.html", "text/html; charset=utf-8")
        elif self.path.startswith("/output/"):
            filepath = self.path[8:]  # 去掉 /output/
            self._serve_file(os.path.join(OUTPUT_DIR, filepath))
        elif self.path == "/api/ips":
            self._json_response({
                "ips": ["pepe", "bayc", "punk", "azuki"],
                "labels": {
                    "pepe": "🐸 Pepe the Frog",
                    "bayc": "🦧 Bored Ape Yacht Club",
                    "punk": "👤 CryptoPunks",
                    "azuki": "🌸 Azuki"
                }
            })
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/api/run":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.read(content_length) if content_length else b"{}"
            data = json.loads(body) if body else {}
            ip_name = data.get("ip", "pepe")

            # 在后台线程运行 Agent
            def run_agent():
                agent = IPWeaveAgent()
                agent.run(ip_name=ip_name)

                # 生成 SVG 视觉资产
                out_dir = os.path.join(OUTPUT_DIR, agent.chain_data.get("name", "IP").replace(" ", "_"))
                save_visual_assets(out_dir, agent.style_profile, agent.results.get("assets_result", {}))

            threading.Thread(target=run_agent, daemon=True).start()
            self._json_response({"status": "started", "ip": ip_name})
        else:
            self.send_error(404)

    def _serve_file(self, path, content_type=None):
        path = os.path.normpath(path)
        if not os.path.exists(path):
            self.send_error(404)
            return
        if content_type is None:
            ext = os.path.splitext(path)[1].lower()
            content_type = {
                ".html": "text/html; charset=utf-8",
                ".svg": "image/svg+xml",
                ".json": "application/json",
                ".md": "text/markdown; charset=utf-8",
                ".png": "image/png",
                ".jpg": "image/jpeg",
            }.get(ext, "application/octet-stream")
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        with open(path, "rb") as f:
            self.wfile.write(f.read())

    def _json_response(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())


def main():
    print(f"  🌐 IP Weave Web UI")
    print(f"  📍 http://{HOST}:{PORT}")
    print(f"  ⏎ 按 Ctrl+C 停止服务器")
    print()
    webbrowser.open(f"http://{HOST}:{PORT}")
    server = HTTPServer((HOST, PORT), WebUIHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()


if __name__ == "__main__":
    main()
