#!/usr/bin/env python3
import json
import mimetypes
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse


BASE_DIR = Path(__file__).resolve().parent
ROOT = (BASE_DIR / "public").resolve()
DATA_PATH = BASE_DIR / "data" / "trainer_data.private.json"
CODES_PATH = BASE_DIR / "data" / "access_codes.private.json"
ADMIN_CODE = os.environ.get("ADMIN_CODE", "admin2026")


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, payload):
    temp_path = path.with_suffix(path.suffix + ".tmp")
    with temp_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")
    temp_path.replace(path)


def deck_summaries():
    data = load_json(DATA_PATH)
    return [
        {
            "id": deck.get("id"),
            "name": deck.get("name"),
            "sentenceCount": len(deck.get("sents", [])),
        }
        for deck in data.get("decks", [])
    ]


def build_payload(code):
    data = load_json(DATA_PATH)
    access_codes = load_json(CODES_PATH)
    profile = access_codes.get(code)
    if not profile:
        return None

    allowed = profile.get("decks")
    all_decks = data.get("decks", [])
    if allowed == "all":
        decks = all_decks
    else:
        allowed_set = set(allowed or [])
        decks = [deck for deck in all_decks if deck.get("id") in allowed_set]

    allowed_sentence_ids = {
        sentence.get("id")
        for deck in decks
        for sentence in deck.get("sents", [])
        if sentence.get("id")
    }
    audio = {
        sentence_id: voices
        for sentence_id, voices in data.get("audio", {}).items()
        if sentence_id in allowed_sentence_ids
    }

    return {
        "label": profile.get("label", "ACCESS GRANTED"),
        "decks": decks,
        "audio": audio,
    }


class ToneTrainerHandler(BaseHTTPRequestHandler):
    server_version = "ToneTrainer/1.0"

    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args))

    def send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def read_json_body(self, max_length=16384):
        length = int(self.headers.get("Content-Length", "0") or "0")
        if length > max_length:
            raise ValueError("请求太大")
        raw = self.rfile.read(length).decode("utf-8")
        return json.loads(raw or "{}")

    def is_admin_request(self):
        return self.headers.get("X-Admin-Code", "").strip() == ADMIN_CODE

    def require_admin(self):
        if self.is_admin_request():
            return True
        self.send_json(HTTPStatus.UNAUTHORIZED, {"error": "管理员口令不对"})
        return False

    def admin_overview(self):
        self.send_json(
            HTTPStatus.OK,
            {
                "decks": deck_summaries(),
                "accessCodes": load_json(CODES_PATH),
            },
        )

    def save_access_code(self, body):
        code = str(body.get("code", "")).strip()
        label = str(body.get("label", "")).strip()
        decks = body.get("decks")
        deck_ids = {deck["id"] for deck in deck_summaries() if deck.get("id")}

        if not code:
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": "code 不能为空"})
            return
        if not label:
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": "label 不能为空"})
            return
        if decks != "all":
            if not isinstance(decks, list) or not decks:
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": "至少选择一个项目"})
                return
            unknown = [deck_id for deck_id in decks if deck_id not in deck_ids]
            if unknown:
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": "项目不存在: " + ", ".join(unknown)})
                return

        access_codes = load_json(CODES_PATH)
        access_codes[code] = {"label": label, "decks": decks}
        save_json(CODES_PATH, access_codes)
        self.send_json(HTTPStatus.OK, {"ok": True, "accessCodes": access_codes})

    def delete_access_code(self, body):
        code = str(body.get("code", "")).strip()
        access_codes = load_json(CODES_PATH)
        if code not in access_codes:
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "code 不存在"})
            return
        del access_codes[code]
        save_json(CODES_PATH, access_codes)
        self.send_json(HTTPStatus.OK, {"ok": True, "accessCodes": access_codes})

    def do_POST(self):
        if self.path == "/api/login":
            try:
                body = self.read_json_body(4096)
            except ValueError as err:
                self.send_json(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"error": str(err)})
                return
            except Exception:
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": "请求格式不对"})
                return

            code = str(body.get("code", "")).strip()
            payload = build_payload(code)
            if not payload:
                self.send_json(HTTPStatus.UNAUTHORIZED, {"error": "口令不对"})
                return

            self.send_json(HTTPStatus.OK, payload)
            return

        if self.path == "/api/admin/login":
            try:
                body = self.read_json_body(4096)
            except Exception:
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": "请求格式不对"})
                return
            if str(body.get("code", "")).strip() != ADMIN_CODE:
                self.send_json(HTTPStatus.UNAUTHORIZED, {"error": "管理员口令不对"})
                return
            self.send_json(HTTPStatus.OK, {"ok": True})
            return

        if self.path == "/api/admin/access-code":
            if not self.require_admin():
                return
            try:
                self.save_access_code(self.read_json_body())
            except Exception:
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": "请求格式不对"})
            return

        if self.path == "/api/admin/access-code/delete":
            if not self.require_admin():
                return
            try:
                self.delete_access_code(self.read_json_body())
            except Exception:
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": "请求格式不对"})
            return

        if self.path != "/api/login":
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "接口不存在"})
            return

    def do_GET(self):
        parsed = urlparse(self.path)
        request_path = unquote(parsed.path)
        if request_path == "/":
            request_path = "/tone_trainer-ponk.html"
        if request_path == "/admin":
            request_path = "/admin.html"
        if request_path == "/api/admin/overview":
            if not self.require_admin():
                return
            self.admin_overview()
            return

        target = (ROOT / request_path.lstrip("/")).resolve()
        if (
            ROOT not in target.parents
            or not target.is_file()
            or target.name.endswith(".private.json")
            or ".private." in target.name
        ):
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        content_type = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
        body = target.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        if target.suffix in {".html", ".js", ".css"}:
            self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


def main():
    port = int(os.environ.get("PORT", "8765"))
    host = os.environ.get("HOST", "127.0.0.1")
    server = ThreadingHTTPServer((host, port), ToneTrainerHandler)
    print(f"Tone trainer backend running at http://{host}:{port}/tone_trainer-ponk.html")
    server.serve_forever()


if __name__ == "__main__":
    main()
