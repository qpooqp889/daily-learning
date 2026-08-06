# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
words = json.load(open('data/words.json', encoding='utf-8'))
today = ['rescue','kindness','breathe','finally','voyage','harvest','compass']
for t in today:
    found = [w for w in words if w['word'].casefold() == t]
    if found:
        w = found[0]
        print(f"[OK] {w['word']} ({w['pos']}) {w['meaning']} 句子數={len(w.get('sentences',[]))}")
        for s in w.get('sentences', []):
            print(f"     - {s['sentence']} | {s['translation']}")
    else:
        print(f"[MISS] {t}")
idioms = json.load(open('data/idioms.json', encoding='utf-8'))
tidioms = ['一鳴驚人','春暖花開','苦口婆心','得心應手','望梅止渴','聚沙成塔','鶴立雞群']
for t in tidioms:
    found = [i for i in idioms if i['idiom'] == t]
    if found:
        i = found[0]
        print(f"[OK] {i['idiom']}: {i['explanation']} | 例: {i['example']}")
    else:
        print(f"[MISS] {t}")
