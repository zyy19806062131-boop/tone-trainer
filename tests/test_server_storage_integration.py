import os
os.environ.setdefault("ADMIN_CODE", "test")

import unittest
from unittest.mock import patch

import server


class FakeCursor:
    def __init__(self, responses=()):
        self.responses = list(responses)
        self.current = []
        self.calls = []

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def execute(self, sql, params=None):
        self.calls.append((" ".join(sql.split()), params))
        self.current = self.responses.pop(0) if self.responses else []

    def fetchone(self):
        return self.current[0] if self.current else None


class FakeConnection:
    def __init__(self, responses=()):
        self.cursor_obj = FakeCursor(responses)
        self.commits = 0

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def cursor(self):
        return self.cursor_obj

    def commit(self):
        self.commits += 1


class ServerStorageIntegrationTest(unittest.TestCase):
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
