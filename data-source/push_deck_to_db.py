#!/usr/bin/env python3
"""把本地某个 deck（含音频）推到线上 Postgres。

背景：线上 `apply_data_migrations()` 只认 hsk1/hsk2/hsk3 三个 deck id，
新 deck（nhsk1/nhsk2/…）改完重启**不会**自动同步；而 admin API 只能改
文本，**没有任何上传音频的接口**（`server.py` 里 data["audio"] 只被读和删）。
所以带音频的新 deck 只有直连 Postgres 这一条路。

安全约定：
  - 连接串不写死在代码里，也**不打印**；从文件或环境变量读。
  - 写库前必定先把线上整包备份到 backups/（该目录已 gitignore）。
  - 默认 dry-run，只有显式 --apply 才写。
  - 只动目标 deck 和它自己那些句子的音频，其余 deck 一律不碰。

用法：
    /usr/bin/python3 push_deck_to_db.py nhsk2                 # 只看差异，不写
    /usr/bin/python3 push_deck_to_db.py nhsk2 --apply         # 真写
    /usr/bin/python3 push_deck_to_db.py hsk1 nhsk1 nhsk2      # 三套一次合并演练
    /usr/bin/python3 push_deck_to_db.py nhsk2 --verify-only   # 只看线上现状
"""
import argparse
import datetime
import json
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOCAL_DATA = BASE_DIR / "data" / "trainer_data.private.json"
BACKUP_DIR = BASE_DIR / "backups"
DEFAULT_URL_FILE = Path.home() / "Claude" / "私密" / "tone_trainer_db.txt"
STATE_KEY = "trainer_data"


def die(msg):
    print(f"[错误] {msg}", file=sys.stderr)
    sys.exit(1)


def get_db_url(url_file):
    url = os.environ.get("DATABASE_URL", "").strip()
    if url:
        return url, "环境变量 DATABASE_URL"
    path = Path(url_file)
    if path.exists():
        url = path.read_text(encoding="utf-8").strip()
        if url:
            return url, f"文件 {path}"
    die(
        "拿不到连接串。请把 Render → tone-trainer 的 Postgres "
        f"External Database URL 存到 {path}（一行，别的什么都不要写），"
        "或者 export DATABASE_URL=… 之后再跑。"
    )


def ensure_ssl(url):
    return url if "sslmode=" in url else url + ("&" if "?" in url else "?") + "sslmode=require"


def mb(obj):
    return len(json.dumps(obj, ensure_ascii=False).encode("utf-8")) / 1e6


def describe(payload, label):
    decks = payload.get("decks", [])
    audio = payload.get("audio", {})
    print(f"\n== {label} ==")
    print(f"  整包 {mb(payload):.1f} MB · 音频 {len(audio)} 条 · _dataVersion={payload.get('_dataVersion')}")
    for deck in decks:
        sids = [s.get("id") for s in deck.get("sents", [])]
        with_audio = sum(1 for s in sids if s in audio)
        print(
            f"  - {deck.get('id'):<10} {deck.get('name', ''):<8} "
            f"单元 {len(deck.get('units', [])):>2} · 句 {len(sids):>3} · 有音频 {with_audio:>3}"
        )


def merge_decks(online, local, deck_ids):
    """Return one payload with selected local decks merged into the online state."""
    ordered_ids = list(dict.fromkeys(deck_ids))
    wanted = set(ordered_ids)
    local_by_id = {deck.get("id"): deck for deck in local.get("decks", [])}
    missing_decks = [deck_id for deck_id in ordered_ids if deck_id not in local_by_id]
    if missing_decks:
        raise ValueError("本地没有 deck：" + ", ".join(missing_decks))

    local_audio = local.get("audio", {})
    new_sentence_ids = set()
    for deck_id in ordered_ids:
        for sentence in local_by_id[deck_id].get("sents", []):
            sentence_id = sentence.get("id")
            if sentence_id:
                new_sentence_ids.add(sentence_id)
    missing_audio = sorted(
        sentence_id for sentence_id in new_sentence_ids if sentence_id not in local_audio
    )
    if missing_audio:
        raise ValueError(f"本地有 {len(missing_audio)} 句没有音频：{missing_audio[:5]}")

    merged = json.loads(json.dumps(online, ensure_ascii=False))
    online_decks = merged.get("decks", [])
    first_target_index = next(
        (index for index, deck in enumerate(online_decks) if deck.get("id") in wanted),
        len(online_decks),
    )
    unrelated_before = sum(
        1 for deck in online_decks[:first_target_index] if deck.get("id") not in wanted
    )
    old_target_sentence_ids = {
        sentence.get("id")
        for deck in online_decks
        if deck.get("id") in wanted
        for sentence in deck.get("sents", [])
        if sentence.get("id")
    }
    unrelated_decks = [deck for deck in online_decks if deck.get("id") not in wanted]
    replacement_decks = [
        json.loads(json.dumps(local_by_id[deck_id], ensure_ascii=False))
        for deck_id in ordered_ids
    ]
    merged["decks"] = (
        unrelated_decks[:unrelated_before]
        + replacement_decks
        + unrelated_decks[unrelated_before:]
    )

    unrelated_sentence_ids = {
        sentence.get("id")
        for deck in unrelated_decks
        for sentence in deck.get("sents", [])
        if sentence.get("id")
    }
    merged_audio = merged.setdefault("audio", {})
    for sentence_id in old_target_sentence_ids - new_sentence_ids - unrelated_sentence_ids:
        merged_audio.pop(sentence_id, None)
    for sentence_id in new_sentence_ids:
        merged_audio[sentence_id] = json.loads(
            json.dumps(local_audio[sentence_id], ensure_ascii=False)
        )
    return merged


def parse_args(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("deck_ids", nargs="+")
    ap.add_argument("--apply", action="store_true", help="真的写库（默认只看不写）")
    ap.add_argument("--verify-only", action="store_true", help="只打印线上现状后退出")
    ap.add_argument("--url-file", default=str(DEFAULT_URL_FILE))
    return ap.parse_args(argv)


def main():
    args = parse_args()

    try:
        import psycopg2
    except ImportError:
        die("缺 psycopg2：/usr/bin/python3 -m pip install --user psycopg2-binary")

    url, source = get_db_url(args.url_file)
    print(f"[i] 连接串来自：{source}（不打印内容）")

    conn = psycopg2.connect(ensure_ssl(url))
    conn.autocommit = False
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT payload FROM app_state WHERE key = %s", (STATE_KEY,))
            row = cur.fetchone()
        if not row:
            die(f"线上库里没有 key={STATE_KEY} 这行，先确认连的是不是对的库")
        online = row[0] if isinstance(row[0], (dict, list)) else json.loads(row[0])
        describe(online, "线上现状")

        if args.verify_only:
            return

        if not LOCAL_DATA.exists():
            die(f"本地数据文件不存在：{LOCAL_DATA}")
        local = json.loads(LOCAL_DATA.read_text(encoding="utf-8"))
        local_by_id = {deck.get("id"): deck for deck in local.get("decks", [])}
        try:
            merged = merge_decks(online, local, args.deck_ids)
        except ValueError as exc:
            die(str(exc))

        online_ids = {deck.get("id") for deck in online.get("decks", [])}
        expected = {}
        print("\n[计划] 以下 deck 在同一次事务中合并；其余 deck 不动：")
        for deck_id in dict.fromkeys(args.deck_ids):
            src_deck = local_by_id[deck_id]
            sids = [sentence.get("id") for sentence in src_deck.get("sents", [])]
            expected[deck_id] = sids
            print(
                f"  - {'覆盖' if deck_id in online_ids else '新增'} {deck_id}"
                f"（{len(src_deck.get('units', []))} 单元 / {len(sids)} 句 / {len(sids)} 条音频）"
            )

        describe(merged, "写入后（预期）")
        print(f"\n[体积] {mb(online):.1f} MB → {mb(merged):.1f} MB")

        if not args.apply:
            print("\n[dry-run] 没有写库。确认无误后加 --apply 重跑。")
            return

        BACKUP_DIR.mkdir(exist_ok=True)
        stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = BACKUP_DIR / f"线上_trainer_data_{stamp}.json"
        backup.write_text(json.dumps(online, ensure_ascii=False), encoding="utf-8")
        print(f"\n[备份] 线上原样已存 {backup}（{backup.stat().st_size / 1e6:.1f} MB）")

        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE app_state SET payload = %s::jsonb, updated_at = NOW()
                WHERE key = %s
                """,
                (json.dumps(merged, ensure_ascii=False), STATE_KEY),
            )
        conn.commit()
        print("[写入] 已提交")

        with conn.cursor() as cur:
            cur.execute("SELECT payload, updated_at FROM app_state WHERE key = %s", (STATE_KEY,))
            row2 = cur.fetchone()
        back = row2[0] if isinstance(row2[0], (dict, list)) else json.loads(row2[0])
        describe(back, f"回读复核（updated_at={row2[1]}）")

        all_ok = True
        print("\n[复核]")
        for deck_id, sids in expected.items():
            deck_back = next((d for d in back.get("decks", []) if d.get("id") == deck_id), None)
            ok_sents = deck_back is not None and len(deck_back.get("sents", [])) == len(sids)
            ok_audio = all(sid in back.get("audio", {}) for sid in sids)
            print(f"  - {deck_id}: 句数一致={ok_sents} · 音频齐全={ok_audio}")
            all_ok = all_ok and ok_sents and ok_audio
        if not all_ok:
            die("回读对不上，检查后可用备份文件回滚")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
