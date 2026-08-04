# -*- coding: utf-8 -*-
"""Fix tail parsing issues in idioms_yjbys.json."""
import json, re

idioms = json.load(open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms_yjbys.json', encoding='utf-8'))
print('count:', len(idioms))
print('last 6:')
for i in idioms[-6:]:
    print('  ', i['num'], i['idiom'], '|', i['explanation'][:40], '|', i['example'][:40])
