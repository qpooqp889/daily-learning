# -*- coding: utf-8 -*-
"""Fix remaining Chinese pos values in words.json new entries."""
import json

DATA = r'C:\Users\twric\.qclaw\workspace\daily-learning\data\words.json'
POS_MAP = {
    '名詞': 'n.', '動詞': 'v.', '形容詞': 'a.', '副詞': 'ad.',
    '介系詞': 'prep.', '連接詞': 'conj.', '代名詞': 'pron.',
    '冠詞': 'art.', '感嘆詞': 'interj.', '縮寫': 'abbr.',
    '數字': 'num.', '限定詞': 'det.',
    '代詞': 'pron.', '數詞': 'num.', '助動詞': 'aux.', '限定詞': 'det.',
    '感嘆詞': 'interj.', '副詞': 'ad.',
}
import re
def fix_pos(pos):
    if not pos:
        return pos
    parts = re.split(r'[/／、]', pos)
    out = []
    for p in parts:
        p = p.strip()
        out.append(POS_MAP.get(p, p))
    return '/'.join(out)

ws = json.load(open(DATA, encoding='utf-8'))
changed = 0
for w in ws:
    if w['id'] >= 109:
        newp = fix_pos(w['pos'])
        if newp != w['pos']:
            w['pos'] = newp
            changed += 1
with open(DATA, 'w', encoding='utf-8') as f:
    json.dump(ws, f, ensure_ascii=False, indent=1)
print('changed:', changed)

from collections import Counter
c = Counter(w['pos'] for w in ws if w['id'] >= 109)
print('pos dist now:', dict(c.most_common(25)))
