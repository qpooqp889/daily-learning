# -*- coding: utf-8 -*-
"""Precise repr of suspicious rows."""
import json, re

ws = json.load(open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\words.json', encoding='utf-8'))
report = []
report.append('total: %d' % len(ws))
for w in ws:
    if w['id'] >= 109:
        stripped = re.sub(r'\s+', '', w['word'])
        if stripped in ('單字', '詞性', '音標', '解釋') or not stripped:
            report.append('id=%d word=%r pos=%r meaning=%r' % (w['id'], w['word'], w['pos'], w['meaning']))
open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\report_bad.txt', 'w', encoding='utf-8').write('\n'.join(report))
print('done, lines:', len(report))
