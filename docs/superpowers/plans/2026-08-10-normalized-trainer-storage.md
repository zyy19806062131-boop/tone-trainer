# Normalized Trainer Storage Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在不升级 Render 数据库套餐的前提下，把音调训练器从单行大型 JSONB 改成项目/语音小行存储，并安全恢复旧 HSK1 153 句与新 HSK1 198 句。

**Architecture:** 新建 `trainer_store_meta`、`trainer_decks`、`trainer_audio` 三张表；启用记录不存在或计数异常时，服务端继续读取未改动的旧 `app_state.trainer_data`。兼容代码先上线，之后用小行 CSV 在一个事务内装入 18 个项目和 415 条音频，验证通过后最后写入启用记录。

**Tech Stack:** Python 3、标准库 `unittest`/`csv`/`json`、`psycopg2`、PostgreSQL JSONB、Render CLI、原生 HTML/JavaScript 前端。

## Global Constraints

- 不升级 Render Postgres 套餐，不增加月费。
- 不修改前台布局、访问码、权限含义或管理员操作方式。
- 不覆盖或删除旧 `app_state.trainer_data`；它始终是回退真源。
- 本轮只恢复 `hsk1` 与 `nhsk1`，不启用 `nhsk2`。
- 私有训练 JSON、访问码、连接串、CSV、SQL 和备份不得进入 Git。
- 当前工作树已有他人未提交改动；只编辑和暂存本计划列出的文件，不清理、不回退、不顺手提交其他文件。
- 每个代码任务必须先看到指定测试失败，再写最小实现，再跑回归测试。
- 生产写入前必须再次核对旧行 MD5 `0d9c484c79f558e39d80133e88514f78`；变化即停止。

## File Map

- Create: `trainer_storage.py` — 逻辑数据拆分/重建、目标 deck 合并、规范化表 DDL、读取和写入。
- Modify: `server.py:67-138,271-309` — 启动建表、优先读取规范化数据、规范化事务保存；其余 API 契约不变。
- Create: `tests/test_trainer_storage.py` — 纯数据模型、合并、规范化读取/写入单元测试。
- Create: `tests/test_server_storage_integration.py` — `server.load_json`/`save_json` 的兼容回退与分流测试。
- Create: `data-source/build_normalized_import.py` — 从写前备份和本地成品生成小行 CSV、清单、回滚 SQL、正式 SQL。
- Create: `tests/test_build_normalized_import.py` — 导入包计数、逐行体积、SQL 安全闸测试。
- Create: `docs/operations/2026-08-10-normalized-storage-migration.md` — 实际部署、回读、播放和回退证据。
- Modify: `docs/superpowers/specs/2026-08-09-normalized-trainer-storage-design.md` — 完成后把状态改成“已实施并验收”，并链接操作记录。
- Do not stage: 现有未跟踪的 `data-source/push_deck_to_db.py`、`tests/test_push_deck_to_db.py` 及其他当前脏文件。

---

### Task 1: 纯数据拆分、重建与目标项目合并

**Files:**
- Create: `trainer_storage.py`
- Create: `tests/test_trainer_storage.py`

**Interfaces:**
- Produces: `TrainerRows`, `split_trainer_payload(payload)`, `reconstruct_trainer_payload(rows)`, `merge_selected_decks(online, local, deck_ids)`。
- Consumers: Tasks 2–4 的数据库读写和导入包生成器。

- [ ] **Step 1: 写拆分/重建失败测试**

在 `tests/test_trainer_storage.py` 建立包含两套项目、一个无音频句子、一个孤立音频和额外顶层字段的样本：

```python
import copy
import unittest

from trainer_storage import (
    merge_selected_decks,
    reconstruct_trainer_payload,
    split_trainer_payload,
)


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
```

- [ ] **Step 2: 运行测试并确认因模块不存在而失败**

Run: `ADMIN_CODE=test python3 -m unittest tests.test_trainer_storage.PayloadRowsTest -v`
Expected: FAIL，错误包含 `ModuleNotFoundError: No module named 'trainer_storage'`。

- [ ] **Step 3: 实现最小数据模型**

在 `trainer_storage.py` 写入下列公开类型和逻辑；所有返回值使用深拷贝，不能修改输入：

```python
from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class DeckRow:
    deck_order: int
    deck_id: str
    payload: dict[str, Any]


@dataclass(frozen=True)
class AudioRow:
    sentence_id: str
    deck_id: str | None
    payload: dict[str, Any]


@dataclass(frozen=True)
class TrainerRows:
    meta: dict[str, Any]
    decks: list[DeckRow]
    audio: list[AudioRow]


def split_trainer_payload(payload: dict[str, Any]) -> TrainerRows:
    if not isinstance(payload, dict):
        raise ValueError("训练数据必须是对象")
    decks = payload.get("decks")
    audio = payload.get("audio")
    if not isinstance(decks, list) or not isinstance(audio, dict):
        raise ValueError("训练数据必须包含 decks 数组和 audio 对象")

    seen_decks: set[str] = set()
    sentence_owner: dict[str, str] = {}
    deck_rows: list[DeckRow] = []
    for order, deck in enumerate(decks):
        deck_id = str(deck.get("id", "")).strip()
        if not deck_id:
            raise ValueError("项目 ID 不能为空")
        if deck_id in seen_decks:
            raise ValueError(f"重复项目 ID：{deck_id}")
        seen_decks.add(deck_id)
        for sentence in deck.get("sents", []):
            sentence_id = str(sentence.get("id", "")).strip()
            if not sentence_id:
                raise ValueError(f"{deck_id} 中有空句子 ID")
            if sentence_id in sentence_owner:
                raise ValueError(f"重复句子 ID：{sentence_id}")
            sentence_owner[sentence_id] = deck_id
        deck_rows.append(DeckRow(order, deck_id, copy.deepcopy(deck)))

    audio_rows = [
        AudioRow(str(sentence_id), sentence_owner.get(str(sentence_id)), copy.deepcopy(voices))
        for sentence_id, voices in audio.items()
    ]
    meta = copy.deepcopy({key: value for key, value in payload.items() if key not in {"decks", "audio"}})
    return TrainerRows(meta=meta, decks=deck_rows, audio=audio_rows)


def reconstruct_trainer_payload(rows: TrainerRows) -> dict[str, Any]:
    payload = copy.deepcopy(rows.meta)
    payload["decks"] = [copy.deepcopy(row.payload) for row in sorted(rows.decks, key=lambda item: item.deck_order)]
    payload["audio"] = {row.sentence_id: copy.deepcopy(row.payload) for row in rows.audio}
    return payload
```

- [ ] **Step 4: 写目标项目合并失败测试**

加入三个测试：目标 deck 按指定顺序插回第一个旧目标位置；旧目标独占音频被删除；无关项目/音频/顶层字段逐项不变；目标缺 deck 或缺音频时抛 `ValueError`。

```python
class MergeSelectedDecksTest(unittest.TestCase):
    def test_merge_replaces_targets_and_preserves_unrelated_content(self):
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
```

- [ ] **Step 5: 运行新增测试确认 `merge_selected_decks` 尚未实现**

Run: `ADMIN_CODE=test python3 -m unittest tests.test_trainer_storage.MergeSelectedDecksTest -v`
Expected: FAIL，错误指出 `merge_selected_decks` 不存在或未实现。

- [ ] **Step 6: 实现合并函数并跑全文件测试**

函数必须：去重 `deck_ids` 但保持顺序；验证目标存在及每个目标句子都有音频；删除只属于旧目标项目的旧音频；保留无关和孤立音频；返回深拷贝。

```python
def merge_selected_decks(online, local, deck_ids):
    ordered_ids = list(dict.fromkeys(deck_ids))
    wanted = set(ordered_ids)
    local_by_id = {deck.get("id"): deck for deck in local.get("decks", [])}
    missing_decks = [deck_id for deck_id in ordered_ids if deck_id not in local_by_id]
    if missing_decks:
        raise ValueError("本地没有 deck：" + ", ".join(missing_decks))

    local_audio = local.get("audio", {})
    new_sentence_ids = {
        sentence.get("id")
        for deck_id in ordered_ids
        for sentence in local_by_id[deck_id].get("sents", [])
        if sentence.get("id")
    }
    missing_audio = sorted(sentence_id for sentence_id in new_sentence_ids if sentence_id not in local_audio)
    if missing_audio:
        raise ValueError(f"本地有 {len(missing_audio)} 句没有音频：{missing_audio[:5]}")

    merged = copy.deepcopy(online)
    online_decks = merged.get("decks", [])
    first_target_index = next(
        (index for index, deck in enumerate(online_decks) if deck.get("id") in wanted),
        len(online_decks),
    )
    insertion_index = sum(
        1 for deck in online_decks[:first_target_index] if deck.get("id") not in wanted
    )
    old_target_sentence_ids = {
        sentence.get("id")
        for deck in online_decks if deck.get("id") in wanted
        for sentence in deck.get("sents", []) if sentence.get("id")
    }
    unrelated_decks = [deck for deck in online_decks if deck.get("id") not in wanted]
    unrelated_sentence_ids = {
        sentence.get("id")
        for deck in unrelated_decks
        for sentence in deck.get("sents", []) if sentence.get("id")
    }
    replacements = [copy.deepcopy(local_by_id[deck_id]) for deck_id in ordered_ids]
    merged["decks"] = (
        unrelated_decks[:insertion_index] + replacements + unrelated_decks[insertion_index:]
    )
    merged_audio = merged.setdefault("audio", {})
    for sentence_id in old_target_sentence_ids - new_sentence_ids - unrelated_sentence_ids:
        merged_audio.pop(sentence_id, None)
    for sentence_id in new_sentence_ids:
        merged_audio[sentence_id] = copy.deepcopy(local_audio[sentence_id])
    return merged
```

Run: `ADMIN_CODE=test python3 -m unittest tests.test_trainer_storage -v`
Expected: PASS。

- [ ] **Step 7: 提交 Task 1**

```bash
git add trainer_storage.py tests/test_trainer_storage.py
git commit -m "feat: add normalized trainer payload model" -m "Co-Authored-By: Codex <codex@openai.com>"
```

---

### Task 2: 规范化表结构与安全读取

**Files:**
- Modify: `trainer_storage.py`
- Modify: `tests/test_trainer_storage.py`

**Interfaces:**
- Consumes: `TrainerRows`, `reconstruct_trainer_payload(rows)`。
- Produces: `ensure_normalized_schema(cursor) -> None`, `load_normalized_trainer_data(conn, warn=print) -> dict | None`。
- Consumer: Task 3 的 `server.load_json()`。

- [ ] **Step 1: 写表结构与读取失败测试**

测试使用一个按顺序返回 `fetchone()`/`fetchall()` 结果的 `ScriptedConnection`，记录全部 SQL；覆盖：无启用记录返回 `None`、完整记录重建、项目计数不符时调用 `warn` 并返回 `None`。

```python
class ScriptedCursor:
    def __init__(self, responses):
        self.responses = list(responses)
        self.current = []
        self.calls = []

    def __enter__(self): return self
    def __exit__(self, *_): return False
    def execute(self, sql, params=None):
        self.calls.append(("execute", " ".join(sql.split()), params))
        self.current = self.responses.pop(0) if self.responses else []
    def executemany(self, sql, params):
        self.calls.append(("executemany", " ".join(sql.split()), list(params)))
    def fetchone(self): return self.current[0] if self.current else None
    def fetchall(self): return list(self.current)


class ScriptedConnection:
    def __init__(self, responses): self.cursor_obj = ScriptedCursor(responses)
    def cursor(self): return self.cursor_obj
```

有效读取的脚本结果固定为：

```python
responses = [
    [({"_dataVersion": 14}, 2, 3)],
    [(0, "hsk1", SAMPLE["decks"][0]), (1, "scene", SAMPLE["decks"][1])],
    [(sid, None if sid == "orphan" else ("hsk1" if sid == "h1-a" else "scene"), voices)
     for sid, voices in SAMPLE["audio"].items()],
]
```

- [ ] **Step 2: 运行读取测试确认函数不存在**

Run: `ADMIN_CODE=test python3 -m unittest tests.test_trainer_storage.NormalizedReadTest -v`
Expected: FAIL，错误指出读取函数不存在。

- [ ] **Step 3: 实现 DDL 与读取**

`ensure_normalized_schema()` 依次执行三条 `CREATE TABLE IF NOT EXISTS` 和 `trainer_audio(deck_id)` 索引；字段必须与设计文档完全一致。`load_normalized_trainer_data()` 的查询顺序固定为 meta→decks→audio：

```python
NORMALIZED_SCHEMA_SQL = (
    """
    CREATE TABLE IF NOT EXISTS trainer_store_meta (
        id SMALLINT PRIMARY KEY CHECK (id = 1),
        payload JSONB NOT NULL,
        expected_deck_count INTEGER NOT NULL,
        expected_audio_count INTEGER NOT NULL,
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS trainer_decks (
        deck_id TEXT PRIMARY KEY,
        deck_order INTEGER UNIQUE NOT NULL,
        payload JSONB NOT NULL,
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS trainer_audio (
        sentence_id TEXT PRIMARY KEY,
        deck_id TEXT NULL,
        payload JSONB NOT NULL,
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    )
    """,
    "CREATE INDEX IF NOT EXISTS trainer_audio_deck_id_idx ON trainer_audio(deck_id)",
)


def ensure_normalized_schema(cursor):
    for statement in NORMALIZED_SCHEMA_SQL:
        cursor.execute(statement)
```

读取实现：

```python
def load_normalized_trainer_data(conn, warn=print):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT payload, expected_deck_count, expected_audio_count "
            "FROM trainer_store_meta WHERE id = 1"
        )
        meta_row = cur.fetchone()
        if not meta_row:
            return None
        meta, expected_decks, expected_audio = meta_row
        cur.execute("SELECT deck_order, deck_id, payload FROM trainer_decks ORDER BY deck_order")
        deck_rows = [DeckRow(order, deck_id, _json_value(payload)) for order, deck_id, payload in cur.fetchall()]
        cur.execute("SELECT sentence_id, deck_id, payload FROM trainer_audio ORDER BY sentence_id")
        audio_rows = [AudioRow(sentence_id, deck_id, _json_value(payload)) for sentence_id, deck_id, payload in cur.fetchall()]
    if len(deck_rows) != expected_decks or len(audio_rows) != expected_audio:
        warn(
            "[warn] 规范化训练数据不完整，退回旧 app_state："
            f"decks {len(deck_rows)}/{expected_decks}, audio {len(audio_rows)}/{expected_audio}"
        )
        return None
    return reconstruct_trainer_payload(TrainerRows(_json_value(meta), deck_rows, audio_rows))
```

`_json_value()` 接受 psycopg2 已解码的 `dict/list` 或 JSON 字符串，其他类型抛 `ValueError`。

- [ ] **Step 4: 跑读取测试和 Task 1 回归**

Run: `ADMIN_CODE=test python3 -m unittest tests.test_trainer_storage -v`
Expected: PASS。

- [ ] **Step 5: 提交 Task 2**

```bash
git add trainer_storage.py tests/test_trainer_storage.py
git commit -m "feat: read normalized trainer rows safely" -m "Co-Authored-By: Codex <codex@openai.com>"
```

---

### Task 3: 原子写入与服务端兼容分流

**Files:**
- Modify: `trainer_storage.py`
- Modify: `server.py:67-138,271-309`
- Modify: `tests/test_trainer_storage.py`
- Create: `tests/test_server_storage_integration.py`

**Interfaces:**
- Consumes: `split_trainer_payload()`, `ensure_normalized_schema()`, `load_normalized_trainer_data()`。
- Produces: `save_normalized_trainer_data(conn, payload) -> None`；`server.load_json()` 和 `save_json()` 保持原签名。

- [ ] **Step 1: 写原子写入失败测试**

测试 `save_normalized_trainer_data()` 的 SQL 调用必须满足：先取得事务级 advisory lock；删除旧 meta/audio/decks；逐行 `executemany` 项目与音频；最后写 meta；音频参数包含孤立音频的 `deck_id=None`；任何参数都不是完整 `SAMPLE` 的单个 JSON。

```python
def test_save_uses_small_rows_and_writes_meta_last(self):
    conn = ScriptedConnection([])
    save_normalized_trainer_data(conn, SAMPLE)
    calls = conn.cursor_obj.calls
    sql_text = [call[1] for call in calls]
    self.assertIn("pg_advisory_xact_lock", sql_text[0])
    self.assertIn("DELETE FROM trainer_store_meta", " ".join(sql_text))
    self.assertIn("DELETE FROM trainer_audio", " ".join(sql_text))
    self.assertIn("DELETE FROM trainer_decks", " ".join(sql_text))
    self.assertIn("INSERT INTO trainer_store_meta", sql_text[-1])
    audio_call = next(call for call in calls if call[0] == "executemany" and "trainer_audio" in call[1])
    orphan = next(params for params in audio_call[2] if params[0] == "orphan")
    self.assertIsNone(orphan[1])
```

- [ ] **Step 2: 运行写入测试确认失败**

Run: `ADMIN_CODE=test python3 -m unittest tests.test_trainer_storage.NormalizedWriteTest -v`
Expected: FAIL，错误指出写入函数不存在。

- [ ] **Step 3: 实现原子小行写入**

实现固定顺序，函数不自行 `commit`，由调用者控制事务：

```python
TRAINER_ADVISORY_LOCK = 824_202_608


def save_normalized_trainer_data(conn, payload):
    rows = split_trainer_payload(payload)
    with conn.cursor() as cur:
        cur.execute("SELECT pg_advisory_xact_lock(%s)", (TRAINER_ADVISORY_LOCK,))
        ensure_normalized_schema(cur)
        cur.execute("DELETE FROM trainer_store_meta WHERE id = 1")
        cur.execute("DELETE FROM trainer_audio")
        cur.execute("DELETE FROM trainer_decks")
        cur.executemany(
            "INSERT INTO trainer_decks(deck_id, deck_order, payload, updated_at) "
            "VALUES (%s, %s, %s::jsonb, NOW())",
            [(row.deck_id, row.deck_order, json.dumps(row.payload, ensure_ascii=False)) for row in rows.decks],
        )
        cur.executemany(
            "INSERT INTO trainer_audio(sentence_id, deck_id, payload, updated_at) "
            "VALUES (%s, %s, %s::jsonb, NOW())",
            [(row.sentence_id, row.deck_id, json.dumps(row.payload, ensure_ascii=False)) for row in rows.audio],
        )
        cur.execute(
            "INSERT INTO trainer_store_meta(id, payload, expected_deck_count, expected_audio_count, updated_at) "
            "VALUES (1, %s::jsonb, %s, %s, NOW())",
            (json.dumps(rows.meta, ensure_ascii=False), len(rows.decks), len(rows.audio)),
        )
```

- [ ] **Step 4: 写服务端分流失败测试**

在测试导入 `server` 前设置 `ADMIN_CODE=test`。使用 `unittest.mock.patch` 验证：

1. `load_json(DATA_PATH)` 在规范化读取返回对象时不查询旧行。
2. 规范化读取返回 `None` 时查询并返回旧 `app_state` 行。
3. `save_json(DATA_PATH, payload)` 调用 `save_normalized_trainer_data()` 并 `commit()`。
4. `save_json(CODES_PATH, payload)` 仍走原 `app_state` UPSERT，不调用规范化写入。

- [ ] **Step 5: 运行服务端测试确认旧代码不识别规范化存储**

Run: `ADMIN_CODE=test python3 -m unittest tests.test_server_storage_integration -v`
Expected: FAIL，至少一个断言表明 `load_json` 未调用规范化读取或 `save_json` 仍写单行 `trainer_data`。

- [ ] **Step 6: 接入 `server.py`**

修改点必须局限在：

- 文件顶部导入 `ensure_normalized_schema`、`load_normalized_trainer_data`、`save_normalized_trainer_data`。
- `init_db()` 创建 `app_state` 后调用 `ensure_normalized_schema(cur)`；空表不写 meta。
- `load_json()` 对 `trainer_data` 先调用规范化读取，返回 `None` 才查旧 `app_state`。
- `save_json()` 对 `trainer_data` 调用规范化写入并提交；`access_codes` 保持旧 UPSERT。

不要改 `build_payload()`、API 路由或前端。

`load_json()` 的数据库分支使用同一连接完成新表检查和旧行回退：

```python
if key and db_enabled():
    init_db()
    with db_connect() as conn:
        if key == "trainer_data":
            normalized = load_normalized_trainer_data(conn)
            if normalized is not None:
                return normalized
        with conn.cursor() as cur:
            cur.execute("SELECT payload FROM app_state WHERE key = %s", (key,))
            row = cur.fetchone()
    if row:
        return normalize_db_payload(row[0])
```

`save_json()` 在现有 `if key and db_enabled()` 分支最前面分流：

```python
if key == "trainer_data":
    with db_connect() as conn:
        save_normalized_trainer_data(conn, payload)
        conn.commit()
    return
```

`init_db()` 在创建 `app_state` 的同一 cursor 内调用 `ensure_normalized_schema(cur)`，但不写 `trainer_store_meta`。

- [ ] **Step 7: 跑所有存储测试和语法检查**

Run: `ADMIN_CODE=test python3 -m unittest tests.test_trainer_storage tests.test_server_storage_integration -v`
Expected: PASS。
Run: `python3 -m py_compile server.py trainer_storage.py`
Expected: exit 0。

- [ ] **Step 8: 提交 Task 3**

```bash
git add trainer_storage.py server.py tests/test_trainer_storage.py tests/test_server_storage_integration.py
git commit -m "feat: store trainer data in normalized rows" -m "Co-Authored-By: Codex <codex@openai.com>"
```

---

### Task 4: 生成可审计的小行导入包

**Files:**
- Create: `data-source/build_normalized_import.py`
- Create: `tests/test_build_normalized_import.py`

**Interfaces:**
- Consumes: `merge_selected_decks()`, `split_trainer_payload()`, `TRAINER_ADVISORY_LOCK`。
- Produces: `build_bundle(online, local, deck_ids, out_dir, expected_online_md5) -> dict`，以及 CLI 生成 `meta.csv`、`decks.csv`、`audio.csv`、`manifest.json`、`check.sql`、`apply.sql`。

- [ ] **Step 1: 写导入包失败测试**

用 `tempfile.TemporaryDirectory()` 和 Task 1 的样本验证：

```python
import csv
import importlib.util
import tempfile
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "data-source" / "build_normalized_import.py"
SPEC = importlib.util.spec_from_file_location("build_normalized_import", MODULE_PATH)
build_normalized_import = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(build_normalized_import)
build_bundle = build_normalized_import.build_bundle


def test_bundle_uses_small_rows_and_two_safe_sql_files(self):
    with tempfile.TemporaryDirectory() as tmp:
        manifest = build_bundle(online, local, ["hsk1", "nhsk1"], Path(tmp), "abc123")
        self.assertEqual(manifest["deckCount"], 3)
        self.assertEqual(manifest["audioCount"], 4)
        self.assertEqual(manifest["targets"], {"hsk1": 1, "nhsk1": 1})
        self.assertEqual(sum(1 for _ in csv.reader((Path(tmp) / "decks.csv").open())), 3)
        self.assertEqual(sum(1 for _ in csv.reader((Path(tmp) / "audio.csv").open())), 4)
        self.assertLess(manifest["maxJsonCellBytes"], 2_000_000)
        check_sql = (Path(tmp) / "check.sql").read_text()
        apply_sql = (Path(tmp) / "apply.sql").read_text()
        self.assertIn("ROLLBACK;", check_sql)
        self.assertNotIn("COMMIT;", check_sql)
        self.assertIn("COMMIT;", apply_sql)
        self.assertIn("md5(payload::text)", apply_sql)
        self.assertIn("abc123", apply_sql)
        self.assertIn("INSERT INTO trainer_store_meta", apply_sql)
```

另写两条拒绝测试：`expected_online_md5` 不是 32 位十六进制；任一 JSON 单元格达到 2,000,000 bytes。

- [ ] **Step 2: 运行测试确认生成器不存在**

Run: `ADMIN_CODE=test python3 -m unittest tests.test_build_normalized_import -v`
Expected: FAIL，错误包含文件或模块不存在。

- [ ] **Step 3: 实现 CSV 与清单生成**

`build_bundle()` 必须执行以下固定步骤：

```python
merged = merge_selected_decks(online, local, deck_ids)
rows = split_trainer_payload(merged)
targets = {
    deck_id: len(next(row.payload for row in rows.decks if row.deck_id == deck_id)["sents"])
    for deck_id in dict.fromkeys(deck_ids)
}
```

- `meta.csv`：一行三列，`json.dumps(rows.meta)`、项目数、音频数。
- `decks.csv`：每项目一行，顺序、项目 ID、该项目 JSON。
- `audio.csv`：每音频一行，句子 ID、可空项目 ID、该句音频 JSON。
- `manifest.json`：只含计数、目标句数、每个文件 SHA-256、最大 JSON 单元格字节数，不含访问码和音频正文。
- 任一 JSON 单元格 `>=2_000_000` bytes 时抛错，防止重新制造大行。

CLI 使用下列参数，`--deck` 可重复且至少一个；默认只生成文件，不连接数据库：

```python
import argparse
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from trainer_storage import (
    TRAINER_ADVISORY_LOCK,
    merge_selected_decks,
    split_trainer_payload,
)


def parse_args(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--online-json", type=Path, required=True)
    parser.add_argument("--local-json", type=Path, required=True)
    parser.add_argument("--deck", action="append", required=True)
    parser.add_argument("--expected-online-md5", required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    return parser.parse_args(argv)
```

- [ ] **Step 4: 实现回滚/正式 SQL 模板**

两个 SQL 文件内容相同，只有结尾分别为 `ROLLBACK;` 与 `COMMIT;`。模板必须依次执行：

1. `\set ON_ERROR_STOP on`、`BEGIN`、`SELECT pg_advisory_xact_lock(824202608)`。
2. 建三个临时 staging 表并用绝对路径 `\copy` 读取三个 CSV。
3. 断言 staging 行数等于 manifest，项目顺序与 ID 唯一。
4. 断言旧 `app_state.trainer_data` 的 `md5(payload::text)` 等于参数值。
5. 删除 `trainer_store_meta`、`trainer_audio`、`trainer_decks` 的旧规范化行。
6. 从 staging 小行插入 `trainer_decks` 和 `trainer_audio`。
7. 断言插入行与 staging 逐行 JSONB 相等，目标 `hsk1`/`nhsk1` 句数正确且每句都有 `f.n`/`f.s`。
8. 最后插入 `trainer_store_meta(id=1)`。
9. 再断言 meta 期望计数与实际表计数一致。
10. `check.sql` 回滚；`apply.sql` 提交，并在提交后只输出计数和更新时间，不输出音频或访问码。

模板的核心 SQL 必须是明确的小行复制与逐行相等检查，不允许出现 `%s::jsonb` 的整包参数：

```sql
\set ON_ERROR_STOP on
BEGIN;
SELECT pg_advisory_xact_lock(824202608);

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

\copy stage_meta(payload, expected_deck_count, expected_audio_count) FROM '{meta_csv_sql}' WITH (FORMAT csv, ENCODING 'UTF8')
\copy stage_decks(deck_order, deck_id, payload) FROM '{decks_csv_sql}' WITH (FORMAT csv, ENCODING 'UTF8')
\copy stage_audio(sentence_id, deck_id, payload) FROM '{audio_csv_sql}' WITH (FORMAT csv, ENCODING 'UTF8')

DO $guard$
BEGIN
    IF (SELECT md5(payload::text) FROM app_state WHERE key='trainer_data')
       <> '{expected_online_md5}' THEN
        RAISE EXCEPTION 'legacy trainer_data changed after backup';
    END IF;
    IF (SELECT count(*) FROM stage_decks) <> {deck_count}
       OR (SELECT count(*) FROM stage_audio) <> {audio_count} THEN
        RAISE EXCEPTION 'staging counts do not match manifest';
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
    IF (SELECT jsonb_array_length(payload->'sents') FROM trainer_decks WHERE deck_id='hsk1') <> 153
       OR (SELECT jsonb_array_length(payload->'sents') FROM trainer_decks WHERE deck_id='nhsk1') <> 198 THEN
        RAISE EXCEPTION 'target sentence counts differ';
    END IF;
    IF (SELECT count(*)
        FROM trainer_decks d,
             LATERAL jsonb_array_elements(d.payload->'sents') sentence
        JOIN trainer_audio a ON a.sentence_id = sentence->>'id'
        WHERE d.deck_id IN ('hsk1', 'nhsk1')
          AND a.payload->'f' ? 'n'
          AND a.payload->'f' ? 's') <> 351 THEN
        RAISE EXCEPTION 'target audio completeness differs';
    END IF;
END
$verify$;

INSERT INTO trainer_store_meta(id, payload, expected_deck_count, expected_audio_count, updated_at)
SELECT 1, payload, expected_deck_count, expected_audio_count, NOW() FROM stage_meta;

{transaction_end}
```

上述 SQL 放在 Python f-string 中；生成器先验证 MD5 格式和整数计数，再插入数值，并对三个绝对路径中的单引号做 SQL 转义。生成 `check.sql` 时 `transaction_end="ROLLBACK;"`；生成 `apply.sql` 时 `transaction_end` 为 `COMMIT;` 加三张规范化表的只读计数查询。

- [ ] **Step 5: 跑生成器测试、全套单元测试和语法检查**

Run: `ADMIN_CODE=test python3 -m unittest discover -s tests -v`
Expected: 所有本轮测试 PASS；如果工作树中的旧未跟踪测试被 discover 到，也必须单独报告其归属，不能删掉。
Run: `python3 -m py_compile data-source/build_normalized_import.py`
Expected: exit 0。

- [ ] **Step 6: 提交 Task 4**

```bash
git add data-source/build_normalized_import.py tests/test_build_normalized_import.py
git commit -m "feat: build safe normalized import bundles" -m "Co-Authored-By: Codex <codex@openai.com>"
```

---

### Task 5: 本地全量预检并部署兼容代码

**Files:**
- No source changes expected.
- Generated private artifacts: `backups/normalized-hsk1-20260810/`（Git 忽略）。

**Interfaces:**
- Consumes: Tasks 1–4 的全部代码。
- Produces: 已部署但尚未启用的新表兼容代码；线上仍显示旧数据。

- [ ] **Step 1: 跑新鲜全套验证**

Run: `ADMIN_CODE=test python3 -m unittest discover -s tests -v`
Expected: 本轮测试全部 PASS。
Run: `python3 -m py_compile server.py trainer_storage.py data-source/build_normalized_import.py`
Expected: exit 0。
Run: `git diff --check`
Expected: 本轮文件无空白错误；若其他脏文件已有错误，按路径分开报告，不修改它们。

- [ ] **Step 2: 用真实写前备份生成两版 HSK1 私有导入包**

```bash
python3 data-source/build_normalized_import.py \
  --online-json backups/线上_trainer_data_写前_20260809-194327.json \
  --local-json data/trainer_data.private.json \
  --deck hsk1 --deck nhsk1 \
  --expected-online-md5 0d9c484c79f558e39d80133e88514f78 \
  --out-dir backups/normalized-hsk1-20260810
```

Expected manifest: `deckCount=18`、`audioCount=415`、`targets.hsk1=153`、`targets.nhsk1=198`；最大 JSON 单元格小于 2,000,000 bytes。

- [ ] **Step 3: 核对私有产物未进入 Git**

Run: `git status --short --ignored backups/normalized-hsk1-20260810`
Expected: 所有生成文件标记为 ignored；没有 `??` 或 staged 文件。

- [ ] **Step 4: 推送代码提交**

Run: `git status --short`，逐项确认 staged 为空且未提交脏文件仍是原来的文件。
Run: `git push origin main`。
Expected: origin/main 前进到本轮最后一个代码提交；Render 自动开始部署。

- [ ] **Step 5: 等待 Render 兼容代码部署成功**

Run: `render deploys list srv-d8g4504p3tds73cb8eog --output json`，每次使用最新游标/状态，直到本轮 commit 为 `live` 或明确失败。
Run: `render logs --resources srv-d8g4504p3tds73cb8eog --limit 100 --output text`。
Expected: 服务启动成功，三张表创建无错误，无 signal 9/数据库重启。

- [ ] **Step 6: 在未启用状态验证旧线上仍可用**

Run:

```sql
SELECT count(*) FROM trainer_store_meta;
SELECT count(*) FROM trainer_decks;
SELECT count(*) FROM trainer_audio;
SELECT updated_at, md5(payload::text) FROM app_state WHERE key='trainer_data';
```

通过 `render psql tone-trainer-db` 执行。Expected: 三张规范化表计数均为 0；旧行 MD5 仍为 `0d9c...`。
Run: `curl -L --max-time 30 -sS -o /dev/null -w '%{http_code}\n' https://tone-trainer.onrender.com/`。
Expected: `200`。使用本机私密访问码登录一次，仍看到旧线上状态；不得在输出中打印访问码。

---

### Task 6: 回滚演练、正式启用与真实播放验收

**Files:**
- Generated private SQL/CSV only; no Git changes during database write.

**Interfaces:**
- Consumes: `backups/normalized-hsk1-20260810/check.sql` 和 `apply.sql`。
- Produces: 线上启用的 18 项/415 音频规范化数据，旧单行备份保持不变。

- [ ] **Step 1: 执行只回滚演练**

Run:

```bash
PATH="/opt/homebrew/opt/libpq/bin:$PATH" \
render psql tone-trainer-db --command \
"\i /Users/a1/Claude/repos/tone-trainer/backups/normalized-hsk1-20260810/check.sql"
```

Expected: staging、逐行插入、目标音频验证全部通过，最终明确 `ROLLBACK`，连接不被杀死。

- [ ] **Step 2: 演练后确认正式状态完全未变**

Expected: `trainer_store_meta/decks/audio` 均为 0；旧行 MD5、17 项、184 音频不变；站点 HTTP 200。

- [ ] **Step 3: 执行正式单事务启用**

重新核对旧行 MD5 后运行：

```bash
PATH="/opt/homebrew/opt/libpq/bin:$PATH" \
render psql tone-trainer-db --command \
"\i /Users/a1/Claude/repos/tone-trainer/backups/normalized-hsk1-20260810/apply.sql"
```

Expected: `COMMIT`；输出只显示 meta=1、decks=18、audio=415 和更新时间。

- [ ] **Step 4: 数据库与 API 回读**

数据库必须同时满足：

- `trainer_store_meta=1`、`trainer_decks=18`、`trainer_audio=415`。
- `trainer_decks.hsk1.sents=153`、`trainer_decks.nhsk1.sents=198`。
- 351 个目标句子各自都有 `trainer_audio` 行，且 `payload->'f'` 同时有 `n` 和 `s`。
- 旧 `app_state.trainer_data` 的更新时间与 MD5 不变。

用本机私密全权限访问码 POST `/api/login`，脚本只打印目标项目句数和目标音频匹配数。Expected: 两个目标项目存在；153/198 句全部在响应的 `audio` 中；不打印访问码或 base64。

- [ ] **Step 5: 真实页面播放至少 12 次**

使用 Chrome 现有登录状态或从私密文件读取全权限码：

1. 进入旧 HSK1，分别选首句、中间句、末句；每句播放原速和慢速。
2. 进入新 HSK1，做同样六次播放。
3. 每次确认声音真实开始、控制台无音频错误、页面不出现 `No embedded audio` 或 `Using fallback voice`。
4. 管理后台确认两套项目均出现；访问码配置数量和权限摘要不变。

- [ ] **Step 6: 只读验证回退开关**

在一个 `BEGIN ... ROLLBACK` 事务内临时删除 `trainer_store_meta WHERE id=1`，查询确认规范化启用记录为 0，然后回滚；事务外再次确认 meta=1。不要让网页请求参与这个瞬时事务。

- [ ] **Step 7: 若任何验收失败，执行预定回退**

只在失败时执行一个短事务删除 `trainer_store_meta WHERE id=1` 并提交；随后验证页面退回旧 17 项状态、旧行 MD5 不变。保留新表数据供核查，不删除项目/音频行。若全部通过，不执行此步骤。

---

### Task 7: 操作记录、最终回归与交付

**Files:**
- Create: `docs/operations/2026-08-10-normalized-storage-migration.md`
- Modify: `docs/superpowers/specs/2026-08-09-normalized-trainer-storage-design.md`
- Update outside repo: `/Users/a1/Claude/当前行动台账.md`

**Interfaces:**
- Consumes: Task 6 的实际命令时间、提交号、数据库计数和播放结果。
- Produces: 可交接的部署证据与未完成边界。

- [ ] **Step 1: 写实际操作记录**

记录以下已发生事实，不复制私密数据：代码 commit、Render deploy ID/状态、旧行 MD5 是否保持、规范化三表计数、两版句数、目标音频完整率、12 次播放结果、回退开关演练结果。若某项未通过，明确写 `INCOMPLETE` 和当前回退状态。

- [ ] **Step 2: 更新设计状态与行动台账**

设计文档顶部状态只在所有验收通过后改为“已实施并验收”，并链接操作记录。台账 K23–K26 更新为最终事实；`nhsk2` 仍标为未上线和待做浏览器响应体积测试。

- [ ] **Step 3: 运行完成前验证技能和全套命令**

Required sub-skill: `superpowers:verification-before-completion`。

Run: `ADMIN_CODE=test python3 -m unittest discover -s tests -v`。
Run: `python3 -m py_compile server.py trainer_storage.py data-source/build_normalized_import.py`。
Run: `git diff --check -- trainer_storage.py server.py tests/test_trainer_storage.py tests/test_server_storage_integration.py data-source/build_normalized_import.py tests/test_build_normalized_import.py docs/operations/2026-08-10-normalized-storage-migration.md docs/superpowers/specs/2026-08-09-normalized-trainer-storage-design.md`。
Expected: 本轮测试和检查全部通过；生产回读仍是 meta=1/decks=18/audio=415。

- [ ] **Step 4: 提交并推送操作记录**

```bash
git add docs/operations/2026-08-10-normalized-storage-migration.md \
  docs/superpowers/specs/2026-08-09-normalized-trainer-storage-design.md
git commit -m "docs: record normalized trainer migration" -m "Co-Authored-By: Codex <codex@openai.com>"
git push origin main
```

- [ ] **Step 5: 最终工作树边界检查**

Run: `git status --short`。
Expected: 只剩开工前已经存在、且本轮未暂存的他人改动；列明但不修改。最终回复只报告实际完成项、真实线上状态、回退位置和新 HSK2 的未上线边界。
