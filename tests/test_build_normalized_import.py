import csv
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "data-source" / "build_normalized_import.py"
SPEC = importlib.util.spec_from_file_location("build_normalized_import", MODULE_PATH)
build_normalized_import = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(build_normalized_import)
build_bundle = build_normalized_import.build_bundle


ONLINE = {
    "_dataVersion": 14,
    "accessCode": "online-private-code",
    "decks": [
        {"id": "hsk1", "sents": [{"id": "old-1"}]},
        {"id": "scene", "sents": [{"id": "scene-1"}]},
    ],
    "audio": {
        "old-1": {"f": {"n": "old-n", "s": "old-s"}},
        "scene-1": {"f": {"n": "scene-n", "s": "scene-s"}},
        "orphan": {"f": {"n": "orphan-n", "s": "orphan-s"}},
    },
}

LOCAL = {
    "decks": [
        {"id": "hsk1", "sents": [{"id": "hsk-1"}]},
        {"id": "nhsk1", "sents": [{"id": "nhsk-1"}]},
    ],
    "audio": {
        "hsk-1": {"f": {"n": "hsk-n", "s": "hsk-s"}},
        "nhsk-1": {"f": {"n": "nhsk-n", "s": "nhsk-s"}},
    },
}


class BuildNormalizedImportTest(unittest.TestCase):
    def test_bundle_uses_small_rows_and_two_safe_sql_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            expected_md5 = "a" * 32
            manifest = build_bundle(ONLINE, LOCAL, ["hsk1", "nhsk1"], output, expected_md5)

            self.assertEqual(manifest["deckCount"], 3)
            self.assertEqual(manifest["audioCount"], 4)
            self.assertEqual(manifest["targets"], {"hsk1": 1, "nhsk1": 1})
            with (output / "decks.csv").open(newline="", encoding="utf-8") as stream:
                self.assertEqual(sum(1 for _ in csv.reader(stream)), 3)
            with (output / "audio.csv").open(newline="", encoding="utf-8") as stream:
                self.assertEqual(sum(1 for _ in csv.reader(stream)), 4)
            self.assertLess(manifest["maxJsonCellBytes"], 2_000_000)
            self.assertEqual(set(manifest), {"deckCount", "audioCount", "targets", "files", "maxJsonCellBytes"})
            self.assertNotIn("online-private-code", json.dumps(manifest))
            self.assertNotIn("hsk-n", json.dumps(manifest))

            check_sql = (output / "check.sql").read_text()
            apply_sql = (output / "apply.sql").read_text()
            self.assertIn("ROLLBACK;", check_sql)
            self.assertNotIn("COMMIT;", check_sql)
            self.assertIn("COMMIT;", apply_sql)
            self.assertIn("pg_advisory_xact_lock(824202608)", apply_sql)
            self.assertIn("md5(payload::text)", apply_sql)
            self.assertIn(expected_md5, apply_sql)
            self.assertIn("VALUES (0, 'hsk1'), (1, 'nhsk1'), (2, 'scene')", apply_sql)
            self.assertIn("FROM stage_decks\n        EXCEPT", apply_sql)
            self.assertIn("expected deck order or IDs differ", apply_sql)
            self.assertIn("INSERT INTO trainer_store_meta", apply_sql)
            self.assertIn(str((output / "decks.csv").resolve()), apply_sql)
            self.assertNotIn("%s::jsonb", apply_sql)
            self.assertIn("count(*) FROM trainer_store_meta) AS meta_count", apply_sql)

    def test_normalizes_uppercase_md5_for_postgres_md5_guard(self):
        with tempfile.TemporaryDirectory() as tmp:
            sql = (Path(tmp) / "apply.sql")
            build_bundle(ONLINE, LOCAL, ["hsk1"], Path(tmp), "A" * 32)
            self.assertIn("'" + "a" * 32 + "'", sql.read_text())
            self.assertNotIn("'" + "A" * 32 + "'", sql.read_text())

    def test_rejects_expected_md5_that_is_not_exactly_32_hex_characters(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "32 位十六进制"):
                build_bundle(ONLINE, LOCAL, ["hsk1"], Path(tmp), "g" * 32)
            with self.assertRaisesRegex(ValueError, "32 位十六进制"):
                build_bundle(ONLINE, LOCAL, ["hsk1"], Path(tmp), "a" * 31)

    def test_rejects_json_cell_at_or_above_two_megabytes(self):
        oversized_local = json.loads(json.dumps(LOCAL))
        oversized_local["audio"]["hsk-1"]["f"]["n"] = "x" * 2_000_000
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "JSON 单元格"):
                build_bundle(ONLINE, oversized_local, ["hsk1"], Path(tmp), "a" * 32)


if __name__ == "__main__":
    unittest.main()
