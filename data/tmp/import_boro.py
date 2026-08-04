# -*- coding: utf-8 -*-
"""Re-import fixed boro_words.json into words.json."""
import json, urllib.parse, datetime

DATA = r'C:\Users\twric\.qclaw\workspace\daily-learning\data\words.json'
BORO = r'C:\Users\twric\.qclaw\workspace\daily-learning\data\boro_words.json'

def gurl(word):
    return 'https://translate.google.com/?hl=zh-TW&eotf=0&sl=en&tl=zh-TW&text=' + urllib.parse.quote(word) + '&op=translate'

words = json.load(open(DATA, encoding='utf-8'))
# Drop bad import (id >= 109 from previous attempt)
words = [w for w in words if w['id'] < 109]
print('words.json restored to:', len(words))

boro = json.load(open(BORO, encoding='utf-8'))
existing = {w['word'].strip().lower() for w in words}
new_words = [w for w in boro if w['word'].strip().lower() not in existing]
print('new words to add:', len(new_words))

start_id = max(w['id'] for w in words) + 1
today = datetime.date.today().isoformat()
added = []
for i, w in enumerate(new_words):
    added.append({
        'id': start_id + i,
        'word': w['word'],
        'pos': w['pos'],
        'meaning': w['meaning'],
        'gtranslate_url': gurl(w['word']),
        'created_at': today,
        'sentences': [],
        'phonetic': w['phonetic'],
    })

print('first:', json.dumps(added[0], ensure_ascii=False))
print('last:', json.dumps(added[-1], ensure_ascii=False))

all_words = words + added
with open(DATA, 'w', encoding='utf-8') as f:
    json.dump(all_words, f, ensure_ascii=False, indent=1)
print('TOTAL words now:', len(all_words))
print('added ids:', start_id, '-', start_id + len(added) - 1)
