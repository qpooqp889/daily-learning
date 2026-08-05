# -*- coding: utf-8 -*-
"""Final QA: all explanations complete and reasonable."""
import json

ids = json.load(open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms.json', encoding='utf-8'))
print('total idioms:', len(ids))

empty = [i for i in ids if not i.get('explanation','').strip()]
short = [i for i in ids if 0 < len(i.get('explanation','').strip()) < 10]
prefix = [i for i in ids if i.get('example','').startswith('例句：')]
dups = {}
for i in ids:
    dups.setdefault(i['idiom'], []).append(i['id'])
dup_list = {k: v for k, v in dups.items() if len(v) > 1}

print('empty explanation:', len(empty))
print('short <10:', len(short))
print('例句： prefix:', len(prefix))
print('duplicates:', len(dup_list))
for k, v in list(dup_list.items())[:10]: print('  ', k, v)

# length stats
lens = [len(i.get('explanation','').strip()) for i in ids]
import statistics
print('explanation len: min={} avg={:.1f} max={}'.format(min(lens), statistics.mean(lens), max(lens)))
