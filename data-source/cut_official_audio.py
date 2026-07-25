#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把官方配套音频按长静音切成逐句 clip,注入 App 数据的 audio 表。
原理: 句间停顿≥GAP秒,句内逗号停顿≈0.5秒,故按长静音切分;段数必须==该轨句数,不等即报错跳过(不硬切)。
每句生成 n(原声原速) + s(原声 atempo 慢速);挂在 'f' 键(App 默认音色槽位)。
用法: python3 cut_official_audio.py --deck nhsk1 --audio-dir <官方音频目录>
依赖 <deck>_track_map.json (build_deck.py 产出)。
"""
import json, argparse, base64, subprocess, re, tempfile
from pathlib import Path

GAP = 0.8          # 句间静音阈值(秒)
NOISE = '-35dB'
SLOW_TEMPO = 0.7   # 慢速版速率

ap = argparse.ArgumentParser()
ap.add_argument('--deck', required=True)
ap.add_argument('--audio-dir', required=True)
ap.add_argument('--dry-run', action='store_true', help='只报切分结果不写数据')
args = ap.parse_args()

here = Path(__file__).resolve().parent
data_path = here.parent / 'data' / 'trainer_data.private.json'
track_map = json.load(open(here / f"{args.deck}_track_map.json"))
audio_dir = Path(args.audio_dir)

# track -> [(sid, pos, clip, sub)] 按轨内序号排; clip=手工区间, sub=head/tail 细切
by_track = {}
for sid, entry in track_map.items():
    track, pos, total = entry[0], entry[1], entry[2]
    clip = entry[3] if len(entry) > 3 else None
    sub = entry[4] if len(entry) > 4 else None
    by_track.setdefault(track, {'total': total, 'sents': []})
    by_track[track]['sents'].append((pos, sid, clip, sub))

def fine_subseg(mp3, a, b, which):
    """在 [a,b] 内按细静音(≥0.3s)切,取首/尾语音子段"""
    out = subprocess.run(['ffmpeg', '-ss', f'{a:.3f}', '-to', f'{b:.3f}', '-i', str(mp3),
                          '-af', f'silencedetect=noise={NOISE}:d=0.3', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    sil = [[float(m[1]), None] for m in re.finditer(r'silence_start: ([\d.]+)', out)]
    for i, e in enumerate(re.finditer(r'silence_end: ([\d.]+)', out)):
        sil[i][1] = float(e[1])
    span = b - a
    if sil and sil[-1][1] is None: sil[-1][1] = span
    segs, cur = [], 0.0
    for s0, s1 in sil:
        if s0 - cur > 0.15: segs.append((cur, s0))
        cur = s1
    if span - cur > 0.15: segs.append((cur, span))
    if not segs: return a, b
    lo, hi = segs[0] if which == 'head' else segs[-1]
    return a + lo, a + hi

def detect_segments(mp3):
    """返回 [(start,end)] 语音段,按≥GAP静音切"""
    out = subprocess.run(['ffmpeg', '-i', str(mp3), '-af',
                          f'silencedetect=noise={NOISE}:d=0.3', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    dur = None
    m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', out)
    if m: dur = int(m[1])*3600 + int(m[2])*60 + float(m[3])
    sil = []  # (start,end)
    for s in re.finditer(r'silence_start: ([\d.]+)', out):
        sil.append([float(s[1]), None])
    for i, e in enumerate(re.finditer(r'silence_end: ([\d.]+)', out)):
        sil[i][1] = float(e[1])
    if sil and sil[-1][1] is None: sil[-1][1] = dur
    # 语音段 = 静音段之间的间隙;只有≥GAP的静音才算句界,短静音并入语音
    cuts = [(a, b) for a, b in sil if b - a >= GAP]
    segs, cur = [], 0.0
    for a, b in cuts:
        if a - cur > 0.15: segs.append((cur, a))
        cur = b
    if dur - cur > 0.15: segs.append((cur, dur))
    return segs, dur

def clip_uri(mp3, start, end, dur, tempo=None):
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
        tmp = Path(f.name)
    pad = 0.12  # 首尾留一点呼吸
    a, b = max(0, start - pad), min(end + pad, dur)
    # ⚠tempo须两步:先切出片段,再整段atempo。一步做会被-to按输出时间截断,慢速版只剩前70%内容
    subprocess.run(['ffmpeg', '-y', '-i', str(mp3), '-ss', f'{a:.3f}', '-to', f'{b:.3f}',
                    '-c:a', 'libmp3lame', '-q:a', '6', str(tmp)],
                   capture_output=True, check=True)
    if tempo:
        tmp2 = tmp.with_suffix('.slow.mp3')
        subprocess.run(['ffmpeg', '-y', '-i', str(tmp), '-af', f'atempo={tempo}',
                        '-c:a', 'libmp3lame', '-q:a', '6', str(tmp2)],
                       capture_output=True, check=True)
        tmp.unlink(); tmp = tmp2
    uri = 'data:audio/mpeg;base64,' + base64.b64encode(tmp.read_bytes()).decode()
    tmp.unlink()
    return uri

data = json.load(open(data_path))
audio = data.setdefault('audio', {})
ok = bad = 0
for track, info in sorted(by_track.items()):
    mp3 = audio_dir / f"{track}.mp3"
    if not mp3.exists():
        print(f"MISSING {mp3}"); bad += 1; continue
    segs, dur = detect_segments(mp3)
    if len(segs) != info['total']:
        print(f"SKIP {track}: 切出{len(segs)}段 ≠ 句数{info['total']} segs={[(round(a,1),round(b,1)) for a,b in segs]}")
        bad += 1; continue
    for pos, sid, clip, sub in sorted(info['sents']):
        a, b = clip if clip else segs[pos]
        if sub in ('head', 'tail'):
            a, b = fine_subseg(mp3, a, b, sub)
        if not args.dry_run:
            audio.setdefault(sid, {})['f'] = {
                'n': clip_uri(mp3, a, b, dur),
                's': clip_uri(mp3, a, b, dur, tempo=SLOW_TEMPO),
            }
        print(f"ok {track}[{pos}] -> {sid}  {a:.2f}-{b:.2f}s")
        ok += 1

if not args.dry_run:
    tmp = data_path.with_suffix('.json.tmp')
    json.dump(data, open(tmp, 'w'), ensure_ascii=False, indent=1)
    tmp.replace(data_path)
    print(f"written: {data_path}")
print(f"done: {ok} clips, {bad} tracks skipped")
