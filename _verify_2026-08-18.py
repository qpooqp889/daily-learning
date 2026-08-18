# -*- coding: utf-8 -*-
import json, io

words = json.load(open('data/words.json', encoding='utf-8'))
idioms = json.load(open('data/idioms.json', encoding='utf-8'))

targets = ['concert', 'rhythm', 'melody', 'chorus', 'banner', 'mural', 'campaign']
out = io.StringIO()
for t in targets:
    for w in words:
        if w['word'].lower() == t:
            out.write(f"WORD {w['word']} | {w['pos']} | {w['meaning']} | created {w['created_at']} | sentences: {len(w.get('sentences', []))}\n")
            for s in w.get('sentences', []):
                out.write(f"    S: {s['sentence']}\n    Z: {s['translation']}\n    G: {s['gtranslate_url']}\n")
            break
    else:
        out.write(f"MISSING WORD: {t}\n")

tid = ['杯水車薪', '百步穿楊', '獨當一面', '實至名歸', '妙筆生花', '出神入化', '心無旁騖']
for t in tid:
    for i in idioms:
        if i['idiom'] == t:
            out.write(f"IDIOM {i['idiom']} | {i['explanation']} | ex: {i['example']} | created {i['created_at']} | cat {i['category']}\n")
            break
    else:
        out.write(f"MISSING IDIOM: {t}\n")

with open('_verify_2026-08-18.txt', 'w', encoding='utf-8') as f:
    f.write(out.getvalue())
print('verify done')
