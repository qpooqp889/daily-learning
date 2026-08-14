# -*- coding: utf-8 -*-
import json

path = 'data/words.json'
ws = json.load(open(path, encoding='utf-8'))
targets = ['tornado','recipe','whisper','giraffe','shell','pilot','battery']
added = 0
for w in ws:
    if w['word'] in targets and 'cambridge_url' not in w:
        w['cambridge_url'] = 'https://dictionary.cambridge.org/zht/詞典/英語-漢語-繁體/' + w['word']
        added += 1
json.dump(ws, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
open('chk.txt', 'w', encoding='utf-8').write('cambridge added: %d' % added)
print('done-write')
