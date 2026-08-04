# -*- coding: utf-8 -*-
"""Assign categories to uncategorized idioms using add.py's guess_idiom_cat."""
import json, sys, importlib.util

spec = importlib.util.spec_from_file_location('add', r'C:\Users\twric\.qclaw\workspace\daily-learning\add.py')
add = importlib.util.module_from_spec(spec)
spec.loader.exec_module(add)

ids = json.load(open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms.json', encoding='utf-8'))
print('total:', len(ids))
nocat = [i for i in ids if not i.get('category')]
print('no category:', len(nocat))

from collections import Counter
c = Counter()
for i in nocat:
    cat = add.guess_idiom_cat(i['idiom'], i['explanation'])
    i['category'] = cat
    c[cat] += 1
print('assigned:', dict(c))

json.dump(ids, open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('saved')

# final dist
c2 = Counter(i['category'] for i in ids)
print('final dist:', dict(c2))
