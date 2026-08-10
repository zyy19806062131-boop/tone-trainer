"""Build an offline, auditable normalized Tone Trainer import bundle."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from trainer_storage import (  # noqa: E402
    TRAINER_ADVISORY_LOCK,
    merge_selected_decks,
    split_trainer_payload,
)


MAX_JSON_CELL_BYTES = 2_000_000
_MD5_RE = re.compile(r"^[0-9a-fA-F]{32}$")


def parse_args(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--online-json", type=Path, required=True)
    parser.add_argument("--local-json", type=Path, required=True)
    parser.add_argument("--deck", action="append", required=True)
    parser.add_argument("--expected-online-md5", required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    return parser.parse_args(argv)


def _json_cell(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    if len(encoded.encode("utf-8")) >= MAX_JSON_CELL_BYTES:
        raise ValueError(f"JSON 单元格不得达到 {MAX_JSON_CELL_BYTES} bytes")
    return encoded


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _sql_escape(value: str) -> str:
    return value.replace("'", "''")


def _render_sql(
    *,
    meta_csv: Path,
    decks_csv: Path,
    audio_csv: Path,
    expected_online_md5: str,
    deck_count: int,
    audio_count: int,
    targets: dict[str, int],
    transaction_end: str,
) -> str:
    target_checks = " OR ".join(
        "(SELECT count(*) FROM trainer_decks d "
        "CROSS JOIN LATERAL jsonb_array_elements(d.payload->'sents') sentence "
        f"WHERE d.deck_id = '{_sql_escape(deck_id)}') <> {sentence_count}"
        for deck_id, sentence_count in targets.items()
    ) or "FALSE"
    target_ids = ", ".join(f"'{_sql_escape(deck_id)}'" for deck_id in targets)
    target_total = sum(targets.values())
    return f"""\\set ON_ERROR_STOP on
BEGIN;
SELECT pg_advisory_xact_lock({TRAINER_ADVISORY_LOCK});

CREATE TEMP TABLE stage_meta (
    payload jsonb NOT NULL,
    expected_deck_count integer NOT NULL,
    expected_audio_count integer NOT NULL
);
CREATE TEMP TABLE stage_decks (
    deck_order integer NOT NULL,
    deck_id text NOT NULL,
    payload jsonb NOT NULL
);
CREATE TEMP TABLE stage_audio (
    sentence_id text NOT NULL,
    deck_id text NULL,
    payload jsonb NOT NULL
);

\\copy stage_meta(payload, expected_deck_count, expected_audio_count) FROM '{_sql_escape(str(meta_csv))}' WITH (FORMAT csv, ENCODING 'UTF8')
\\copy stage_decks(deck_order, deck_id, payload) FROM '{_sql_escape(str(decks_csv))}' WITH (FORMAT csv, ENCODING 'UTF8')
\\copy stage_audio(sentence_id, deck_id, payload) FROM '{_sql_escape(str(audio_csv))}' WITH (FORMAT csv, ENCODING 'UTF8')

DO $guard$
BEGIN
    IF (SELECT count(*) FROM stage_meta) <> 1 THEN
        RAISE EXCEPTION 'staging meta must contain exactly one row';
    END IF;
    IF (SELECT count(*) FROM stage_decks) <> {deck_count}
       OR (SELECT count(*) FROM stage_audio) <> {audio_count} THEN
        RAISE EXCEPTION 'staging counts do not match manifest';
    END IF;
    IF EXISTS (SELECT 1 FROM stage_decks GROUP BY deck_id HAVING count(*) <> 1)
       OR EXISTS (SELECT 1 FROM stage_decks GROUP BY deck_order HAVING count(*) <> 1)
       OR EXISTS (SELECT 1 FROM stage_audio GROUP BY sentence_id HAVING count(*) <> 1) THEN
        RAISE EXCEPTION 'staging IDs or deck order are not unique';
    END IF;
    IF (SELECT expected_deck_count FROM stage_meta) <> {deck_count}
       OR (SELECT expected_audio_count FROM stage_meta) <> {audio_count} THEN
        RAISE EXCEPTION 'meta counts do not match manifest';
    END IF;
    IF (SELECT md5(payload::text) FROM app_state WHERE key='trainer_data')
       IS DISTINCT FROM '{_sql_escape(expected_online_md5)}' THEN
        RAISE EXCEPTION 'legacy trainer_data changed after backup';
    END IF;
END
$guard$;

DELETE FROM trainer_store_meta WHERE id=1;
DELETE FROM trainer_audio;
DELETE FROM trainer_decks;

INSERT INTO trainer_decks(deck_id, deck_order, payload, updated_at)
SELECT deck_id, deck_order, payload, NOW() FROM stage_decks ORDER BY deck_order;
INSERT INTO trainer_audio(sentence_id, deck_id, payload, updated_at)
SELECT sentence_id, NULLIF(deck_id, ''), payload, NOW() FROM stage_audio;

DO $verify$
BEGIN
    IF (SELECT count(*) FROM stage_decks s JOIN trainer_decks t
        ON t.deck_id=s.deck_id AND t.deck_order=s.deck_order AND t.payload=s.payload)
       <> {deck_count} THEN
        RAISE EXCEPTION 'deck rows differ after insert';
    END IF;
    IF (SELECT count(*) FROM stage_audio s JOIN trainer_audio t
        ON t.sentence_id=s.sentence_id
       AND t.deck_id IS NOT DISTINCT FROM NULLIF(s.deck_id, '')
       AND t.payload=s.payload) <> {audio_count} THEN
        RAISE EXCEPTION 'audio rows differ after insert';
    END IF;
    IF {target_checks} THEN
        RAISE EXCEPTION 'target sentence counts differ';
    END IF;
    IF (SELECT count(*)
        FROM trainer_decks d,
             LATERAL jsonb_array_elements(d.payload->'sents') sentence
        JOIN trainer_audio a ON a.sentence_id = sentence->>'id'
        WHERE d.deck_id = ANY(ARRAY[{target_ids}])
          AND (a.payload->'f') ? 'n'
          AND (a.payload->'f') ? 's') <> {target_total} THEN
        RAISE EXCEPTION 'target audio completeness differs';
    END IF;
END
$verify$;

INSERT INTO trainer_store_meta(id, payload, expected_deck_count, expected_audio_count, updated_at)
SELECT 1, payload, expected_deck_count, expected_audio_count, NOW() FROM stage_meta;

DO $final$
BEGIN
    IF (SELECT count(*) FROM trainer_decks) <> (SELECT expected_deck_count FROM trainer_store_meta WHERE id=1)
       OR (SELECT count(*) FROM trainer_audio) <> (SELECT expected_audio_count FROM trainer_store_meta WHERE id=1) THEN
        RAISE EXCEPTION 'normalized table counts differ from meta';
    END IF;
END
$final$;

{transaction_end}
"""


def build_bundle(
    online: dict[str, Any],
    local: dict[str, Any],
    deck_ids: list[str],
    out_dir: Path,
    expected_online_md5: str,
) -> dict[str, Any]:
    """Create a database-free CSV and SQL bundle, returning its public manifest."""
    if not _MD5_RE.fullmatch(expected_online_md5):
        raise ValueError("expected_online_md5 必须是 32 位十六进制")
    ordered_deck_ids = list(dict.fromkeys(deck_ids))
    if not ordered_deck_ids:
        raise ValueError("至少需要一个目标项目")

    merged = merge_selected_decks(online, local, ordered_deck_ids)
    rows = split_trainer_payload(merged)
    targets = {
        deck_id: len(next(row.payload for row in rows.decks if row.deck_id == deck_id)["sents"])
        for deck_id in ordered_deck_ids
    }
    deck_cells = [(row.deck_order, row.deck_id, _json_cell(row.payload)) for row in rows.decks]
    audio_cells = [
        (row.sentence_id, row.deck_id or "", _json_cell(row.payload)) for row in rows.audio
    ]
    meta_cell = _json_cell(rows.meta)
    max_json_cell_bytes = max(
        [len(meta_cell.encode("utf-8"))]
        + [len(cell[2].encode("utf-8")) for cell in deck_cells]
        + [len(cell[2].encode("utf-8")) for cell in audio_cells]
    )

    out_dir = Path(out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    meta_csv, decks_csv, audio_csv = (out_dir / name for name in ("meta.csv", "decks.csv", "audio.csv"))
    with meta_csv.open("w", newline="", encoding="utf-8") as stream:
        csv.writer(stream).writerow([meta_cell, len(deck_cells), len(audio_cells)])
    with decks_csv.open("w", newline="", encoding="utf-8") as stream:
        csv.writer(stream).writerows(deck_cells)
    with audio_csv.open("w", newline="", encoding="utf-8") as stream:
        csv.writer(stream).writerows(audio_cells)

    check_sql = _render_sql(
        meta_csv=meta_csv, decks_csv=decks_csv, audio_csv=audio_csv,
        expected_online_md5=expected_online_md5, deck_count=len(deck_cells),
        audio_count=len(audio_cells), targets=targets, transaction_end="ROLLBACK;",
    )
    apply_sql = _render_sql(
        meta_csv=meta_csv, decks_csv=decks_csv, audio_csv=audio_csv,
        expected_online_md5=expected_online_md5, deck_count=len(deck_cells),
        audio_count=len(audio_cells), targets=targets,
        transaction_end=("COMMIT;\n"
                         "SELECT (SELECT count(*) FROM trainer_decks) AS deck_count,\n"
                         "       (SELECT count(*) FROM trainer_audio) AS audio_count,\n"
                         "       (SELECT updated_at FROM trainer_store_meta WHERE id=1) AS updated_at;"),
    )
    (out_dir / "check.sql").write_text(check_sql, encoding="utf-8")
    (out_dir / "apply.sql").write_text(apply_sql, encoding="utf-8")

    manifest = {
        "deckCount": len(deck_cells),
        "audioCount": len(audio_cells),
        "targets": targets,
        "files": {
            path.name: _sha256(path)
            for path in (meta_csv, decks_csv, audio_csv, out_dir / "check.sql", out_dir / "apply.sql")
        },
        "maxJsonCellBytes": max_json_cell_bytes,
    }
    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return manifest


def main(argv=None) -> int:
    args = parse_args(argv)
    online = json.loads(args.online_json.read_text(encoding="utf-8"))
    local = json.loads(args.local_json.read_text(encoding="utf-8"))
    manifest = build_bundle(online, local, args.deck, args.out_dir, args.expected_online_md5)
    print(json.dumps(manifest, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
