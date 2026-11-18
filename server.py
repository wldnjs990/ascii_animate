#!/usr/bin/env python3
"""아스키 영상 플레이어의 로컬 서버.

    python3 server.py        # http://127.0.0.1:8765 를 브라우저로 연다

링크의 영상을 yt-dlp 로 내려받아 이 PC의 브라우저에만 넘겨준다.
개인 감상용. 127.0.0.1 에만 열리며, 외부에 공개하는 용도가 아니다.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = "127.0.0.1"
PORT = int(os.environ.get("PORT", "8765"))
ROOT = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "ascii_play", "web")
ID_RE = re.compile(r"^[0-9a-f]{16}(-opus)?$")
# 같은 링크를 동시에 두 번 받지 않도록 내려받기는 한 번에 하나만 한다.
fetch_lock = threading.Lock()


def cached(video_id):
    path = os.path.join(CACHE_DIR, video_id + ".mp4")
    return path if os.path.isfile(path) else None


def fetch(url, opus):
    """영상을 브라우저가 재생할 수 있는 mp4 로 내려받고 (id, 오류) 를 돌려준다.

    opus 가 참이면 AAC 를 못 트는 브라우저(VS Code 내장 브라우저 등)를 위해
    오디오만 Opus 로 바꾼 사본을 만들어 그 id 를 돌려준다.
    """
    video_id = hashlib.sha1(url.encode()).hexdigest()[:16]
    with fetch_lock:
        if not cached(video_id):
            error = download(url, video_id)
            if error:
                return None, error
        if not opus:
            return video_id, None
        opus_id = video_id + "-opus"
        if not cached(opus_id):
            tmp = os.path.join(CACHE_DIR, opus_id + ".tmp.mp4")
            proc = subprocess.run([
                "ffmpeg", "-y", "-v", "error", "-i", cached(video_id),
                "-c:v", "copy", "-c:a", "libopus", "-b:a", "128k", tmp,
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if proc.returncode != 0:
                return None, "오디오 변환에 실패했습니다."
            os.replace(tmp, os.path.join(CACHE_DIR, opus_id + ".mp4"))
        return opus_id, None


def download(url, video_id):
    """yt-dlp 로 내려받는다. 실패하면 오류 문구를, 성공하면 None 을 돌려준다."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    cmd = [
        "yt-dlp", "--no-playlist", "--no-progress", "--quiet",
        # 아스키 격자는 작으므로 360p면 충분하다. 어느 브라우저에서나 재생되는 H.264/AAC를 우선한다.
        "-f", "bv*[height<=360][vcodec^=avc1]+ba[ext=m4a]/b[height<=360][ext=mp4]/b[height<=360]/b",
        "--merge-output-format", "mp4",
        "-o", os.path.join(CACHE_DIR, video_id + ".%(ext)s"),
        "--", url,
    ]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0 or not cached(video_id):
        lines = proc.stderr.strip().splitlines()
        return lines[-1] if lines else "내려받기에 실패했습니다."
    return None


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        pass

    def send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/":
            self.send_file(os.path.join(ROOT, "index.html"), "text/html; charset=utf-8")
        elif path.startswith("/video/") and ID_RE.match(path[7:]) and cached(path[7:]):
            self.send_file(cached(path[7:]), "video/mp4")
        else:
            self.send_json(404, {"error": "찾을 수 없습니다."})

    def do_POST(self):
        if self.path != "/api/fetch":
            return self.send_json(404, {"error": "찾을 수 없습니다."})
        # 다른 웹사이트가 이 로컬 서버에 요청을 보내는 것을 막는다.
        origin = self.headers.get("Origin")
        if origin and origin != f"http://{self.headers.get('Host')}":
            return self.send_json(403, {"error": "허용되지 않은 요청입니다."})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length))
            url = payload.get("url", "").strip()
        except (ValueError, AttributeError):
            return self.send_json(400, {"error": "요청 형식이 잘못됐습니다."})
        if not url.startswith(("http://", "https://")):
            return self.send_json(400, {"error": "http(s) 링크를 넣어 주세요."})
        video_id, error = fetch(url, bool(payload.get("opus")))
        if error:
            return self.send_json(502, {"error": error})
        self.send_json(200, {"id": video_id})

    def send_file(self, path, content_type):
        size = os.path.getsize(path)
        start, end = 0, size - 1
        # 브라우저가 영상을 탐색하려면 Range 요청에 응답해야 한다.
        match = re.match(r"bytes=(\d*)-(\d*)$", self.headers.get("Range", ""))
        if match and (match.group(1) or match.group(2)):
            if match.group(1):
                start = int(match.group(1))
                if match.group(2):
                    end = min(int(match.group(2)), size - 1)
            else:
                start = max(size - int(match.group(2)), 0)
            if start > end:
                self.send_response(416)
                self.send_header("Content-Range", f"bytes */{size}")
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
            self.send_response(206)
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        else:
            self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(end - start + 1))
        self.end_headers()
        remaining = end - start + 1
        try:
            with open(path, "rb") as f:
                f.seek(start)
                while remaining > 0:
                    chunk = f.read(min(256 * 1024, remaining))
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    remaining -= len(chunk)
        except (BrokenPipeError, ConnectionResetError):
            pass


def main():
    for tool in ("yt-dlp", "ffmpeg"):
        if shutil.which(tool) is None:
            sys.exit(f"'{tool}' 을(를) 찾을 수 없습니다. 예: brew install ffmpeg yt-dlp")
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"브라우저에서 http://{HOST}:{PORT} 을 여세요. (종료: Ctrl+C)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
