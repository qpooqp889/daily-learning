# -*- coding: utf-8 -*-
"""Validate words.json after import."""
import json, re

ws = json.load(open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\words.json', encoding='utf-8'))
print('total:', len(ws))

# 1. Any mojibake / bad chars
moji_pat = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f]')
issues = []
for w in ws:
    for field in ('word', 'pos', 'meaning', 'phonetic'):
        v = w.get(field, '')
        if moji_pat.search(v):
            issues.append((w['id'], field, 'control-char'))
        if 'Ã' in v or 'å\x83' in v:
            issues.append((w['id'], field, 'mojibake'))
print('issues:', len(issues))
for i in issues[:10]:
    print('  ', i)

# 2. Duplicate words
seen = {}
dupes = []
for w in ws:
    k = w['word'].strip().lower()
    if k in seen:
        dupes.append((w['id'], seen[k], w['word']))
    seen[k] = w['id']
print('duplicate words:', len(dupes))
for d in dupes[:10]:
    print('  ', d)

# 3. Empty required fields
empty = [w for w in ws if not w['word'].strip() or not w['meaning'].strip()]
print('empty word/meaning:', len(empty))

# 4. Id sequence
ids = sorted(w['id'] for w in ws)
print('id range:', ids[0], '-', ids[-1], '| count:', len(ids), '| unique:', len(set(ids)))

# 5. pos distribution (new words)
from collections import Counter
c = Counter(w['pos'] for w in ws if w['id'] >= 109)
print('pos dist (new):', dict(c.most_common(20)))

# 6. Sample check by letter
letters = {}
for w in ws:
    if w['id'] >= 109:
        letters.setdefault(w['word'][0].upper(), 0)
        letters[w['word'][0].upper()] += 1
print('letter counts:', dict(sorted(letters.items())))
