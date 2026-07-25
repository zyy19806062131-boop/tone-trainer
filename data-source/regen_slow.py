#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全库重生成慢速版音频: 直接对已有正常速 clip 做 atempo,替换 audio[sid]['f']['s']。
背景: 旧管线一条 ffmpeg 命令同时 -to 截取+atempo,慢速输出被 -to 按输出时间截断,
每条只剩前70%内容(2026-07-22 用户听出)。本脚本只读 n 版,不动切点。"""
import json, base64, tempfile, subprocess, sys
from pathlib import Path

TEMPO = 0.7
data_path = Path(__file__).resolve().parent.parent / 'data' / 'trainer_data.private.json'
data = json.loads(data_path.read_text())
n = 0
for sid, voices in data.get('audio', {}).items():
    f = voices.get('f')
    if not f or 'n' not in f: continue
    raw = base64.b64decode(f['n'].split(',', 1)[1])
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as fh:
        fh.write(raw); src = Path(fh.name)
    dst = src.with_suffix('.slow.mp3')
    subprocess.run(['ffmpeg', '-y', '-i', str(src), '-af', f'atempo={TEMPO}',
                    '-c:a', 'libmp3lame', '-q:a', '6', str(dst)],
                   capture_output=True, check=True)
    f['s'] = 'data:audio/mpeg;base64,' + base64.b64encode(dst.read_bytes()).decode()
    src.unlink(); dst.unlink()
    n += 1
    if n % 50 == 0: print(f'{n} done', flush=True)

tmp = data_path.with_suffix('.json.tmp')
json.dump(data, open(tmp, 'w'), ensure_ascii=False, indent=1)
tmp.replace(data_path)
print(f'done: {n} slow clips regenerated')
