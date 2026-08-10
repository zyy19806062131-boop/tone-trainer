import copy
import unittest

from trainer_storage import reconstruct_trainer_payload, split_trainer_payload


SAMPLE = {
    "_dataVersion": 14,
    "keep": {"unchanged": True},
    "decks": [
        {"id": "hsk1", "name": "HSK1", "units": [], "sents": [
            {"id": "h1-a", "zh": "你好", "en": "hello", "syl": [{"p": "nǐ", "t": 3}, {"p": "hǎo", "t": 3}]},
            {"id": "h1-no-audio", "zh": "谢谢", "en": "thanks", "syl": [{"p": "xiè", "t": 4}, {"p": "xie", "t": 0}]},
        ]},
        {"id": "scene", "name": "Scene", "units": [], "sents": [
            {"id": "scene-a", "zh": "再见", "en": "bye", "syl": [{"p": "zài", "t": 4}, {"p": "jiàn", "t": 4}]},
        ]},
    ],
    "audio": {
        "h1-a": {"f": {"n": "data:audio/mpeg;base64,AAA", "s": "data:audio/mpeg;base64,BBB"}},
        "scene-a": {"f": {"n": "data:audio/mpeg;base64,CCC", "s": "data:audio/mpeg;base64,DDD"}},
        "orphan": {"f": {"n": "data:audio/mpeg;base64,EEE", "s": "data:audio/mpeg;base64,FFF"}},
    },
}


class ScriptedCursor:
    def __init__(self, responses):
        self.responses = list(responses)
        self.current = []
        self.calls = []

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def execute(self, sql, params=None):
        self.calls.append(("execute", " ".join(sql.split()), params))
        self.current = self.responses.pop(0) if self.responses else []

    def executemany(self, sql, params):
        self.calls.append(("executemany", " ".join(sql.split()), list(params)))

    def fetchone(self):
        return self.current[0] if self.current else None

    def fetchall(self):
        return list(self.current)


class ScriptedConnection:
    def __init__(self, responses):
        self.cursor_obj = ScriptedCursor(responses)

    def cursor(self):
        return self.cursor_obj


class PayloadRowsTest(unittest.TestCase):
    def test_split_and_reconstruct_are_exact_with_orphan_and_missing_audio(self):
        original = copy.deepcopy(SAMPLE)
        rows = split_trainer_payload(SAMPLE)

        self.assertEqual([row.deck_id for row in rows.decks], ["hsk1", "scene"])
        self.assertIsNone(next(row for row in rows.audio if row.sentence_id == "orphan").deck_id)
        self.assertEqual(reconstruct_trainer_payload(rows), original)
        self.assertEqual(SAMPLE, original)

    def test_duplicate_deck_id_is_rejected(self):
        payload = copy.deepcopy(SAMPLE)
        payload["decks"].append(copy.deepcopy(payload["decks"][0]))
        with self.assertRaisesRegex(ValueError, "重复项目 ID"):
            split_trainer_payload(payload)

    def test_duplicate_sentence_id_is_rejected(self):
        payload = copy.deepcopy(SAMPLE)
        payload["decks"][1]["sents"][0]["id"] = "h1-a"
        with self.assertRaisesRegex(ValueError, "重复句子 ID"):
            split_trainer_payload(payload)


class NormalizedReadTest(unittest.TestCase):
    def test_returns_none_when_no_normalized_record_is_active(self):
        from trainer_storage import load_normalized_trainer_data

        conn = ScriptedConnection([[]])

        self.assertIsNone(load_normalized_trainer_data(conn))
        self.assertEqual(len(conn.cursor_obj.calls), 1)

    def test_reconstructs_a_complete_normalized_record(self):
        from trainer_storage import load_normalized_trainer_data

        responses = [
            [({"_dataVersion": 14}, 2, 3)],
            [(0, "hsk1", SAMPLE["decks"][0]), (1, "scene", SAMPLE["decks"][1])],
            [
                (sid, None if sid == "orphan" else ("hsk1" if sid == "h1-a" else "scene"), voices)
                for sid, voices in SAMPLE["audio"].items()
            ],
        ]

        self.assertEqual(
            load_normalized_trainer_data(ScriptedConnection(responses)),
            {"_dataVersion": 14, "decks": SAMPLE["decks"], "audio": SAMPLE["audio"]},
        )

    def test_warns_and_returns_none_when_normalized_counts_do_not_match(self):
        from trainer_storage import load_normalized_trainer_data

        warnings = []
        conn = ScriptedConnection([
            [({"_dataVersion": 14}, 2, 3)],
            [(0, "hsk1", SAMPLE["decks"][0])],
            [("h1-a", "hsk1", SAMPLE["audio"]["h1-a"])],
        ])

        self.assertIsNone(load_normalized_trainer_data(conn, warn=warnings.append))
        self.assertEqual(
            warnings,
            ["[warn] 规范化训练数据不完整，退回旧 app_state：decks 1/2, audio 1/3"],
        )

    def test_schema_uses_the_required_tables_and_audio_index(self):
        from trainer_storage import ensure_normalized_schema

        cursor = ScriptedCursor([])

        ensure_normalized_schema(cursor)

        statements = [call[1] for call in cursor.calls]
        self.assertEqual(len(statements), 4)
        self.assertIn("CREATE TABLE IF NOT EXISTS trainer_store_meta", statements[0])
        self.assertIn("CREATE TABLE IF NOT EXISTS trainer_decks", statements[1])
        self.assertIn("CREATE TABLE IF NOT EXISTS trainer_audio", statements[2])
        self.assertEqual(
            statements[3],
            "CREATE INDEX IF NOT EXISTS trainer_audio_deck_id_idx ON trainer_audio(deck_id)",
        )


class MergeSelectedDecksTest(unittest.TestCase):
    def test_merge_replaces_targets_and_preserves_unrelated_content(self):
        from trainer_storage import merge_selected_decks

        online = copy.deepcopy(SAMPLE)
        local = {
            "decks": [
                {"id": "hsk1", "name": "New old HSK1", "units": [], "sents": [{"id": "h1-new"}]},
                {"id": "nhsk1", "name": "New HSK1", "units": [], "sents": [{"id": "nh1-new"}]},
            ],
            "audio": {
                "h1-new": {"f": {"n": "h1n", "s": "h1s"}},
                "nh1-new": {"f": {"n": "nh1n", "s": "nh1s"}},
            },
        }
        merged = merge_selected_decks(online, local, ["hsk1", "nhsk1"])
        self.assertEqual([deck["id"] for deck in merged["decks"]], ["hsk1", "nhsk1", "scene"])
        self.assertEqual(merged["decks"][2], online["decks"][1])
        self.assertEqual(merged["_dataVersion"], online["_dataVersion"])
        self.assertEqual(merged["keep"], online["keep"])
        self.assertNotIn("h1-a", merged["audio"])
        self.assertEqual(merged["audio"]["scene-a"], online["audio"]["scene-a"])
        self.assertEqual(merged["audio"]["orphan"], online["audio"]["orphan"])

    def test_merge_deduplicates_requested_ids_while_preserving_first_seen_order(self):
        from trainer_storage import merge_selected_decks

        local = {
            "decks": [{"id": "hsk1", "sents": [{"id": "h1-new"}]}],
            "audio": {"h1-new": {"f": {"n": "h1n", "s": "h1s"}}},
        }
        merged = merge_selected_decks(SAMPLE, local, ["hsk1", "hsk1"])

        self.assertEqual([deck["id"] for deck in merged["decks"]], ["hsk1", "scene"])

    def test_merge_keeps_inputs_and_result_independently_mutable(self):
        from trainer_storage import merge_selected_decks

        online = copy.deepcopy(SAMPLE)
        local = {
            "decks": [{"id": "hsk1", "sents": [{"id": "h1-new", "extra": {"value": 1}}]}],
            "audio": {"h1-new": {"f": {"n": "h1n", "s": "h1s"}}},
        }
        original_online = copy.deepcopy(online)
        original_local = copy.deepcopy(local)

        merged = merge_selected_decks(online, local, ["hsk1"])
        merged["decks"][0]["sents"][0]["extra"]["value"] = 2
        merged["audio"]["h1-new"]["f"]["n"] = "changed"
        merged["keep"]["unchanged"] = False

        self.assertEqual(online, original_online)
        self.assertEqual(local, original_local)
        self.assertEqual(local["decks"][0]["sents"][0]["extra"]["value"], 1)
        self.assertEqual(local["audio"]["h1-new"]["f"]["n"], "h1n")
        self.assertTrue(online["keep"]["unchanged"])

    def test_merge_rejects_a_requested_deck_missing_locally(self):
        from trainer_storage import merge_selected_decks

        with self.assertRaisesRegex(ValueError, "本地没有 deck：nhsk1"):
            merge_selected_decks(SAMPLE, {"decks": [], "audio": {}}, ["nhsk1"])

    def test_merge_rejects_a_requested_sentence_missing_audio(self):
        from trainer_storage import merge_selected_decks

        local = {"decks": [{"id": "hsk1", "sents": [{"id": "h1-new"}]}], "audio": {}}
        with self.assertRaisesRegex(ValueError, "本地有 1 句没有音频"):
            merge_selected_decks(SAMPLE, local, ["hsk1"])
