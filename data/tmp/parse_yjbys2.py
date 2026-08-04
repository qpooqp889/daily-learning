# -*- coding: utf-8 -*-
"""Parse yjbys2 (成语大全及解释汇总), merge to reach 500 idioms."""
import re, json

html = open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms_yjbys2.html', encoding='utf-8').read()
ps = re.findall(r'<p[^>]*>(.*?)</p>', html, re.S)
ps = [re.sub(r'<[^>]+>', '', p).strip() for p in ps]
ps = [p for p in ps if p]

HEAD_RE = re.compile(r'^(\d{1,3})[、､]\s*([\u4e00-\u9fff]{2,8})\s*[:：]\s*(.*)$')
idioms = []
for p in ps:
    m = HEAD_RE.match(p)
    if m:
        num, name, expl = int(m.group(1)), m.group(2), m.group(3).strip()
        # extract example if present (造句：)
        ex = ''
        parts = re.split(r'造句[：:]', expl, maxsplit=1)
        if len(parts) == 2:
            expl, ex = parts[0].strip(), parts[1].strip()
        idioms.append({'num': num, 'idiom': name, 'explanation': expl, 'example': ex})
print('parsed:', len(idioms))

# internal dupes
seen, dupes = set(), []
for i in idioms:
    if i['idiom'] in seen:
        dupes.append((i['num'], i['idiom']))
    seen.add(i['idiom'])
print('internal dupes:', len(dupes), dupes[:15])

# weird / empty
weird = [i for i in idioms if re.search(r'[【】《》a-zA-Z]', i['explanation'])]
print('weird:', len(weird))
for w in weird[:10]: print('  ', w)
not4 = [i for i in idioms if len(i['idiom']) != 4]
print('not 4 chars:', len(not4))
noex = [i for i in idioms if not i['example']]
print('no example:', len(noex))

json.dump(idioms, open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms_yjbys2.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('saved idioms_yjbys2.json')
