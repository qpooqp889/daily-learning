# -*- coding: utf-8 -*-
"""Check for obviously wrong/broken explanations."""
import json, re

ids = json.load(open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms.json', encoding='utf-8'))

# check for idioms whose explanation contains the idiom itself (circular)
circular = []
for i in ids:
    e = i.get('explanation','')
    if e and i['idiom'] in e:
        circular.append((i['id'], i['idiom'], e[:40]))
print('circular explanations:', len(circular))
for c in circular[:10]: print('  ', c)

# check for known typos / odd entries
odd = []
for i in ids:
    e = i.get('explanation','')
    if '另人' in e or '乍舌' in i['idiom'] or '一十行' in i.get('example',''):
        odd.append((i['id'], i['idiom'], e[:40], i.get('example','')[:30]))
print('odd entries:', len(odd))
for o in odd: print('  ', o)

# check explanations that are just a single word repeat
single = [i for i in ids if len(i.get('explanation','').strip()) <= 5]
print('very short remaining:', len(single))
for s in single: print('  ', s['id'], s['idiom'], '|', repr(s['explanation']))
