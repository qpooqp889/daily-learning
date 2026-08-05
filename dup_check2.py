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

cand_words = ['community', 'pollution', 'preserve', 'courage', 'patient', 'apologize', 'climate',
              'plastic', 'electricity', 'volunteer', 'neighbor', 'holiday', 'camera', 'popular',
              'instrument', 'message', 'station', 'famous', 'decide', 'collect', 'nature',
              'countryside', 'factory', 'imagine', 'planet', 'astronaut', 'mystery', 'unusual',
              'compare', 'protect', 'energy', 'reduce', 'invite', 'prepare', 'problem']
cand_idioms = ['如魚得水', '豁然開朗', '熟能生巧', '學以致用', '精益求精', '見賢思齊', '有志者事竟成',
               '百發百中', '一諾千金', '不恥下問', '集思廣益', '聞雞起舞', '愚公移山', '柳暗花明',
               '水滴石穿', '一本正經', '九牛二虎之力', '大顯身手', '手忙腳亂', '耳目一新',
               '念念不忘', '美不勝收', '驚天動地', '相輔相成', '自強不息', '腳踏實地']

out = []
out.append('=== WORD CHECK ===')
for w in cand_words:
    out.append('{} -> {}'.format(w, 'DUP' if norm(w) in wset else 'OK'))
out.append('=== IDIOM CHECK ===')
for i in cand_idioms:
    out.append('{} -> {}'.format(i, 'DUP' if norm(i) in iset else 'OK'))

with open('dup_check2.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print('done')
