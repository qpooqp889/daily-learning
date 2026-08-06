# -*- coding: utf-8 -*-
"""Precisely count template/placeholder examples (not real sentences)."""
import json, re

ids = json.load(open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms.json', encoding='utf-8'))

TPL_PATTERNS = [
    re.compile(r'^他這樣的做法，真是.+。$'),
    re.compile(r'^這件事讓大家體會到.+的道理。$'),
    re.compile(r'^老師用.+來提醒我們。$'),
    re.compile(r'^面對這種情況，.+最適合形容。$'),
    re.compile(r'^他的表現可說是.+的具體寫照。$'),
]

tpl_ids = []
for i in ids:
    e = i.get('example', '').strip()
    for p in TPL_PATTERNS:
        if p.match(e):
            tpl_ids.append(i['id'])
            break

print('total idioms:', len(ids))
print('template examples:', len(tpl_ids))
print('real examples:', len(ids) - len(tpl_ids))

# save the list
with open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\tmp\tpl_ids.json', 'w', encoding='utf-8') as f:
    json.dump(tpl_ids, f, ensure_ascii=False)
print('saved tpl_ids.json')

# also check near-miss patterns (other suspicious placeholders)
other = []
for i in ids:
    if i['id'] in tpl_ids: continue
    e = i.get('example', '').strip()
    if re.search(r'(最適合形容|來提醒我們|具體寫照|的道理。|真是。$)', e):
        other.append((i['id'], i['idiom'], e[:35]))
print('other suspicious:', len(other))
for o in other[:15]: print('  ', o)
