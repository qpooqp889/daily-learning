# -*- coding: utf-8 -*-
"""Merge yjbys2 into idioms.json to reach 500. Dedupe vs all existing."""
import re, json

src = json.load(open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms_yjbys2.json', encoding='utf-8'))
cur = json.load(open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms.json', encoding='utf-8'))

exist_names = {e['idiom'] for e in cur}
print('current total:', len(cur))

new_entries = []
seen = set()
for i in src:
    name = i['idiom']
    if name in exist_names or name in seen:
        continue
    seen.add(name)
    new_entries.append({
        'idiom': name,
        'explanation': i['explanation'],
        'example': i['example'],
        'created_at': '2026-08-03',
        'category': ''
    })
print('new from yjbys2:', len(new_entries))

max_id = max(e['id'] for e in cur)
for n, e in enumerate(new_entries):
    e['id'] = max_id + 1 + n

merged = cur + new_entries
print('merged total:', len(merged))
json.dump(merged, open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('saved. target 500:', 'OK' if len(merged) >= 500 else 'need more')
