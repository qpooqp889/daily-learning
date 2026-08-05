# -*- coding: utf-8 -*-
import json, unicodedata

def norm(s):
    s = unicodedata.normalize("NFC", (s or "").strip())
    s = s.replace(" ", "").replace("\u3000", "")
    return s.casefold()

words = json.load(open('data/words.json', encoding='utf-8'))
idioms = json.load(open('data/idioms.json', encoding='utf-8'))
wset = set(norm(w['word']) for w in words)
iset = set(norm(i['idiom']) for i in idioms)

cand_words = ['environment', 'celebrate', 'invention', 'generous', 'experience', 'foreign', 'language',
              'geography', 'recycle', 'brave', 'dinosaur', 'library']
cand_idioms = ['有志竟成', '亡羊補牢', '畫蛇添足', '半途而廢', '滴水穿石', '聚精會神', '按部就班',
               '舉一反三', '融會貫通', '刮目相看', '如魚得水', '百折不撓', '懸樑刺股', '鐵杵磨針']

out = []
out.append('=== WORD CHECK ===')
for w in cand_words:
    out.append('{} -> {}'.format(w, 'DUPLICATE' if norm(w) in wset else 'OK'))
out.append('=== IDIOM CHECK ===')
for i in cand_idioms:
    out.append('{} -> {}'.format(i, 'DUPLICATE' if norm(i) in iset else 'OK'))

with open('dup_check.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print('done')
