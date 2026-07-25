#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把编译好的 deck JSON 注入 data/trainer_data.private.json。
同 id 的 deck 原位替换,新 id 追加到末尾;audio 表不动。
用法: python3 data-source/apply_deck.py data-source/hsk1_deck.json
"""
import sys, json
from pathlib import Path

deck_path = Path(sys.argv[1])
data_path = Path(__file__).resolve().parent.parent / 'data' / 'trainer_data.private.json'

deck = json.load(open(deck_path))
data = json.load(open(data_path))

decks = data['decks']
idx = next((i for i, d in enumerate(decks) if d.get('id') == deck['id']), None)
if idx is None:
    decks.append(deck)
    print(f"追加新 deck: {deck['id']} ({len(deck['sents'])} 句)")
else:
    decks[idx] = deck
    print(f"替换 deck: {deck['id']} ({len(deck['sents'])} 句)")

tmp = data_path.with_suffix('.json.tmp')
json.dump(data, open(tmp, 'w'), ensure_ascii=False, indent=1)
tmp.replace(data_path)
print(f"written: {data_path}")
