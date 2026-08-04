# -*- coding: utf-8 -*-
"""Final QA: idioms.json — all traditional, deduped, categorized, complete."""
import json, re

ids = json.load(open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms.json', encoding='utf-8'))
print('total:', len(ids))

# simplified char check
s_chars = '惊墙书学马龙东丰见无与为习读练习证设议记认让讲许论识词语说请课谁调谈谊谢谨变责败质贪贫购货费贴贸资赶起越趋践踪踊跃车轨转轮软轻载辞达迁远还这进迎运近退还适选追送适'
hits = []
for i in ids:
    sc = [ch for ch in i['idiom'] + i['explanation'] + i['example'] if ch in s_chars]
    if sc:
        hits.append((i['id'], i['idiom'], ''.join(set(sc))[:8]))
print('simplified hits:', len(hits))
for h in hits[:15]: print('  ', h)

# dupes
seen = {}
dupes = []
for i in ids:
    if i['idiom'] in seen:
        dupes.append((i['id'], i['idiom']))
    seen[i['idiom']] = i['id']
print('dupes:', len(dupes))

# categories
from collections import Counter
c = Counter(i.get('category','') for i in ids)
print('categories:', dict(c))
nocat = [i for i in ids if not i.get('category')]
print('no category:', len(nocat))

# empty fields
noexpl = [i for i in ids if not i['explanation'].strip()]
noex = [i for i in ids if not i['example'].strip()]
print('no explanation:', len(noexpl), '| no example:', len(noex))

# id check
idset = [i['id'] for i in ids]
print('id unique:', len(idset) == len(set(idset)), '| range:', min(idset), '-', max(idset))

# weird brackets
weird = [i for i in ids if re.search(r'[【】《》]', i['explanation'] + i['example'])]
print('brackets in text:', len(weird))
for w in weird[:5]: print('  ', w['id'], w['idiom'], '|', (w['explanation']+w['example'])[:60])
