#!/usr/bin/env python3
import json
import mimetypes
import os
import re
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse


BASE_DIR = Path(__file__).resolve().parent
ROOT = (BASE_DIR / "public").resolve()
DATA_PATH = BASE_DIR / "data" / "trainer_data.private.json"
CODES_PATH = BASE_DIR / "data" / "access_codes.private.json"
ADMIN_CODE = os.environ.get("ADMIN_CODE", "admin2026")
DECK_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
DEFAULT_UNIT_ID = "default"
DEFAULT_UNIT_NAME = "全部"


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
    for deck in data.get("decks", []):
        normalize_deck(deck)
    return [
        {
            "id": deck.get("id"),
            "name": deck.get("name"),
            "full": bool(deck.get("full", False)),
            "hidden": bool(deck.get("hidden", False)),
            "units": deck.get("units", []),
            "sentenceCount": len(deck.get("sents", [])),
            "unitCount": len(deck.get("units", [])),
        }
        for deck in data.get("decks", [])
    ]


def find_deck(data, deck_id):
    for deck in data.get("decks", []):
        if deck.get("id") == deck_id:
            return deck
    return None


def normalize_deck(deck):
    units = deck.get("units")
    if not isinstance(units, list) or not units:
        units = [{"id": DEFAULT_UNIT_ID, "name": DEFAULT_UNIT_NAME}]
    clean_units = []
    seen = set()
    for unit in units:
        unit_id = str(unit.get("id", "")).strip()
        name = str(unit.get("name", "")).strip()
        if not unit_id or not name or unit_id in seen:
            continue
        clean_units.append({"id": unit_id, "name": name, "hidden": bool(unit.get("hidden", False))})
        seen.add(unit_id)
    if not clean_units:
        clean_units = [{"id": DEFAULT_UNIT_ID, "name": DEFAULT_UNIT_NAME, "hidden": False}]
        seen = {DEFAULT_UNIT_ID}
    if DEFAULT_UNIT_ID not in seen:
        clean_units.insert(0, {"id": DEFAULT_UNIT_ID, "name": DEFAULT_UNIT_NAME, "hidden": False})
        seen.add(DEFAULT_UNIT_ID)
    deck["units"] = clean_units
    for sentence in deck.get("sents", []):
        if sentence.get("unitId") not in seen:
            sentence["unitId"] = clean_units[0]["id"]
    return deck


def validate_unit(unit):
    unit_id = str(unit.get("id", "")).strip()
    name = str(unit.get("name", "")).strip()
    if not unit_id:
        raise ValueError("二级项目 ID 不能为空")
    if not DECK_ID_RE.match(unit_id):
        raise ValueError("二级项目 ID 只能用小写字母、数字和连字符，并且要以字母或数字开头")
    if not name:
        raise ValueError("二级项目名称不能为空")
    return {"id": unit_id, "name": name, "hidden": bool(unit.get("hidden", False))}


def validate_sentence(sentence):
    sentence_id = str(sentence.get("id", "")).strip()
    zh = str(sentence.get("zh", "")).strip()
    en = str(sentence.get("en", "")).strip()
    syl = sentence.get("syl")
    if not sentence_id:
        raise ValueError("句子 id 不能为空")
    if not zh:
        raise ValueError("中文不能为空")
    if not en:
        raise ValueError("英文不能为空")
    if not isinstance(syl, list) or not syl:
        raise ValueError("拼音/声调不能为空")

    clean_syl = []
    for item in syl:
        pinyin = str(item.get("p", "")).strip()
        try:
            tone = int(item.get("t"))
        except Exception as exc:
            raise ValueError("声调必须是数字") from exc
        stress = str(item.get("s", "")).strip()
        if not pinyin:
            raise ValueError("拼音不能为空")
        if tone not in {0, 1, 2, 3, 4, 5}:
            raise ValueError("声调只能是 0-5")
        clean = {"p": pinyin, "t": tone}
        if stress in {"stress", "weak"}:
            clean["s"] = stress
        clean_syl.append(clean)

    if len(clean_syl) != len(zh):
        raise ValueError("拼音数量需要和汉字数量一致")
    return {"id": sentence_id, "zh": zh, "en": en, "syl": clean_syl}


def validate_deck(deck):
    deck_id = str(deck.get("id", "")).strip()
    name = str(deck.get("name", "")).strip()
    if not deck_id:
        raise ValueError("项目 ID 不能为空")
    if not DECK_ID_RE.match(deck_id):
        raise ValueError("项目 ID 只能用小写字母、数字和连字符，并且要以字母或数字开头")
    if not name:
        raise ValueError("项目名称不能为空")
    return {"id": deck_id, "name": name, "full": bool(deck.get("full", False)), "hidden": bool(deck.get("hidden", False))}


def visible_deck_for_profile(deck, profile):
    normalize_deck(deck)
    if deck.get("hidden"):
        return None
    unit_rules = profile.get("units") if isinstance(profile.get("units"), dict) else {}
    allowed_units = unit_rules.get(deck.get("id"))
    visible_units = []
    for unit in deck.get("units", []):
        if unit.get("hidden"):
            continue
        if isinstance(allowed_units, list) and unit.get("id") not in allowed_units:
            continue
        visible_units.append(unit)
    visible_unit_ids = {unit.get("id") for unit in visible_units}
    visible_sents = [
        sentence
        for sentence in deck.get("sents", [])
        if sentence.get("unitId", DEFAULT_UNIT_ID) in visible_unit_ids
    ]
    if not visible_units and not visible_sents:
        return None
    return {**deck, "units": visible_units, "sents": visible_sents}


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
    decks = [visible for deck in decks if (visible := visible_deck_for_profile(deck, profile))]

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
        units = body.get("units") if isinstance(body.get("units"), dict) else {}
        summaries = deck_summaries()
        deck_ids = {deck["id"] for deck in summaries if deck.get("id")}
        unit_ids_by_deck = {
            deck["id"]: {unit.get("id") for unit in deck.get("units", []) if unit.get("id")}
            for deck in summaries
        }

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
        clean_units = {}
        for deck_id, unit_ids in units.items():
            if deck_id not in deck_ids:
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": "项目不存在: " + deck_id})
                return
            if not isinstance(unit_ids, list):
                continue
            unknown_units = [unit_id for unit_id in unit_ids if unit_id not in unit_ids_by_deck.get(deck_id, set())]
            if unknown_units:
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": "二级项目不存在: " + ", ".join(unknown_units)})
                return
            clean_units[deck_id] = unit_ids

        access_codes = load_json(CODES_PATH)
        profile = {"label": label, "decks": decks}
        if clean_units:
            profile["units"] = clean_units
        access_codes[code] = profile
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

    def admin_deck(self, deck_id):
        data = load_json(DATA_PATH)
        deck = find_deck(data, deck_id)
        if not deck:
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "项目不存在"})
            return
        normalize_deck(deck)
        self.send_json(HTTPStatus.OK, {"deck": deck})

    def save_deck(self, body):
        original_id = str(body.get("originalId", "")).strip()
        clean_deck = validate_deck(body.get("deck") or {})
        data = load_json(DATA_PATH)
        decks = data.setdefault("decks", [])
        match_id = original_id or clean_deck["id"]
        existing_index = next((i for i, item in enumerate(decks) if item.get("id") == match_id), None)
        duplicate = next(
            (item for item in decks if item.get("id") == clean_deck["id"] and item.get("id") != match_id),
            None,
        )
        if duplicate:
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": "项目 ID 已存在"})
            return

        access_codes = load_json(CODES_PATH)
        access_changed = False
        if existing_index is None:
            decks.append({**clean_deck, "units": [{"id": DEFAULT_UNIT_ID, "name": DEFAULT_UNIT_NAME, "hidden": False}], "sents": []})
        else:
            old_deck = decks[existing_index]
            normalize_deck(old_deck)
            old_id = old_deck.get("id")
            decks[existing_index] = {
                **old_deck,
                **clean_deck,
                "units": old_deck.get("units", []),
                "sents": old_deck.get("sents", []),
            }
            if old_id != clean_deck["id"]:
                for profile in access_codes.values():
                    if isinstance(profile.get("decks"), list):
                        profile["decks"] = [
                            clean_deck["id"] if deck_id == old_id else deck_id
                            for deck_id in profile.get("decks", [])
                        ]
                        access_changed = True
                    if isinstance(profile.get("units"), dict) and old_id in profile["units"]:
                        profile["units"][clean_deck["id"]] = profile["units"].pop(old_id)
                        access_changed = True

        save_json(DATA_PATH, data)
        if access_changed:
            save_json(CODES_PATH, access_codes)
        self.send_json(
            HTTPStatus.OK,
            {"ok": True, "decks": deck_summaries(), "accessCodes": load_json(CODES_PATH)},
        )

    def delete_deck(self, body):
        deck_id = str(body.get("deckId", "")).strip()
        data = load_json(DATA_PATH)
        decks = data.setdefault("decks", [])
        deck = find_deck(data, deck_id)
        if not deck:
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "项目不存在"})
            return

        removed_sentence_ids = {item.get("id") for item in deck.get("sents", []) if item.get("id")}
        data["decks"] = [item for item in decks if item.get("id") != deck_id]
        audio = data.get("audio", {})
        for sentence_id in removed_sentence_ids:
            audio.pop(sentence_id, None)

        access_codes = load_json(CODES_PATH)
        for profile in access_codes.values():
            if isinstance(profile.get("decks"), list):
                profile["decks"] = [item for item in profile.get("decks", []) if item != deck_id]
            if isinstance(profile.get("units"), dict):
                profile["units"].pop(deck_id, None)

        save_json(DATA_PATH, data)
        save_json(CODES_PATH, access_codes)
        self.send_json(
            HTTPStatus.OK,
            {"ok": True, "decks": deck_summaries(), "accessCodes": access_codes},
        )

    def reorder_deck(self, body):
        deck_id = str(body.get("deckId", "")).strip()
        direction = str(body.get("direction", "")).strip()
        data = load_json(DATA_PATH)
        decks = data.setdefault("decks", [])
        index = next((i for i, item in enumerate(decks) if item.get("id") == deck_id), None)
        if index is None:
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "项目不存在"})
            return
        if direction not in {"up", "down"}:
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": "移动方向不对"})
            return
        new_index = index - 1 if direction == "up" else index + 1
        if 0 <= new_index < len(decks):
            decks[index], decks[new_index] = decks[new_index], decks[index]
            save_json(DATA_PATH, data)
        self.send_json(HTTPStatus.OK, {"ok": True, "decks": deck_summaries()})

    def save_unit(self, body):
        deck_id = str(body.get("deckId", "")).strip()
        original_id = str(body.get("originalId", "")).strip()
        clean_unit = validate_unit(body.get("unit") or {})
        data = load_json(DATA_PATH)
        deck = find_deck(data, deck_id)
        if not deck:
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "项目不存在"})
            return
        normalize_deck(deck)
        units = deck.setdefault("units", [])
        match_id = original_id or clean_unit["id"]
        existing_index = next((i for i, item in enumerate(units) if item.get("id") == match_id), None)
        duplicate = next((item for item in units if item.get("id") == clean_unit["id"] and item.get("id") != match_id), None)
        if duplicate:
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": "二级项目 ID 已存在"})
            return
        if existing_index is None:
            units.append(clean_unit)
        else:
            old_id = units[existing_index].get("id")
            units[existing_index] = clean_unit
            if old_id != clean_unit["id"]:
                for sentence in deck.get("sents", []):
                    if sentence.get("unitId") == old_id:
                        sentence["unitId"] = clean_unit["id"]
                access_codes = load_json(CODES_PATH)
                for profile in access_codes.values():
                    unit_rules = profile.get("units")
                    if isinstance(unit_rules, dict) and isinstance(unit_rules.get(deck_id), list):
                        unit_rules[deck_id] = [
                            clean_unit["id"] if unit_id == old_id else unit_id
                            for unit_id in unit_rules.get(deck_id, [])
                        ]
                save_json(CODES_PATH, access_codes)
        save_json(DATA_PATH, data)
        self.send_json(HTTPStatus.OK, {"ok": True, "deck": deck, "decks": deck_summaries()})

    def delete_unit(self, body):
        deck_id = str(body.get("deckId", "")).strip()
        unit_id = str(body.get("unitId", "")).strip()
        if unit_id == DEFAULT_UNIT_ID:
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": "默认二级项目不能删除"})
            return
        data = load_json(DATA_PATH)
        deck = find_deck(data, deck_id)
        if not deck:
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "项目不存在"})
            return
        normalize_deck(deck)
        before = len(deck.get("units", []))
        deck["units"] = [item for item in deck.get("units", []) if item.get("id") != unit_id]
        if len(deck["units"]) == before:
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "二级项目不存在"})
            return
        for sentence in deck.get("sents", []):
            if sentence.get("unitId") == unit_id:
                sentence["unitId"] = DEFAULT_UNIT_ID
        access_codes = load_json(CODES_PATH)
        for profile in access_codes.values():
            unit_rules = profile.get("units")
            if isinstance(unit_rules, dict) and isinstance(unit_rules.get(deck_id), list):
                unit_rules[deck_id] = [item for item in unit_rules.get(deck_id, []) if item != unit_id]
        save_json(CODES_PATH, access_codes)
        save_json(DATA_PATH, data)
        self.send_json(HTTPStatus.OK, {"ok": True, "deck": deck, "decks": deck_summaries()})

    def reorder_unit(self, body):
        deck_id = str(body.get("deckId", "")).strip()
        unit_id = str(body.get("unitId", "")).strip()
        direction = str(body.get("direction", "")).strip()
        data = load_json(DATA_PATH)
        deck = find_deck(data, deck_id)
        if not deck:
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "项目不存在"})
            return
        normalize_deck(deck)
        units = deck.get("units", [])
        index = next((i for i, item in enumerate(units) if item.get("id") == unit_id), None)
        if index is None:
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "二级项目不存在"})
            return
        if direction not in {"up", "down"}:
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": "移动方向不对"})
            return
        new_index = index - 1 if direction == "up" else index + 1
        if 0 <= new_index < len(units):
            units[index], units[new_index] = units[new_index], units[index]
            save_json(DATA_PATH, data)
        self.send_json(HTTPStatus.OK, {"ok": True, "deck": deck, "decks": deck_summaries()})

    def save_sentence(self, body):
        deck_id = str(body.get("deckId", "")).strip()
        unit_id = str(body.get("unitId", "")).strip() or DEFAULT_UNIT_ID
        original_id = str(body.get("originalId", "")).strip()
        sentence = validate_sentence(body.get("sentence") or {})
        data = load_json(DATA_PATH)
        deck = find_deck(data, deck_id)
        if not deck:
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "项目不存在"})
            return
        normalize_deck(deck)
        unit_ids = {unit.get("id") for unit in deck.get("units", [])}
        if unit_id not in unit_ids:
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": "二级项目不存在"})
            return
        sentence["unitId"] = unit_id

        sentences = deck.setdefault("sents", [])
        match_id = original_id or sentence["id"]
        existing_index = next((i for i, item in enumerate(sentences) if item.get("id") == match_id), None)
        duplicate = next(
            (item for item in sentences if item.get("id") == sentence["id"] and item.get("id") != match_id),
            None,
        )
        if duplicate:
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": "句子 id 已存在"})
            return

        if existing_index is None:
            sentences.append(sentence)
        else:
            old_id = sentences[existing_index].get("id")
            sentences[existing_index] = sentence
            if old_id != sentence["id"] and old_id in data.get("audio", {}):
                data.setdefault("audio", {})[sentence["id"]] = data.get("audio", {}).pop(old_id)

        save_json(DATA_PATH, data)
        self.send_json(HTTPStatus.OK, {"ok": True, "deck": deck})

    def delete_sentence(self, body):
        deck_id = str(body.get("deckId", "")).strip()
        sentence_id = str(body.get("sentenceId", "")).strip()
        data = load_json(DATA_PATH)
        deck = find_deck(data, deck_id)
        if not deck:
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "项目不存在"})
            return
        before = len(deck.get("sents", []))
        deck["sents"] = [item for item in deck.get("sents", []) if item.get("id") != sentence_id]
        if len(deck["sents"]) == before:
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "句子不存在"})
            return
        data.get("audio", {}).pop(sentence_id, None)
        save_json(DATA_PATH, data)
        self.send_json(HTTPStatus.OK, {"ok": True, "deck": deck})

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

        if self.path == "/api/admin/deck":
            if not self.require_admin():
                return
            try:
                self.save_deck(self.read_json_body(16384))
            except ValueError as err:
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": str(err)})
            except Exception:
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": "请求格式不对"})
            return

        if self.path == "/api/admin/deck/delete":
            if not self.require_admin():
                return
            try:
                self.delete_deck(self.read_json_body())
            except Exception:
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": "请求格式不对"})
            return

        if self.path == "/api/admin/deck/reorder":
            if not self.require_admin():
                return
            try:
                self.reorder_deck(self.read_json_body())
            except Exception:
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": "请求格式不对"})
            return

        if self.path == "/api/admin/unit":
            if not self.require_admin():
                return
            try:
                self.save_unit(self.read_json_body())
            except ValueError as err:
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": str(err)})
            except Exception:
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": "请求格式不对"})
            return

        if self.path == "/api/admin/unit/delete":
            if not self.require_admin():
                return
            try:
                self.delete_unit(self.read_json_body())
            except Exception:
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": "请求格式不对"})
            return

        if self.path == "/api/admin/unit/reorder":
            if not self.require_admin():
                return
            try:
                self.reorder_unit(self.read_json_body())
            except Exception:
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": "请求格式不对"})
            return

        if self.path == "/api/admin/sentence":
            if not self.require_admin():
                return
            try:
                self.save_sentence(self.read_json_body(65536))
            except ValueError as err:
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": str(err)})
            except Exception:
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": "请求格式不对"})
            return

        if self.path == "/api/admin/sentence/delete":
            if not self.require_admin():
                return
            try:
                self.delete_sentence(self.read_json_body())
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
        if request_path == "/api/admin/deck":
            if not self.require_admin():
                return
            deck_id = (parse_qs(parsed.query).get("id") or [""])[0]
            self.admin_deck(deck_id)
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
