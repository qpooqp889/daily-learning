# -*- coding: utf-8 -*-
"""Inspect words.json for header leftover rows."""
import json

ws = json.load(open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\words.json', encoding='utf-8'))
print('total:', len(ws))
bad = [w for w in ws if w['word'] in ('單字', '詞性', '音標', '解釋') or w['pos'] == '詞性']
print('bad rows:', len(bad))
for b in bad:
    print('  id:', b['id'], '| word:', repr(b['word']), '| pos:', repr(b['pos']), '| meaning:', repr(b['meaning']))
