#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""通用 deck 编译器: 课文源(py模块里的 LESSONS) -> 音调训练器 deck JSON。
含全局去重(课内+跨课,同纯汉字句保留首次)。
用法: python3 build_deck.py --source nhsk1_kewen_source --deck-id nhsk1 --name 新HSK1
输出: <deck-id>_deck.json (本目录);再用 apply_deck.py 注入 App 数据。
"""
import sys, json, argparse, importlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from compile_lib import compile_sentence, han

ap = argparse.ArgumentParser()
ap.add_argument('--source', required=True, help='课文源模块名,如 nhsk1_kewen_source')
ap.add_argument('--deck-id', required=True)
ap.add_argument('--name', required=True)
ap.add_argument('--free-units', type=int, default=1, help='前N课免费')
args = ap.parse_args()

LESSONS = importlib.import_module(args.source).LESSONS

deck = {'id': args.deck_id, 'name': args.name, 'full': True, 'hidden': False,
        'units': [], 'sents': []}
errors, dropped = [], []
seen_zh = set()
track_map = {}  # sid -> (音轨名, 句在轨内序号, 轨内句总数) 供切音频用

for li, L in enumerate(LESSONS):
    num = L['id'].split('-')[1]
    deck['units'].append({'id': L['id'], 'name': f"{int(num)} {L['title']}",
                          'hidden': False,
                          'access': 'free' if li < args.free_units else 'paid',
                          'paymentUrl': ''})
    sidx = 0
    for sc in L['scenes']:
        n_in_track = len(sc['sents'])
        for pos, sent in enumerate(sc['sents']):
            zh, py, en = sent[:3]
            opts = sent[3] if len(sent) > 3 else {}
            syl, err = compile_sentence(zh, py)
            if err:
                errors.append(err); continue
            if len(syl) != len(han(zh)):
                errors.append(f"音节数{len(syl)}≠字数{len(han(zh))}: {zh}"); continue
            # 去重键=汉字+数字字母(两句手机号汉字部分相同但号码不同,不能误判重复)
            zh_bare = ''.join(c for c in zh if ('一' <= c <= '鿿') or c.isalnum())
            if zh_bare in seen_zh:
                dropped.append(f"{L['id']} {zh}"); continue
            seen_zh.add(zh_bare)
            sidx += 1
            sid = f"{args.deck_id}-{L['id']}-{sidx:02d}"  # 带deck前缀,防跨deck撞id(音频表全局按id存)
            # zh 保留原句(标点/AI等非汉字照显);声调格只挂汉字(前端 drawContour 已按汉字过滤)
            deck['sents'].append({'id': sid, 'unitId': L['id'],
                                  'zh': zh, 'en': en, 'syl': syl,
                                  'spokenZh': zh})
            if sc.get('track'):
                # opts.clip=(start,end) 绝对时间区间绕过自动切分;
                # opts.sub='head'/'tail' 段内按细静音再切取首/尾子段(去呼语用)
                track_map[sid] = (sc['track'], pos, n_in_track,
                                  opts.get('clip'), opts.get('sub'))

print(f"lessons={len(deck['units'])} sentences={len(deck['sents'])} "
      f"errors={len(errors)} 去重丢弃={len(dropped)}")
for d in dropped: print("  DUP:", d)
for e in errors[:40]: print("  ERR:", e)

out_dir = Path(__file__).resolve().parent
json.dump(deck, open(out_dir / f"{args.deck_id}_deck.json", 'w'),
          ensure_ascii=False, indent=1)
json.dump(track_map, open(out_dir / f"{args.deck_id}_track_map.json", 'w'),
          ensure_ascii=False, indent=1)
print("written:", out_dir / f"{args.deck_id}_deck.json")
print("written:", out_dir / f"{args.deck_id}_track_map.json")

print("\n抽查(每课第1句):")
seen = set()
for s in deck['sents']:
    if s['unitId'] in seen: continue
    seen.add(s['unitId'])
    print(f"  [{s['unitId']}] {s['zh']}")
    print("     ", ' '.join(f"{c['p']}{c['t']}" for c in s['syl']))
