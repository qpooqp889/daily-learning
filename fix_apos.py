# -*- coding: utf-8 -*-
import json

path = 'data/words.json'
ws = json.load(open(path, encoding='utf-8'))
fixed = 0
for w in ws:
    if w['word'] == 'whisper':
        for s in w.get('sentences', []):
            if 'don%27t' in s.get('gtranslate_url', ''):
                s['gtranslate_url'] = s['gtranslate_url'].replace('don%27t', 'don%E2%80%99t')
                fixed += 1
json.dump(ws, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
open('chk.txt', 'w', encoding='utf-8').write('fixed: %d' % fixed)
print('done-write')
