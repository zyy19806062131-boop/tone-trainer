import copy
import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "data-source" / "push_deck_to_db.py"
SPEC = importlib.util.spec_from_file_location("push_deck_to_db", MODULE_PATH)
push_deck_to_db = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(push_deck_to_db)


class MergeDecksTest(unittest.TestCase):
    def test_three_deck_merge_preserves_unrelated_data_and_removes_replaced_audio(self):
        online = {
            "_dataVersion": 14,
            "keep": {"unchanged": True},
            "decks": [
                {
                    "id": "hsk1",
                    "name": "Old HSK1",
                    "units": [{"id": "old-unit"}],
                    "sents": [{"id": "old-hsk1-sentence"}],
                },
                {
                    "id": "hsk2",
                    "name": "Unrelated HSK2",
                    "units": [{"id": "legacy-unit"}],
                    "sents": [{"id": "legacy-hsk2-sentence"}],
                },
            ],
            "audio": {
                "old-hsk1-sentence": {"f": {"n": "old-normal", "s": "old-slow"}},
                "legacy-hsk2-sentence": {"f": {"n": "keep-normal", "s": "keep-slow"}},
            },
        }
        local = {
            "decks": [
                {
                    "id": "hsk1",
                    "name": "HSK1",
                    "units": [{"id": "lesson-01"}],
                    "sents": [{"id": "hsk1-new"}],
                },
                {
                    "id": "nhsk1",
                    "name": "新HSK1",
                    "units": [{"id": "lesson-01"}],
                    "sents": [{"id": "nhsk1-new"}],
                },
                {
                    "id": "nhsk2",
                    "name": "新HSK2",
                    "units": [{"id": "lesson-01"}],
                    "sents": [{"id": "nhsk2-new"}],
                },
            ],
            "audio": {
                "hsk1-new": {"f": {"n": "h1-normal", "s": "h1-slow"}},
                "nhsk1-new": {"f": {"n": "nh1-normal", "s": "nh1-slow"}},
                "nhsk2-new": {"f": {"n": "nh2-normal", "s": "nh2-slow"}},
            },
        }
        online_before = copy.deepcopy(online)
        local_before = copy.deepcopy(local)

        merged = push_deck_to_db.merge_decks(
            online,
            local,
            ["hsk1", "nhsk1", "nhsk2"],
        )

        self.assertEqual(
            [deck["id"] for deck in merged["decks"]],
            ["hsk1", "nhsk1", "nhsk2", "hsk2"],
        )
        self.assertEqual(merged["keep"], {"unchanged": True})
        self.assertEqual(
            sorted(merged["audio"]),
            ["hsk1-new", "legacy-hsk2-sentence", "nhsk1-new", "nhsk2-new"],
        )
        self.assertEqual(
            merged["audio"]["legacy-hsk2-sentence"],
            {"f": {"n": "keep-normal", "s": "keep-slow"}},
        )
        self.assertEqual(online, online_before)
        self.assertEqual(local, local_before)

    def test_merge_rejects_a_target_sentence_without_audio(self):
        online = {"decks": [], "audio": {}}
        local = {
            "decks": [
                {
                    "id": "nhsk2",
                    "name": "新HSK2",
                    "units": [{"id": "lesson-01"}],
                    "sents": [{"id": "nhsk2-missing-audio"}],
                }
            ],
            "audio": {},
        }

        with self.assertRaisesRegex(ValueError, "没有音频"):
            push_deck_to_db.merge_decks(online, local, ["nhsk2"])

    def test_merge_rejects_a_requested_deck_missing_from_local_data(self):
        online = {"decks": [], "audio": {}}
        local = {"decks": [], "audio": {}}

        with self.assertRaisesRegex(ValueError, "本地没有 deck"):
            push_deck_to_db.merge_decks(online, local, ["nhsk1"])


class CliArgsTest(unittest.TestCase):
    def test_cli_accepts_three_decks_for_one_merge(self):
        args = push_deck_to_db.parse_args(["hsk1", "nhsk1", "nhsk2"])

        self.assertEqual(args.deck_ids, ["hsk1", "nhsk1", "nhsk2"])
        self.assertFalse(args.apply)


if __name__ == "__main__":
    unittest.main()
