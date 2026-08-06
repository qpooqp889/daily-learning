# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
words = json.load(open('data/words.json', encoding='utf-8'))
for t in ['rescue','kindness','breathe','finally','voyage','harvest','compass']:
    w = [x for x in words if x['word'].casefold() == t][0]
    print(f"{w['word']}: gtranslate_url = {w['gtranslate_url']}")
    for s in w.get('sentences', []):
        print(f"    sentence gtranslate = {s['gtranslate_url']}")
        print(f"    has cambridge = {w.get('cambridge_url', 'N/A')}")
