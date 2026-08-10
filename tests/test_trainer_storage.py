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
        self.assertNotIn("h1-a", merged["audio"])
        self.assertEqual(merged["audio"]["scene-a"], online["audio"]["scene-a"])
        self.assertEqual(merged["audio"]["orphan"], online["audio"]["orphan"])

    def test_merge_rejects_a_requested_deck_missing_locally(self):
        from trainer_storage import merge_selected_decks

        with self.assertRaisesRegex(ValueError, "本地没有 deck：nhsk1"):
            merge_selected_decks(SAMPLE, {"decks": [], "audio": {}}, ["nhsk1"])

    def test_merge_rejects_a_requested_sentence_missing_audio(self):
        from trainer_storage import merge_selected_decks

        local = {"decks": [{"id": "hsk1", "sents": [{"id": "h1-new"}]}], "audio": {}}
        with self.assertRaisesRegex(ValueError, "本地有 1 句没有音频"):
            merge_selected_decks(SAMPLE, local, ["hsk1"])
