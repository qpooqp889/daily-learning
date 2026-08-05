# -*- coding: utf-8 -*-
"""QA check for remaining explanation quality issues."""
import json, re

ids = json.load(open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms.json', encoding='utf-8'))
print('total:', len(ids))

# 1. "例句：" prefix residue
ex_pre = [i for i in ids if i.get('example','').startswith('例句：')]
print('example starts with 例句：:', len(ex_pre))
for i in ex_pre[:5]: print('  ', i['id'], i['idiom'], '|', i['example'][:30])

# 2. explanations containing weird chars
weird = [i for i in ids if re.search(r'[【】《》]|：|簡：', i.get('explanation',''))]
print('weird explanation chars:', len(weird))
for i in weird[:10]: print('  ', i['id'], i['idiom'], '|', i['explanation'][:40])

# 3. template examples (from gen_examples.py last time) - list them for potential improvement
tpl = [i for i in ids if re.search(r'(他這樣的做法|這件事讓大家體會到|老師用|面對這種情況|他的表現可說是)', i.get('example',''))]
print('template examples:', len(tpl))

# 4. check new idioms added by cron (created_at 2026-08-04, 2026-08-05)
from collections import Counter
c = Counter(i.get('created_at','') for i in ids)
print('by date:', dict(c))

# 5. short explanations after fix
short = [i for i in ids if len(i.get('explanation','').strip()) < 10]
print('short remaining:', len(short))
