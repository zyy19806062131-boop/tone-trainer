#!/usr/bin/env python3
import argparse
import asyncio
import base64
import json
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "trainer_data.private.json"
TMP_DIR = BASE_DIR / ".audio_tmp"

VOICE_SETS = {
    "hsk": {
        "f": "zh-CN-XiaoxiaoNeural",
        "m": "zh-CN-YunyangNeural",
    },
    "yct": {
        "k": "zh-CN-YunxiaNeural",
    },
    "default": {
        "f": "zh-CN-XiaoxiaoNeural",
        "m": "zh-CN-YunyangNeural",
    },
}

RATES = {
    "f": {"n": "+0%", "s": "-40%"},
    "m": {"n": "-12%", "s": "-45%"},
    "k": {"n": "+0%", "s": "-40%"},
}


try:
    import edge_tts
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "edge-tts"], check=True)
    import edge_tts


def deck_voice_set(deck_id):
    if deck_id.startswith("hsk"):
        return VOICE_SETS["hsk"]
    if deck_id.startswith("yct"):
        return VOICE_SETS["yct"]
    return VOICE_SETS["default"]


def data_uri(path):
    return "data:audio/mpeg;base64," + base64.b64encode(path.read_bytes()).decode("ascii")


async def synth(text, voice, rate, path):
    last_error = None
    for attempt in range(1, 4):
        try:
            comm = edge_tts.Communicate(text, voice, rate=rate)
            await comm.save(str(path))
            return
        except Exception as exc:
            last_error = exc
            if path.exists():
                path.unlink()
            if attempt < 3:
                await asyncio.sleep(attempt)
    raise RuntimeError(f"Failed to synthesize {text!r} with {voice}") from last_error


async def list_voices():
    voices = await edge_tts.list_voices()
    for voice in sorted(v["ShortName"] for v in voices if v["ShortName"].startswith("zh-CN")):
        print(voice)


async def build(deck_ids, force):
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    decks = [deck for deck in data.get("decks", []) if not deck_ids or deck.get("id") in deck_ids]
    if not decks:
        raise SystemExit("No matching decks.")

    available = {v["ShortName"] for v in await edge_tts.list_voices()}
    needed = {voice for deck in decks for voice in deck_voice_set(deck["id"]).values()}
    missing = sorted(needed - available)
    if missing:
        raise SystemExit("Unavailable voices: " + ", ".join(missing))

    TMP_DIR.mkdir(exist_ok=True)
    audio = data.setdefault("audio", {})
    jobs = []
    for deck in decks:
        voices = deck_voice_set(deck["id"])
        for sentence in deck.get("sents", []):
            sid = sentence["id"]
            text = sentence["zh"]
            audio.setdefault(sid, {})
            for key, voice in voices.items():
                if not force and key in audio[sid] and {"n", "s"} <= set(audio[sid][key]):
                    continue
                jobs.append((deck["id"], sid, text, key, voice))

    total = len(jobs) * 2
    done = 0
    for deck_id, sid, text, key, voice in jobs:
        normal_path = TMP_DIR / f"{sid}_{key}_n.mp3"
        slow_path = TMP_DIR / f"{sid}_{key}_s.mp3"
        await synth(text, voice, RATES[key]["n"], normal_path)
        await synth(text, voice, RATES[key]["s"], slow_path)
        audio.setdefault(sid, {})[key] = {
            "n": data_uri(normal_path),
            "s": data_uri(slow_path),
        }
        normal_path.unlink(missing_ok=True)
        slow_path.unlink(missing_ok=True)
        done += 2
        print(f"[{done}/{total}] {deck_id} {sid} {key}: {text}")

    try:
        TMP_DIR.rmdir()
    except OSError:
        pass
    DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {DATA_PATH}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--deck", action="append", default=[], help="Deck id to build, e.g. hsk1")
    parser.add_argument("--force", action="store_true", help="Regenerate existing audio")
    parser.add_argument("--list", action="store_true", help="List available zh-CN voices")
    args = parser.parse_args()
    if args.list:
        asyncio.run(list_voices())
    else:
        asyncio.run(build(set(args.deck), args.force))


if __name__ == "__main__":
    main()
