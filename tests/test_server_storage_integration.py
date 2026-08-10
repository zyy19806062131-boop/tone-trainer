import copy
import json
import os
os.environ.setdefault("ADMIN_CODE", "test")

import unittest
from unittest.mock import patch

import server
from trainer_storage import split_trainer_payload


class FakeCursor:
    def __init__(self, responses=(), events=None):
        self.responses = list(responses)
        self.current = []
        self.calls = []
        self.events = events

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def execute(self, sql, params=None):
        normalized = " ".join(sql.split())
        self.calls.append((normalized, params))
        if self.events is not None:
            self.events.append(("query", normalized))
        self.current = self.responses.pop(0) if self.responses else []

    def fetchone(self):
        return self.current[0] if self.current else None

    def fetchall(self):
        return list(self.current)


class FakeConnection:
    def __init__(self, responses=()):
        self.events = []
        self.cursor_obj = FakeCursor(responses, self.events)
        self.commits = 0
        self.set_session_calls = []

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def cursor(self):
        return self.cursor_obj

    def commit(self):
        self.commits += 1

    def set_session(self, **kwargs):
        self.events.append(("set_session", kwargs))
        self.set_session_calls.append(kwargs)


class ConcurrentSameCountCursor:
    def __init__(self, conn):
        self.conn = conn
        self.current = []

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def execute(self, sql, params=None):
        normalized = " ".join(sql.split())
        self.conn.events.append(("query", normalized))
        generation = self.conn.snapshot or self.conn.current_generation
        if "FROM trainer_store_meta" in normalized:
            self.current = [(generation["meta"], 1, 1)]
        elif "FROM trainer_decks" in normalized:
            self.current = [(0, generation["deck_id"], generation["deck"])]
            self.conn.current_generation = self.conn.new_generation
        elif "FROM trainer_audio" in normalized:
            self.current = [
                (generation["sentence_id"], generation["deck_id"], generation["audio"])
            ]
        else:
            raise AssertionError(f"unexpected query: {normalized}")

    def fetchone(self):
        return self.current[0] if self.current else None

    def fetchall(self):
        return list(self.current)


class ConcurrentSameCountConnection:
    def __init__(self):
        self.old_generation = {
            "meta": {"generation": "old"},
            "deck_id": "old-deck",
            "sentence_id": "old-sentence",
            "deck": {
                "id": "old-deck",
                "sents": [{"id": "old-sentence", "zh": "旧句子"}],
            },
            "audio": {"f": {"n": "old-normal", "s": "old-slow"}},
        }
        self.new_generation = {
            "meta": {"generation": "new"},
            "deck_id": "new-deck",
            "sentence_id": "new-sentence",
            "deck": {
                "id": "new-deck",
                "sents": [{"id": "new-sentence", "zh": "新句子"}],
            },
            "audio": {"f": {"n": "new-normal", "s": "new-slow"}},
        }
        self.current_generation = self.old_generation
        self.snapshot = None
        self.events = []

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def cursor(self):
        return ConcurrentSameCountCursor(self)

    def set_session(self, **kwargs):
        if any(event[0] == "query" for event in self.events):
            raise AssertionError("set_session must run before the first query")
        self.events.append(("set_session", kwargs))
        if kwargs == {"isolation_level": "REPEATABLE READ", "readonly": True}:
            self.snapshot = self.current_generation


class TransactionSnapshotCursor:
    def __init__(self, conn):
        self.conn = conn
        self.current = []

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def execute(self, sql, params=None):
        normalized = " ".join(sql.split())
        if "SELECT payload, expected_deck_count, expected_audio_count" in normalized:
            meta = self.conn.state["meta"]
            self.current = [] if meta is None else [
                (meta["payload"], meta["expected_deck_count"], meta["expected_audio_count"])
            ]
        elif "SELECT deck_order, deck_id, payload FROM trainer_decks" in normalized:
            self.current = sorted(copy.deepcopy(self.conn.state["decks"]))
        elif "SELECT sentence_id, deck_id, payload FROM trainer_audio" in normalized:
            self.current = sorted(copy.deepcopy(self.conn.state["audio"]))
        elif normalized.startswith("DELETE FROM trainer_store_meta"):
            self.conn.state["meta"] = None
        elif normalized.startswith("DELETE FROM trainer_audio"):
            self.conn.state["audio"] = []
        elif normalized.startswith("DELETE FROM trainer_decks"):
            self.conn.state["decks"] = []
        elif normalized.startswith("INSERT INTO trainer_store_meta"):
            if self.conn.fail_at == "meta":
                raise RuntimeError("injected meta failure")
            self.conn.state["meta"] = {
                "payload": json.loads(params[0]),
                "expected_deck_count": params[1],
                "expected_audio_count": params[2],
            }
        else:
            self.current = []

    def executemany(self, sql, params):
        rows = list(params)
        if "trainer_decks" in sql:
            if self.conn.fail_at == "decks":
                raise RuntimeError("injected decks failure")
            self.conn.state["decks"] = [
                (deck_order, deck_id, json.loads(payload))
                for deck_id, deck_order, payload in rows
            ]
        elif "trainer_audio" in sql:
            if self.conn.fail_at == "audio":
                raise RuntimeError("injected audio failure")
            self.conn.state["audio"] = [
                (sentence_id, deck_id, json.loads(payload))
                for sentence_id, deck_id, payload in rows
            ]

    def fetchone(self):
        return self.current[0] if self.current else None

    def fetchall(self):
        return list(self.current)


class TransactionSnapshotConnection:
    def __init__(self, payload, *, fail_at):
        rows = split_trainer_payload(payload)
        self.state = {
            "meta": {
                "payload": copy.deepcopy(rows.meta),
                "expected_deck_count": len(rows.decks),
                "expected_audio_count": len(rows.audio),
            },
            "decks": [
                (row.deck_order, row.deck_id, copy.deepcopy(row.payload)) for row in rows.decks
            ],
            "audio": [
                (row.sentence_id, row.deck_id, copy.deepcopy(row.payload)) for row in rows.audio
            ],
        }
        self.fail_at = fail_at
        self.commits = 0
        self.rollbacks = 0
        self.set_session_calls = []
        self._snapshot = None

    def __enter__(self):
        self._snapshot = copy.deepcopy(self.state)
        return self

    def __exit__(self, exc_type, *_):
        if exc_type is not None:
            self.rollback()
        self._snapshot = None
        return False

    def cursor(self):
        return TransactionSnapshotCursor(self)

    def set_session(self, **kwargs):
        self.set_session_calls.append(kwargs)

    def commit(self):
        self.commits += 1
        self._snapshot = copy.deepcopy(self.state)

    def rollback(self):
        self.rollbacks += 1
        self.state = copy.deepcopy(self._snapshot)


class ServerStorageIntegrationTest(unittest.TestCase):
    def test_trainer_load_pins_one_read_only_snapshot_before_same_count_reads(self):
        conn = ConcurrentSameCountConnection()
        expected_old = {
            "generation": "old",
            "decks": [
                {
                    "id": "old-deck",
                    "sents": [{"id": "old-sentence", "zh": "旧句子"}],
                }
            ],
            "audio": {
                "old-sentence": {"f": {"n": "old-normal", "s": "old-slow"}}
            },
        }
        expected_new = {
            "generation": "new",
            "decks": [
                {
                    "id": "new-deck",
                    "sents": [{"id": "new-sentence", "zh": "新句子"}],
                }
            ],
            "audio": {
                "new-sentence": {"f": {"n": "new-normal", "s": "new-slow"}}
            },
        }
        with (
            patch.object(server, "db_enabled", return_value=True),
            patch.object(server, "init_db"),
            patch.object(server, "db_connect", return_value=conn),
        ):
            result = server.load_json(server.DATA_PATH)

        self.assertIn(result, (expected_old, expected_new))
        self.assertEqual(result, expected_old)
        self.assertEqual(
            conn.events[0],
            (
                "set_session",
                {"isolation_level": "REPEATABLE READ", "readonly": True},
            ),
        )

    def test_load_trainer_uses_normalized_payload_without_querying_legacy_row(self):
        conn = FakeConnection()
        normalized = {"decks": [{"id": "hsk1"}], "audio": {}}
        with (
            patch.object(server, "db_enabled", return_value=True),
            patch.object(server, "init_db"),
            patch.object(server, "db_connect", return_value=conn),
            patch.object(server, "load_normalized_trainer_data", return_value=normalized) as load_normalized,
        ):
            self.assertEqual(server.load_json(server.DATA_PATH), normalized)

        load_normalized.assert_called_once_with(conn)
        self.assertEqual(conn.cursor_obj.calls, [])

    def test_load_trainer_falls_back_to_legacy_row_when_normalized_is_inactive(self):
        legacy = {"decks": [{"id": "legacy"}], "audio": {}}
        conn = FakeConnection([[(legacy,)]])
        with (
            patch.object(server, "db_enabled", return_value=True),
            patch.object(server, "init_db"),
            patch.object(server, "db_connect", return_value=conn),
            patch.object(server, "load_normalized_trainer_data", return_value=None) as load_normalized,
        ):
            self.assertEqual(server.load_json(server.DATA_PATH), legacy)

        load_normalized.assert_called_once_with(conn)
        self.assertIn("SELECT payload FROM app_state WHERE key = %s", conn.cursor_obj.calls[0][0])
        self.assertEqual(conn.cursor_obj.calls[0][1], ("trainer_data",))

    def test_absent_normalized_generation_falls_back_on_the_same_pinned_connection(self):
        legacy = {"decks": [{"id": "legacy"}], "audio": {}}
        conn = FakeConnection([[], [(legacy,)]])
        with (
            patch.object(server, "db_enabled", return_value=True),
            patch.object(server, "init_db"),
            patch.object(server, "db_connect", return_value=conn),
        ):
            self.assertEqual(server.load_json(server.DATA_PATH), legacy)

        self.assertEqual(
            conn.events[0],
            (
                "set_session",
                {"isolation_level": "REPEATABLE READ", "readonly": True},
            ),
        )
        self.assertEqual(len(conn.cursor_obj.calls), 2)
        self.assertIn("trainer_store_meta", conn.cursor_obj.calls[0][0])
        self.assertIn("app_state", conn.cursor_obj.calls[1][0])

    def test_incomplete_normalized_generation_falls_back_on_the_same_pinned_connection(self):
        legacy = {"decks": [{"id": "legacy"}], "audio": {}}
        conn = FakeConnection([
            [({"generation": "incomplete"}, 2, 2)],
            [(0, "only-deck", {"id": "only-deck", "sents": []})],
            [("only-audio", None, {"f": {"n": "n", "s": "s"}})],
            [(legacy,)],
        ])
        with (
            patch.object(server, "db_enabled", return_value=True),
            patch.object(server, "init_db"),
            patch.object(server, "db_connect", return_value=conn),
        ):
            self.assertEqual(server.load_json(server.DATA_PATH), legacy)

        self.assertEqual(conn.events[0][0], "set_session")
        self.assertEqual(len(conn.cursor_obj.calls), 4)
        self.assertIn("app_state", conn.cursor_obj.calls[-1][0])

    def test_access_code_load_does_not_request_trainer_snapshot(self):
        access_codes = {"code": {"decks": ["hsk1"]}}
        conn = FakeConnection([[(access_codes,)]])
        with (
            patch.object(server, "db_enabled", return_value=True),
            patch.object(server, "init_db"),
            patch.object(server, "db_connect", return_value=conn),
        ):
            self.assertEqual(server.load_json(server.CODES_PATH), access_codes)

        self.assertEqual(conn.set_session_calls, [])
        self.assertEqual(len(conn.cursor_obj.calls), 1)

    def test_save_trainer_uses_normalized_writer_and_commits(self):
        payload = {"decks": [], "audio": {}}
        conn = FakeConnection()
        with (
            patch.object(server, "db_enabled", return_value=True),
            patch.object(server, "init_db"),
            patch.object(server, "db_connect", return_value=conn),
            patch.object(server, "save_normalized_trainer_data") as save_normalized,
        ):
            server.save_json(server.DATA_PATH, payload)

        save_normalized.assert_called_once_with(conn, payload)
        self.assertEqual(conn.commits, 1)
        self.assertEqual(conn.cursor_obj.calls, [])

    def test_save_codes_keeps_legacy_upsert_without_normalized_writer(self):
        payload = {"code": {"decks": []}}
        conn = FakeConnection()
        with (
            patch.object(server, "db_enabled", return_value=True),
            patch.object(server, "init_db"),
            patch.object(server, "db_connect", return_value=conn),
            patch.object(server, "save_normalized_trainer_data") as save_normalized,
        ):
            server.save_json(server.CODES_PATH, payload)

        save_normalized.assert_not_called()
        self.assertIn("INSERT INTO app_state", conn.cursor_obj.calls[0][0])
        self.assertEqual(conn.cursor_obj.calls[0][1][0], "access_codes")
        self.assertEqual(conn.commits, 1)


class NormalizedTransactionRollbackTest(unittest.TestCase):
    def test_each_normalized_write_failure_rolls_back_to_the_prior_generation(self):
        original = {
            "_dataVersion": 14,
            "keep": "old",
            "decks": [{"id": "old", "sents": [{"id": "old-1"}]}],
            "audio": {"old-1": {"f": {"n": "old-normal", "s": "old-slow"}}},
        }
        replacement = {
            "_dataVersion": 14,
            "keep": "new",
            "decks": [{"id": "new", "sents": [{"id": "new-1"}]}],
            "audio": {"new-1": {"f": {"n": "new-normal", "s": "new-slow"}}},
        }

        for failing_stage in ("decks", "audio", "meta"):
            with self.subTest(failing_stage=failing_stage):
                conn = TransactionSnapshotConnection(original, fail_at=failing_stage)
                with (
                    patch.object(server, "db_enabled", return_value=True),
                    patch.object(server, "init_db"),
                    patch.object(server, "db_connect", return_value=conn),
                ):
                    with self.assertRaisesRegex(RuntimeError, f"injected {failing_stage} failure"):
                        server.save_json(server.DATA_PATH, replacement)

                    self.assertEqual(conn.commits, 0)
                    self.assertEqual(conn.rollbacks, 1)
                    self.assertEqual(server.load_json(server.DATA_PATH), original)
