#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""旧《HSK标准教程》式音轨 -> 逐句音频对齐注入。
轨内结构: 课号播报(中英)+课文播报(中英)+对话句+"New Words"+生词朗读,
故不能按段数硬对,而是: 静音切段 -> 每段过 faster-whisper ASR -> 与课文句
模糊匹配(DP,每句可并1-3个相邻段) -> 取最优窗口截取。
用法: python3 align_official_audio.py --source hsk1_kewen_source --deck hsk1 \
        --audio-dir <轨目录> [--only 01-1] [--dry-run]
ASR结果缓存在 <deck>_asr_cache.json,重跑不重转。
"""
import json, argparse, base64, subprocess, re, tempfile, difflib, sys
from pathlib import Path

GAP = 0.8
NOISE = '-35dB'
SLOW_TEMPO = 0.7
MIN_SCORE = 0.45   # 每句平均得分(含时长惩罚)低于此报人工

ap = argparse.ArgumentParser()
ap.add_argument('--source', required=True)
ap.add_argument('--deck', required=True)
ap.add_argument('--audio-dir', required=True)
ap.add_argument('--only', help='只处理指定轨,逗号分隔')
ap.add_argument('--dry-run', action='store_true')
ap.add_argument('--gap', type=float, default=GAP, help='句界静音阈值(秒)')
ap.add_argument('--force', action='store_true', help='已有音频也重切')
ap.add_argument('--max-take', type=int, default=2,
                help='每句最多并几个相邻段(句内含句号会断段,默认2;误并播报由NW边界+时长惩罚兜住)')
ap.add_argument('--model', default='tiny',
                help="faster-whisper 模型档。⚠️本机(Apple Silicon+系统Python3.9的CTranslate2)"
                     "用 small 会静默段错误(进程直接没了,无traceback),只能 tiny;"
                     "精度够用——内容有教材原文兜底,机器只负责定位")
args = ap.parse_args()

here = Path(__file__).resolve().parent
sys.path.insert(0, str(here))
LESSONS = __import__(args.source).LESSONS
data_path = here.parent / 'data' / 'trainer_data.private.json'
cache_path = here / f"{args.deck}_asr_cache.json"
# 缓存键含 gap 与模型档:换任一个,分段边界/识别结果都会变,不能复用旧条目
audio_dir = Path(args.audio_dir)
cache = json.load(open(cache_path)) if cache_path.exists() else {}

def hanzi(s): return ''.join(c for c in s if '一' <= c <= '鿿')
def sim(a, b):
    a, b = hanzi(a), hanzi(b)
    if not a or not b: return 0.0
    return difflib.SequenceMatcher(None, a, b).ratio()

def detect_segments(mp3):
    out = subprocess.run(['ffmpeg', '-i', str(mp3), '-af',
                          f'silencedetect=noise={NOISE}:d=0.3', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', out)
    dur = int(m[1])*3600 + int(m[2])*60 + float(m[3])
    sil = [[float(s[1]), None] for s in re.finditer(r'silence_start: ([\d.]+)', out)]
    for i, e in enumerate(re.finditer(r'silence_end: ([\d.]+)', out)):
        sil[i][1] = float(e[1])
    if sil and sil[-1][1] is None: sil[-1][1] = dur
    cuts = [(a, b) for a, b in sil if b - a >= args.gap]
    segs, cur = [], 0.0
    for a, b in cuts:
        if a - cur > 0.15: segs.append((cur, a))
        cur = b
    if dur - cur > 0.15: segs.append((cur, dur))
    return segs, dur

_model = None
def asr(mp3, a, b):
    global _model
    if _model is None:
        from faster_whisper import WhisperModel
        _model = WhisperModel(args.model, device='cpu', compute_type='int8')
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
        tmp = Path(f.name)
    subprocess.run(['ffmpeg', '-y', '-i', str(mp3), '-ss', f'{a:.3f}', '-to', f'{b:.3f}',
                    '-ar', '16000', '-ac', '1', str(tmp)], capture_output=True, check=True)
    segs, _ = _model.transcribe(str(tmp), language='zh', beam_size=3,
                                initial_prompt='汉语教材课文录音,普通话。')
    text = ''.join(s.text for s in segs)
    tmp.unlink()
    return text.strip()

def track_asr(track, mp3, segs):
    key = f"{track}:{len(segs)}:g{args.gap}:{args.model}"
    if key in cache: return cache[key]
    texts = [asr(mp3, a, b) for a, b in segs]
    cache[key] = texts
    json.dump(cache, open(cache_path, 'w'), ensure_ascii=False, indent=1)
    return texts

NW_RE = re.compile(r'new\s*words|生词|新语|neww', re.I)

def newwords_idx(texts):
    """找 "New Words" 播报段:它之后全是生词朗读,课文句必须在它之前"""
    for i, t in enumerate(texts):
        if i >= 2 and NW_RE.search(t):
            return i
    return len(texts)

def dur_penalty(expected_zh, a, b):
    """句时长与音节数不匹配则扣分(防吞播报段/误取单字生词)"""
    n = len(hanzi(expected_zh))
    exp = 0.42 * n + 0.4
    return min(0.5, 0.35 * abs((b - a) - exp) / exp)

def align(expected, segs, texts, max_take=1):
    """DP: 每句消费1..max_take个相邻段,句间连续,全部位于 New Words 段之前。
    得分=文本相似度-时长偏离惩罚。返回 [(segA,segB)] 或 None"""
    n = len(expected)
    m = min(len(segs), newwords_idx(texts))
    best = (-1, None)
    for start in range(m):
        dp = {(0, start): (0.0, [])}
        for j in range(n):
            ndp = {}
            for (jj, k), (sc, path) in dp.items():
                if jj != j: continue
                for take in range(1, max_take + 1):
                    if k + take > m: break
                    t = ''.join(texts[k:k+take])
                    s2 = sim(expected[j], t) - dur_penalty(expected[j], segs[k][0], segs[k+take-1][1])
                    key = (j+1, k+take)
                    val = (sc + s2, path + [(k, k+take-1)])
                    if key not in ndp or ndp[key][0] < val[0]:
                        ndp[key] = val
            dp = ndp
            if not dp: break
        for (jj, k), (sc, path) in dp.items():
            if jj == n:
                sc_biased = sc - 0.015 * start  # 同分优先靠前窗口(课文在生词表之前)
                if sc_biased > best[0]:
                    best = (sc_biased, path)
    if best[1] is None: return None, 0
    return best[1], best[0] / n

def clip_uri(mp3, start, end, dur, tempo=None):
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
        tmp = Path(f.name)
    pad = 0.12
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
deck = next(d for d in data['decks'] if d['id'] == args.deck)
# zh(去标点) -> sid 供回查
zh2sid = {hanzi(s['zh']): s['id'] for s in deck['sents']}
only = set(args.only.split(',')) if args.only else None

ok = warn = 0
for L in LESSONS:
    for sc in L['scenes']:
        track = sc.get('track')
        if not track or (only and track not in only): continue
        mp3 = audio_dir / f"{track}.mp3"
        if not mp3.exists():
            print(f"MISSING {mp3}"); warn += 1; continue
        segs, dur = detect_segments(mp3)
        texts = track_asr(track, mp3, segs)
        expected = [s[0] for s in sc['sents']]
        # 源文件第4元组 {"clip":(起,止)} = 手工钉死的绝对区间,覆盖 DP 结果。
        # 用途:相邻句首尾撞词时(如「小雪,生日快乐!」后接「姐姐,生日快乐!」)DP 会整段挪位,
        # 靠分数看不出来——只能人工定界。zh 去标点后作键,与 zh2sid 同口径。
        clips = {hanzi(s[0]): s[3]['clip'] for s in sc['sents']
                 if len(s) > 3 and isinstance(s[3], dict) and s[3].get('clip')}
        path, score = align(expected, segs, texts, args.max_take)
        if path is None or score < MIN_SCORE:
            print(f"REVIEW {track} score={score:.2f}")
            for i, (t, s_) in enumerate(zip(texts, segs)):
                print(f"    seg{i} {s_[0]:.1f}-{s_[1]:.1f} {t}")
            warn += 1; continue
        for j, (zh_full) in enumerate(expected):
            sid = zh2sid.get(hanzi(zh_full))
            if sid is None: continue  # 去重被丢的句子:跳过(首现那条已配)
            a = segs[path[j][0]][0]; b = segs[path[j][1]][1]
            manual = clips.get(hanzi(zh_full))
            if manual:
                a, b = manual
            nsyl = len(hanzi(zh_full))
            flag = '  [手工区间]' if manual else ''
            if not (0.15 * nsyl + 0.1 <= b - a <= 0.7 * nsyl + 2.0):
                flag = f'  ⚠时长{b-a:.1f}s vs {nsyl}音节'
            if not args.dry_run and (args.force or 'f' not in audio.get(sid, {})):
                audio.setdefault(sid, {})['f'] = {
                    'n': clip_uri(mp3, a, b, dur),
                    's': clip_uri(mp3, a, b, dur, tempo=SLOW_TEMPO)}
            print(f"ok {track} [{zh_full}] -> {sid} {a:.1f}-{b:.1f}s (avg {score:.2f}){flag}")
            ok += 1
            if flag: warn += 1

if not args.dry_run:
    tmp = data_path.with_suffix('.json.tmp')
    json.dump(data, open(tmp, 'w'), ensure_ascii=False, indent=1)
    tmp.replace(data_path)
    print('written:', data_path)
print(f"done: {ok} clips, {warn} tracks need attention")
