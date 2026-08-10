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


def merge_selected_decks(
    online: dict[str, Any], local: dict[str, Any], deck_ids: list[str]
) -> dict[str, Any]:
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
