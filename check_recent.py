# -*- coding: utf-8 -*-
import json
from collections import Counter

words = json.load(open('data/words.json', encoding='utf-8'))
idioms = json.load(open('data/idioms.json', encoding='utf-8'))

out = []
out.append('words by date: ' + str(Counter(w['created_at'] for w in words)))
out.append('idioms by date: ' + str(Counter(i['created_at'] for i in idioms)))
out.append('---2026-08-04 words---')
for w in words:
    if w['created_at'] == '2026-08-04':
        out.append('{} | {} | {}'.format(w['word'], w['pos'], w['meaning']))
out.append('---2026-08-04 idioms---')
for i in idioms:
    if i['created_at'] == '2026-08-04':
        out.append(i['idiom'])
out.append('---latest 8 words overall---')
for w in words[:8]:
    out.append('{} | {} | {} | {}'.format(w['word'], w['pos'], w['meaning'], w['created_at']))
out.append('---latest 8 idioms overall---')
for i in idioms[:8]:
    out.append('{} | {} | {}'.format(i['idiom'], i['created_at'], i['explanation'][:30]))

with open('recent_out.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print('written')
