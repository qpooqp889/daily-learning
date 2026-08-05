# -*- coding: utf-8 -*-
"""Check newest idioms (added by cron 8/4, 8/5) for explanation quality."""
import json

ids = json.load(open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms.json', encoding='utf-8'))
print('total:', len(ids))

for i in ids:
    if i.get('created_at') in ('2026-08-04', '2026-08-05'):
        e = i.get('explanation','')
        print('  {} {} | {} | ex: {}'.format(i['id'], i['idiom'], e[:45], i.get('example','')[:30]))
