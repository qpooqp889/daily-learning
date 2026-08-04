# -*- coding: utf-8 -*-
"""Remove global dupes, keep first occurrence. Then handle example-less entries."""
import json

ids = json.load(open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms.json', encoding='utf-8'))
print('before:', len(ids))

seen = {}
keep = []
removed = []
for i in ids:
    if i['idiom'] in seen:
        removed.append((i['id'], i['idiom'], 'dup-of', seen[i['idiom']]))
        continue
    seen[i['idiom']] = i['id']
    keep.append(i)
print('removed dupes:', len(removed))
for r in removed: print('  ', r)
print('after:', len(keep))

# renumber ids sequentially from min
min_id = min(i['id'] for i in keep)
for n, i in enumerate(keep):
    i['id'] = min_id + n

json.dump(keep, open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('saved, id range:', min_id, '-', min_id + len(keep) - 1)

# count example-less
noex = [i for i in keep if not i['example'].strip()]
print('no example:', len(noex))
