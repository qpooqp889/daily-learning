# -*- coding: utf-8 -*-
"""Clean up example prefixes (例句：) and check explanation style."""
import json, re

PATH = r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms.json'
ids = json.load(open(PATH, encoding='utf-8'))

# 1. remove 例句： prefix from examples
n = 0
for i in ids:
    e = i.get('example', '')
    if e.startswith('例句：'):
        i['example'] = e[3:].strip()
        n += 1
print('fixed 例句：prefix:', n)

# 2. look at the 字詞拆解 style explanations — sample distribution
decomp = [i for i in ids if re.match(r'^[^。]{1,6}：', i.get('explanation',''))]
print('decomp-style explanations:', len(decomp))
# sample a few
for i in decomp[:8]:
    print('  ', i['id'], i['idiom'], '|', i['explanation'][:50])

json.dump(ids, open(PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('saved')
