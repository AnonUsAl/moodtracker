"""MoodTracker Web 服务器

用 Python 标准库 http.server 提供本地 Web 界面。
启动后浏览器访问 http://localhost:7777

用法:
    python server.py
"""

import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime
from urllib.parse import parse_qs

from storage import load_records, save_records

HOST = "127.0.0.1"
PORT = 7777
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")


class MoodHandler(SimpleHTTPRequestHandler):
    """处理 Web 界面和 API 请求。"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def _send_cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(204)
        self._send_cors()
        self.end_headers()

    def do_GET(self):
        """GET /api/records → 返回全部记录"""
        if self.path == "/api/records":
            self._send_json(load_records())
        elif self.path.startswith("/api/"):
            self._send_json({"error": "not found"}, 404)
        else:
            # 其他请求交给静态文件处理器（index.html 等）
            super().do_GET()

    def do_POST(self):
        """POST /api/records → 新增一条记录"""
        if self.path != "/api/records":
            self._send_json({"error": "not found"}, 404)
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._send_json({"error": "invalid json"}, 400)
            return

        mood = data.get("mood")
        note = data.get("note", "").strip()

        if mood not in (1, 2, 3, 4, 5):
            self._send_json({"error": "mood must be 1-5"}, 400)
            return

        now = datetime.now()
        record = {
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M"),
            "mood": mood,
            "note": note,
        }

        records = load_records()
        records.append(record)
        save_records(records)

        self._send_json({"ok": True, "record": record})

    def end_headers(self):
        self._send_cors()
        super().end_headers()


def main():
    server = HTTPServer((HOST, PORT), MoodHandler)
    print(f"MoodTracker Web 服务已启动")
    print(f"浏览器访问: http://{HOST}:{PORT}")
    print(f"按 Ctrl+C 停止\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止。")
        server.server_close()


if __name__ == "__main__":
    main()
