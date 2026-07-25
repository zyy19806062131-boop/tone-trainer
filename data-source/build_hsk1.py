#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 hsk1_kewen.py 的课文原文(zh + 教材拼音py + en)编译成音调训练器 hsk1 deck。
声调/字母 取自教材拼音(权威,含不/一变调与轻声);逐字对齐边界借 pypinyin 校准。
儿化的'儿'单列 p='er' t=0 (weak),与旧数据一致。"""
import sys, re, json, unicodedata
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from hsk1_kewen_source import LESSONS
from pypinyin import pinyin, Style

COMB={'̄':1,'́':2,'̌':3,'̀':4}  # ̄ ́ ̌ ̀

def split_syl(toned):
    """单个带调音节 -> (基字母lower含v代ü, 声调0-4)"""
    nfd=unicodedata.normalize('NFD',toned)
    tone=0; base=''
    for ch in nfd:
        if ch in COMB: tone=COMB[ch]; continue
        if unicodedata.combining(ch): continue
        base+=ch
    return base.lower().replace('ü','v').replace('u:','v'), tone

def han(zh): return [c for c in zh if '一'<=c<='鿿']

def base_of(toned_str):
    """整串去调去空格去撇 -> 纯字母"""
    b='';
    for ch in unicodedata.normalize('NFD',toned_str):
        if unicodedata.combining(ch): continue
        if ch in "'’ 　": continue
        b+=ch
    return b.lower().replace('ü','v')

# 把带调整句按 pypinyin 逐字基长切分, 取教材声调
U_MAP={'ǖ':'v̄','ǘ':'v́','ǚ':'v̌','ǜ':'v̀','ü':'v'}
def compile_sentence(zh, py):
    for k,v in U_MAP.items(): py=py.replace(k,v)  # ü系->v+调号,避免分音符挡住声调
    chars=han(zh)
    exp=[p[0] for p in pinyin(zh, style=Style.NORMAL, heteronym=False, errors='ignore')]
    exp=[e.lower().replace('ü','v').replace('u:','v') for e in exp]
    if len(exp)!=len(chars):
        return None, f"pypinyin音节数{len(exp)}≠字数{len(chars)}: {zh}"
    # 教材带调串 -> NFD 保留调号, 去空格/撇, 按字符流走
    toned=[]
    for ch in unicodedata.normalize('NFD',py):
        if ch in "'’ 　": continue
        toned.append(ch)
    # toned 是 (基字母+调号) 的字符流; 逐字消费
    syl=[]; i=0
    def peek_base(n):
        # 从 i 起取 n 个"基字母"(跳过调号),返回(消费到的下标, 基串, 调)
        j=i; got=''; tone=0
        while j<len(toned) and len(got)<n:
            c=toned[j]
            if c in COMB: tone=COMB[c]; j+=1; continue
            if unicodedata.combining(c): j+=1; continue
            got+=c.lower().replace('ü','v'); j+=1
        # 吸收紧跟的调号
        while j<len(toned) and toned[j] in COMB:
            tone=COMB[toned[j]]; j+=1
        return j, got, tone
    for k,ch in enumerate(chars):
        want=exp[k]
        if ch=='儿':
            # 儿化: 剩余基串以 r 开头且不是完整 er -> er/0/weak
            j,got,tone=peek_base(2)
            if got=='er':
                syl.append({'p':'er','t':tone if tone else 2}); i=j
            else:
                # 只有 r (儿化) 或空
                # 消费一个 r
                jj=i
                while jj<len(toned) and toned[jj] in COMB: jj+=1
                if jj<len(toned) and toned[jj].lower()=='r':
                    i=jj+1
                syl.append({'p':'er','t':0,'s':'weak'})
            continue
        # 边界长度取 pypinyin;仅"一"在电话号码读 yāo(3字母)需特判
        n=len(want)
        if ch=='一':
            _,g3,_=peek_base(3)
            if g3=='yao': n=3
        j,got,tone=peek_base(n)
        # 字母/声调一律取教材(got);got 为空说明级联错位
        if not got:
            return None, f"对齐失败(空) 字{ch} @ {zh} | py={py}"
        p=py_syllable(got,tone)
        cell={'p':p,'t':tone}
        if tone==0: cell['s']='weak'
        syl.append(cell)
        i=j
    return syl, None

# 把 (基字母, 声调) 还原成带调拼音展示串
VOWEL_ORDER='aoeiuv'
TONE_CHARS={
 'a':'aāáǎà','o':'oōóǒò','e':'eēéěè','i':'iīíǐì','u':'uūúǔù','v':'üǖǘǚǜ'}
def py_syllable(base, tone):
    if tone==0:
        return base.replace('v','ü')
    # 选调号位置: a>o>e; 否则 iu/ui 标在后一个; 其余唯一元音
    b=base
    idx=-1
    if 'a' in b: idx=b.index('a')
    elif 'o' in b: idx=b.index('o')
    elif 'e' in b: idx=b.index('e')
    else:
        # 找最后一个 i/u/v
        for m in range(len(b)-1,-1,-1):
            if b[m] in 'iuv': idx=m; break
    if idx<0: return b.replace('v','ü')
    v=b[idx]
    marked=TONE_CHARS[v][tone]
    return (b[:idx]+marked+b[idx+1:]).replace('v','ü')

def unit_access(idx):
    return 'free' if idx==0 else 'paid'

deck={'id':'hsk1','name':'HSK1','full':True,'hidden':False,'units':[],'sents':[]}
errors=[]; scount=0
seen_zh=set()  # 全局去重(课内+跨课):同一纯汉字句只保留首次出现
dropped=[]
for li,L in enumerate(LESSONS):
    num=L['id'].split('-')[1]
    deck['units'].append({'id':L['id'],'name':f"{int(num)} {L['title']}",
                          'hidden':False,'access':unit_access(li),'paymentUrl':''})
    sidx=0
    for sc in L['scenes']:
        for zh,py,en in sc['sents']:
            syl,err=compile_sentence(zh,py)
            if err: errors.append(err); continue
            # 校验:音节数==非标点汉字数
            if len(syl)!=len(han(zh)):
                errors.append(f"音节数{len(syl)}≠字数{len(han(zh))}: {zh}"); continue
            zh_bare=''.join(han(zh))  # App逐字映射,zh存纯汉字(与旧数据一致,零改动兼容)
            if zh_bare in seen_zh:
                dropped.append(f"{L['id']} {zh}"); continue
            seen_zh.add(zh_bare)
            sidx+=1
            deck['sents'].append({
                'id':f"{L['id']}-{sidx:02d}",
                'unitId':L['id'],
                'zh':zh_bare,'en':en,
                'syl':syl,
                'spokenZh':zh,   # 带标点原句,供TTS自然停顿
            })
            scount+=1

print(f"lessons={len(deck['units'])} sentences={scount} errors={len(errors)} 去重丢弃={len(dropped)}")
for d_ in dropped: print("  DUP:",d_)
for e in errors[:40]: print("  ERR:",e)
OUT=Path(__file__).resolve().parent/'hsk1_deck.json'
json.dump(deck, open(OUT,'w'), ensure_ascii=False, indent=1)
print("written:",OUT)
# 打印抽查:每课第1句
print("\n抽查(每课第1句):")
seen=set()
for s in deck['sents']:
    if s['unitId'] in seen: continue
    seen.add(s['unitId'])
    print(f"  [{s['unitId']}] {s['zh']}")
    print("     ", ' '.join(f"{c['p']}{c['t']}" for c in s['syl']))
