#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给已配音频的句子生成字级时间戳(字随声亮)。
对每句的正常速 clip 跑 faster-whisper(word_timestamps),把识别字与课文汉字
difflib 对齐,缺口线性插值,写入句子 'ts': [[start,end],...] (与 syl 对齐,秒)。
慢速版无需另存:前端按 音频时长/正常时长 比例缩放。
用法: python3 add_char_timings.py [--deck hsk1] [--force]
缓存: char_ts_cache.json (键=sid:clip字节数)
"""
import json, argparse, base64, tempfile, difflib, sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('--deck', action='append', default=[])
ap.add_argument('--force', action='store_true')
args = ap.parse_args()

here = Path(__file__).resolve().parent
data_path = here.parent / 'data' / 'trainer_data.private.json'
cache_path = here / 'char_ts_cache.json'
cache = json.load(open(cache_path)) if cache_path.exists() else {}

def hanzi(s): return [c for c in s if '一' <= c <= '鿿']

_model = None
def transcribe_chars(mp3_bytes):
    """clip -> [(char,start,end)] 识别字符流(词内均分时长)"""
    global _model
    if _model is None:
        from faster_whisper import WhisperModel
        _model = WhisperModel('small', device='cpu', compute_type='int8')
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
        f.write(mp3_bytes); tmp = Path(f.name)
    segs, _ = _model.transcribe(str(tmp), language='zh', beam_size=3,
                                word_timestamps=True,
                                initial_prompt='汉语教材课文录音,普通话。')
    out = []
    for seg in segs:
        for w in (seg.words or []):
            chars = hanzi(w.word)
            if not chars: continue
            step = (w.end - w.start) / len(chars)
            for i, c in enumerate(chars):
                out.append((c, w.start + i*step, w.start + (i+1)*step))
    tmp.unlink()
    return out

def align_ts(expected, rec):
    """把识别字符时间对齐到期望汉字;未匹配处线性插值。返回 [[s,e],...]"""
    n = len(expected)
    ts = [None]*n
    sm = difflib.SequenceMatcher(None, expected, [c for c,_,_ in rec])
    for op, a1, a2, b1, b2 in sm.get_opcodes():
        if op == 'equal':
            for k in range(a2-a1):
                ts[a1+k] = [rec[b1+k][1], rec[b1+k][2]]
    # 插值补洞: 用前后已知锚点均分
    total = rec[-1][2] if rec else None
    i = 0
    while i < n:
        if ts[i] is not None: i += 1; continue
        j = i
        while j < n and ts[j] is None: j += 1
        left = ts[i-1][1] if i > 0 else 0.0
        right = ts[j][0] if j < n else (total if total else left + 0.4*(j-i))
        if right <= left: right = left + 0.3*(j-i)
        step = (right-left)/(j-i)
        for k in range(j-i):
            ts[i+k] = [left+k*step, left+(k+1)*step]
        i = j
    # 单调化
    for k in range(1, n):
        if ts[k][0] < ts[k-1][1]-0.01: ts[k][0] = ts[k-1][1]
        if ts[k][1] < ts[k][0]: ts[k][1] = ts[k][0]+0.15
    return [[round(a,2), round(b,2)] for a,b in ts]

data = json.load(open(data_path))
audio = data.get('audio', {})
done = skip = 0
for deck in data['decks']:
    if args.deck and deck['id'] not in args.deck: continue
    for s in deck['sents']:
        clip = audio.get(s['id'], {}).get('f', {}).get('n')
        if not clip: continue
        if 'ts' in s and not args.force: skip += 1; continue
        raw = base64.b64decode(clip.split(',', 1)[1])
        key = f"{s['id']}:{len(raw)}"
        if key in cache:
            rec = [tuple(x) for x in cache[key]]
        else:
            rec = transcribe_chars(raw)
            cache[key] = rec
            json.dump(cache, open(cache_path, 'w'), ensure_ascii=False)
        exp = hanzi(s['zh'])
        if not rec:
            print(f"WARN 无识别 {s['id']} {s['zh']}"); continue
        s['ts'] = align_ts(exp, rec)
        matched = sum(1 for op,a1,a2,_,_ in difflib.SequenceMatcher(
            None, exp, [c for c,_,_ in rec]).get_opcodes() if op=='equal' for _ in range(a2-a1))
        print(f"ok {s['id']} {s['zh']}  锚点{matched}/{len(exp)}")
        done += 1

tmp = data_path.with_suffix('.json.tmp')
json.dump(data, open(tmp, 'w'), ensure_ascii=False, indent=1)
tmp.replace(data_path)
print(f"done: {done} sentences, {skip} skipped(已有ts)")
