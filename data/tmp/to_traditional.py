# -*- coding: utf-8 -*-
"""Convert simplified Chinese idioms/entries to Traditional (Taiwan) via OpenCC."""
import json
from opencc import OpenCC

cc = OpenCC('s2twp')  # simplified -> Taiwan traditional (with phrases)

ids = json.load(open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms.json', encoding='utf-8'))
print('total:', len(ids))

# Only convert entries added today (id >= 110) — original 107 already traditional
changed = 0
for i in ids:
    if i['id'] < 110:
        continue
    new_idiom = cc.convert(i['idiom'])
    new_expl = cc.convert(i['explanation'])
    new_ex = cc.convert(i['example'])
    if (new_idiom, new_expl, new_ex) != (i['idiom'], i['explanation'], i['example']):
        # dedupe check: if converted name collides with existing, skip or keep both
        i['idiom'] = new_idiom
        i['explanation'] = new_expl
        i['example'] = new_ex
        changed += 1
print('converted entries:', changed)

# post-check duplicates
seen = {}
dupes = []
for i in ids:
    if i['idiom'] in seen:
        dupes.append((i['id'], seen[i['idiom']], i['idiom']))
    seen[i['idiom']] = i['id']
print('dupes after conversion:', len(dupes))
for d in dupes[:20]:
    print('  ', d)

json.dump(ids, open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('saved')

# sample
for i in ids:
    if i['id'] in (110, 420, 700, 800):
        print('  ', i['id'], i['idiom'], '|', i['explanation'][:30], '|', i['example'][:30])
