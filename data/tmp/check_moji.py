# -*- coding: utf-8 -*-
"""Find rows with remaining mojibake (contain replacement chars or typical UTF-8-as-Latin1 patterns)."""
import json, re

ws = json.load(open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\words.json', encoding='utf-8'))

def is_mojibake(s):
    if not s:
        return False
    # Typical mojibake pattern: sequences of Ã, Â, å, ç, è, etc. (Latin-1 rendering of UTF-8)
    bad = re.findall(r'[ÃÂåæçèéêëìíîïðñòóôõöøùúûüýþÿ¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿]', s)
    return len(bad) >= 2

bad = [w for w in ws if is_mojibake(w.get('meaning', '')) or is_mojibake(w.get('word', '')) or is_mojibake(w.get('pos', '')) or is_mojibake(w.get('phonetic', ''))]
print('mojibake rows:', len(bad))
for w in bad[:30]:
    print('  id=%d word=%r pos=%r meaning=%r phon=%r' % (w['id'], w['word'][:20], w['pos'][:15], w['meaning'][:25], w['phonetic'][:20]))
