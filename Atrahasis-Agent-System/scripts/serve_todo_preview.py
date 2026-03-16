#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import time
import webbrowser
from datetime import datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

try:
    import markdown
except ImportError as exc:  # pragma: no cover - dependency availability is environment-specific
    raise SystemExit(
        "The 'markdown' package is required for the live TODO preview. Install it with 'pip install markdown'."
    ) from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Serve a live browser preview for docs/TODO.md.")
    parser.add_argument("--host", default="127.0.0.1", help="Bind address. Default: 127.0.0.1")
    parser.add_argument("--port", type=int, default=4173, help="Port to serve on. Default: 4173")
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open the live preview in your default browser after the server starts.",
    )
    return parser


def extract_title(source: str) -> str:
    for line in source.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return "Atrahasis TODO"


def count_tables(lines: list[str]) -> int:
    separator_pattern = re.compile(r"^\|?(?:\s*:?-{3,}:?\s*\|){1,}\s*:?-{3,}:?\s*\|?\s*$")
    return sum(1 for line in lines if separator_pattern.match(line.strip()))


def render_todo_payload(target_file: Path, repo_root: Path) -> dict[str, Any]:
    source = target_file.read_text(encoding="utf-8")
    lines = source.splitlines()
    stat = target_file.stat()

    engine = markdown.Markdown(extensions=["extra", "toc", "sane_lists"])
    html = engine.convert(source)
    toc_html = engine.toc or ""
    word_count = len(re.findall(r"\S+", source))
    heading_count = sum(1 for line in lines if re.match(r"^#{1,6}\s+", line.strip()))
    title = extract_title(source)

    return {
        "title": title,
        "html": html,
        "toc_html": toc_html,
        "line_count": len(lines),
        "word_count": word_count,
        "heading_count": heading_count,
        "table_count": count_tables(lines),
        "byte_count": len(source.encode("utf-8")),
        "updated_at": datetime.fromtimestamp(stat.st_mtime).astimezone().isoformat(),
        "updated_at_display": datetime.fromtimestamp(stat.st_mtime).astimezone().strftime("%b %d, %Y %I:%M:%S %p"),
        "source_path": str(target_file),
        "source_relpath": str(target_file.relative_to(repo_root)).replace("\\", "/"),
        "fingerprint": f"{stat.st_mtime_ns}-{stat.st_size}",
        "raw_url": "/TODO.md",
    }


def file_signature(target_file: Path) -> str:
    try:
        stat = target_file.stat()
    except FileNotFoundError:
        return "missing"
    return f"{stat.st_mtime_ns}-{stat.st_size}"


class TodoPreviewServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, server_address: tuple[str, int], handler_class: type[BaseHTTPRequestHandler], repo_root: Path):
        super().__init__(server_address, handler_class)
        self.repo_root = repo_root
        self.docs_dir = repo_root / "docs"
        self.target_file = self.docs_dir / "TODO.md"
        self.preview_file = self.docs_dir / "TODO.live.html"


class TodoPreviewHandler(BaseHTTPRequestHandler):
    server_version = "TodoPreview/1.0"

    @property
    def preview_server(self) -> TodoPreviewServer:
        return self.server  # type: ignore[return-value]

    def do_GET(self) -> None:
        path = urlparse(self.path).path

        if path in {"/", "/TODO.live.html"}:
            self.serve_preview_html()
            return

        if path in {"/TODO.md", "/raw/TODO.md"}:
            self.serve_raw_markdown()
            return

        if path == "/api/todo":
            self.serve_todo_payload()
            return

        if path == "/events":
            self.serve_events()
            return

        self.send_error(HTTPStatus.NOT_FOUND, "Not found")

    def serve_preview_html(self) -> None:
        preview_path = self.preview_server.preview_file
        if not preview_path.exists():
            self.send_error(HTTPStatus.NOT_FOUND, "Preview HTML not found")
            return

        body = preview_path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def serve_raw_markdown(self) -> None:
        target_file = self.preview_server.target_file
        if not target_file.exists():
            self.send_error(HTTPStatus.NOT_FOUND, "TODO.md not found")
            return

        body = target_file.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/markdown; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def serve_todo_payload(self) -> None:
        target_file = self.preview_server.target_file
        if not target_file.exists():
            self.send_json({"error": f"Missing markdown source: {target_file}"}, status=HTTPStatus.NOT_FOUND)
            return

        payload = render_todo_payload(target_file, self.preview_server.repo_root)
        self.send_json(payload)

    def serve_events(self) -> None:
        target_file = self.preview_server.target_file
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "keep-alive")
        self.end_headers()

        last_signature = None
        idle_ticks = 0

        try:
            while True:
                signature = file_signature(target_file)
                if signature != last_signature:
                    payload = {"fingerprint": signature, "updated_at": datetime.now().astimezone().isoformat()}
                    self.wfile.write(b"event: todo\n")
                    self.wfile.write(f"data: {json.dumps(payload)}\n\n".encode("utf-8"))
                    self.wfile.flush()
                    last_signature = signature
                    idle_ticks = 0
                else:
                    idle_ticks += 1
                    if idle_ticks >= 15:
                        self.wfile.write(b": keep-alive\n\n")
                        self.wfile.flush()
                        idle_ticks = 0

                time.sleep(0.75)
        except (BrokenPipeError, ConnectionResetError):
            return

    def send_json(self, payload: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {self.address_string()} {format % args}")


def main() -> int:
    args = build_parser().parse_args()
    repo_root = Path(__file__).resolve().parents[1]

    server = TodoPreviewServer((args.host, args.port), TodoPreviewHandler, repo_root)
    host, port = server.server_address
    url = f"http://{host}:{port}/TODO.live.html"

    print(f"Serving live preview for {server.target_file}")
    print(f"Open {url}")

    if args.open:
        webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping preview server.")
    finally:
        server.server_close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
