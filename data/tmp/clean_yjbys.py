# -*- coding: utf-8 -*-
"""Final clean: fix 322/324 pinyin leftovers, trim trailing junk."""
import re, json

idioms = json.load(open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms_yjbys.json', encoding='utf-8'))

for i in idioms:
    e = i['explanation']
    if i['num'] == 322:  # 举措失当
        e = re.sub(r'^jǔ cu shī dàng\s*【解释】[:：]?\s*', '', e)
    if i['num'] == 324:  # 如醉如痴
        e = re.sub(r'^zuì rú chī\s*成语解释[:：]?\s*', '', e)
    e = re.sub(r'\s*【成语故事】.*$', '', e)
    e = re.sub(r'\s*成语故事或出处.*$', '', e)
    i['explanation'] = e.strip()
    # example: strip trailing source junk
    x = i['example']
    x = re.sub(r'\s*：\s*此人枭獍.*$', '', x)
    x = re.sub(r'\s*【出处】.*$', '', x)
    x = re.sub(r'\s*【成语故事】.*$', '', x)
    i['example'] = x.strip()

for i in idioms:
    if re.search(r'[a-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]', i['explanation']):
        print('PINYIN LEFT:', i['num'], i['idiom'], '|', i['explanation'][:60])
    if '相关文章' in i['example'] or '成语解释及造句' in i['example']:
        print('JUNK EXAMPLE:', i['num'], i['idiom'])
    if '【' in i['explanation']:
        print('BRACKET EXPL:', i['num'], i['idiom'], '|', i['explanation'][:60])

print('--- 322/324/325 ---')
for i in idioms:
    if i['num'] in (322, 323, 324, 325):
        print('  ', i['num'], i['idiom'], '|', i['explanation'][:50], '|', i['example'][:50])

json.dump(idioms, open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms_yjbys.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('saved')
