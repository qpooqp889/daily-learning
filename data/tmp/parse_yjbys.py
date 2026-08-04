# -*- coding: utf-8 -*-
"""Parse yjbys idioms v4: two-pass. Pass1 find sequential headers, Pass2 attribute paragraphs."""
import re, json

html = open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms_yjbys.html', encoding='utf-8').read()
ps = re.findall(r'<p[^>]*>(.*?)</p>', html, re.S)
ps = [re.sub(r'<[^>]+>', '', p).strip() for p in ps]
ps = [p for p in ps if p]

HEAD_RE = re.compile(r'^(\d{1,3})[、､]\s*([\u4e00-\u9fff]{2,8})\s*[:：]?\s*(.*)$')

# Pass 1: locate sequential headers
headers = []  # (idx, num, name, rest)
expect = 1
i = 0
while i < len(ps):
    m = HEAD_RE.match(ps[i])
    if m and int(m.group(1)) == expect:
        headers.append((i, int(m.group(1)), m.group(2), m.group(3).strip()))
        expect += 1
        i += 1
        continue
    i += 1
print('headers found:', len(headers), 'expect next:', expect)

# Pass 2: attribute paragraphs after each header until next header
idioms = []
for h, (idx, num, name, rest) in enumerate(headers):
    end = headers[h + 1][0] if h + 1 < len(headers) else len(ps)
    body = ps[idx + 1:end]
    expl = rest
    ex = ''
    # split inline rest
    if rest:
        parts = re.split(r'造句[：:]', rest, maxsplit=1)
        if len(parts) == 2:
            expl = parts[0].strip()
            ex = parts[1].strip()
        else:
            expl = rest
    for b in body:
        if re.match(r'^【出自】', b) or re.match(r'^【示例】', b):
            ex = (ex + ' ' + re.sub(r'^【(出自|示例)】', '', b)).strip()
            continue
        if '相关文章' in b or re.match(r'^\d+[、､]', b):
            continue
        # if explanation empty, first body line is explanation; else example
        if not expl:
            parts = re.split(r'造句[：:]', b, maxsplit=1)
            if len(parts) == 2:
                expl = parts[0].strip()
                ex = (ex + ' ' + parts[1]).strip()
            else:
                expl = b
        else:
            ex = (ex + ' ' + b).strip()
    expl = re.sub(r'^【解释】[:：]?', '', expl).strip()
    expl = re.sub(r'^成语解释[:：]?', '', expl).strip()
    expl = re.sub(r'^【拼音】[^\s]*\s*', '', expl).strip()
    expl = re.sub(r'^成语拼音[：:]\s*\S+\s*', '', expl).strip()
    ex = re.sub(r'^【例句】[:：]?', '', ex).strip()
    ex = re.sub(r'^造句[：:]', '', ex).strip()
    ex = ex.replace('造句：', '').strip()
    idioms.append({'num': num, 'idiom': name, 'explanation': expl, 'example': ex})

print('idioms:', len(idioms))
print('nums:', idioms[0]['num'], '-', idioms[-1]['num'])
missing = [n for n in range(1, 326) if n not in {i['num'] for i in idioms}]
print('missing:', missing)
noex = [i for i in idioms if not i['example']]
print('no example:', len(noex))
for i in noex:
    print('  ', i['num'], i['idiom'], '|', i['explanation'][:40])
noexpl = [i for i in idioms if not i['explanation']]
print('no explanation:', len(noexpl))
for i in noexpl:
    print('  ', i['num'], i['idiom'], '|', i['example'][:40])
print('--- sample ---')
for i in idioms[:3] + idioms[316:]:
    print('  ', i['num'], i['idiom'], '|', i['explanation'][:30], '|', i['example'][:30])

json.dump(idioms, open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms_yjbys.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('saved')
