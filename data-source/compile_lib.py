#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""课文编译公共库: 教材拼音+汉字 -> 逐字音节声调 (从 build_hsk1.py 抽出,逻辑未动)"""
import re, unicodedata
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
    annotate_sandhi(zh, chars, syl)
    return syl, None

def sandhi_groups(zh, n):
    """按 jieba 分词把汉字序号切成变调作用组:
    - 多字词自成一组(词内可变调)
    - 连续的单字词并成一组(如 我/很/好、给/我)
    - 标点/非汉字 token 断组;多字词与单字词之间断组(如 上午|你、有|几口)
    返回 [(起,止)] 含两端。"""
    import jieba
    spans = []  # (start,end,len) 每个汉字词的序号区间
    hi = 0
    for tok in jieba.lcut(zh):
        hc = sum(1 for c in tok if '一' <= c <= '鿿')
        if hc == 0:
            spans.append(None)  # 标点等,断组标记
            continue
        spans.append((hi, hi + hc - 1))
        hi += hc
    groups = []
    cur = None
    for sp in spans:
        if sp is None:
            if cur: groups.append(cur); cur = None
            continue
        single = sp[0] == sp[1]
        if cur and single and cur[2]:          # 单字接续单字串
            cur = (cur[0], sp[1], True)
        else:
            if cur: groups.append(cur)
            cur = (sp[0], sp[1], single)
        if not single:                          # 多字词自成一组,立即封口
            groups.append(cur); cur = None
    if cur: groups.append(cur)
    return [(a, b) for a, b, _ in groups]

def annotate_sandhi(zh, chars, syl):
    """标注变调: cell 加 sd='原调-实读调', 三三变调另加 ta=实读调(曲线画实读)。
    - 三三变调: 只在变调作用组内(见 sandhi_groups),从右向左级联:
      前字为3且后字实读为3 => 前字实读2 (故 有几口 只标 几,我很好 只标 很)
    - 不: 教材已印 bú(2) => 4-2
    - 一: 教材已印 yí(2)/yì(4) => 1-2/1-4;电话号 yāo 不标
    """
    n = len(syl)
    for ch, s in zip(chars, syl):
        if ch == '不' and s['t'] == 2:
            s['sd'] = '4-2'
        elif ch == '一' and s['t'] in (2, 4):
            s['sd'] = f"1-{s['t']}"
    actual = [s['t'] for s in syl]
    for a, b in sandhi_groups(zh, n):
        for k in range(min(b, n - 1) - 1, a - 1, -1):
            if syl[k]['t'] == 3 and actual[k + 1] == 3:
                actual[k] = 2
                syl[k]['sd'] = '3-2'
                syl[k]['ta'] = 2

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

