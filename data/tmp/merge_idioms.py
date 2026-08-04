# -*- coding: utf-8 -*-
"""Final QA on 325 yjbys idioms, then merge into idioms.json (target 500)."""
import re, json

idioms = json.load(open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms_yjbys.json', encoding='utf-8'))
print('total parsed:', len(idioms))

# internal dupes
seen, dupes = set(), []
for i in idioms:
    if i['idiom'] in seen:
        dupes.append((i['num'], i['idiom']))
    seen.add(i['idiom'])
print('internal dupes:', len(dupes))
for d in dupes: print('  ', d)

# weird chars
weird = []
for i in idioms:
    if re.search(r'[【】《》a-zA-Z]', i['explanation']):
        weird.append((i['num'], i['idiom'], i['explanation'][:40]))
    if '相关' in i['example'] or '成语解释' in i['example']:
        weird.append((i['num'], i['idiom'], 'JUNK-EXAMPLE'))
print('weird:', len(weird))
for w in weird: print('  ', w)

# 4-char check
not4 = [i for i in idioms if len(i['idiom']) != 4]
print('not 4 chars:', len(not4))
for i in not4: print('  ', i['num'], i['idiom'])

# empty
empty = [i for i in idioms if not i['explanation'].strip() or not i['example'].strip()]
print('empty:', len(empty))

# merge into idioms.json
existing = json.load(open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms.json', encoding='utf-8'))
print('existing idioms:', len(existing))
exist_names = {e['idiom'] for e in existing}
new_entries = [i for i in idioms if i['idiom'] not in exist_names]
print('new to add:', len(new_entries))

# assign ids continuing from max existing
max_id = max(e['id'] for e in existing)
print('max existing id:', max_id)
for n, entry in enumerate(new_entries):
    entry['id'] = max_id + 1 + n
    entry['created_at'] = '2026-08-03'
    entry['category'] = ''
    del entry['num']

merged = existing + new_entries
print('merged total:', len(merged))
json.dump(merged, open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('merged saved')
