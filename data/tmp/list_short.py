# -*- coding: utf-8 -*-
import json
ids = json.load(open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms.json', encoding='utf-8'))
short = [i for i in ids if len(i.get('explanation','').strip()) < 10]
print('explanations <10 chars:', len(short))
for i in sorted(short, key=lambda x: len(x['explanation'])):
    print('  {} {} | {} | ex: {}'.format(i['id'], i['idiom'], i['explanation'], i.get('example','')[:25]))
