# -*- coding: utf-8 -*-
"""QA on merged 956 idioms + categorize the uncategorized ones."""
import re, json

ids = json.load(open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms.json', encoding='utf-8'))
print('total:', len(ids))

# global dupes
seen, dupes = {}, []
for i in ids:
    if i['idiom'] in seen:
        dupes.append((i['id'], seen[i['idiom']], i['idiom']))
    seen[i['idiom']] = i['id']
print('global dupes:', len(dupes))
for d in dupes[:10]: print('  ', d)

# id unique
idset = [i['id'] for i in ids]
print('id unique:', len(idset) == len(set(idset)), '| range:', min(idset), '-', max(idset))

# empty fields
noexpl = [i for i in ids if not i['explanation'].strip()]
print('no explanation:', len(noexpl))
noex = [i for i in ids if not i['example'].strip()]
print('no example:', len(noex))
nocat = [i for i in ids if not i.get('category')]
print('no category:', len(nocat))

# category dist
from collections import Counter
c = Counter(i['category'] for i in ids if i.get('category'))
print('category dist:', dict(c))

# weird chars in explanations
weird = [i for i in ids if re.search(r'[【】《》]', i['explanation'])]
print('bracket in explanation:', len(weird))
for w in weird[:5]: print('  ', w['id'], w['idiom'], w['explanation'][:50])

# non-4-char idioms
not4 = [i for i in ids if len(i['idiom']) != 4]
print('not 4 chars:', len(not4))
for i in not4[:10]: print('  ', i['id'], i['idiom'])
