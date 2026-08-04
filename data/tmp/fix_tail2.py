# -*- coding: utf-8 -*-
"""Manually fix entries 322/324."""
import json

idioms = json.load(open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms_yjbys.json', encoding='utf-8'))
for i in idioms:
    if i['num'] == 322:
        i['explanation'] = '举措：举动，措置。指行动措施不得当。'
    if i['num'] == 324:
        i['explanation'] = '形容神态失常，失去自制。'
        i['example'] = '元·马致远《汉宫秋》第二折中就有「如醉如痴」的用法。'
    if i['num'] == 323 and not i['example']:
        i['example'] = '古典音乐虽然高雅，但对一般人来说可能像阳春白雪一样难以欣赏。'
    if i['num'] == 325 and not i['example']:
        i['example'] = '春节将至，家家户户张灯结彩，到处洋溢着喜庆的气氛。'
for i in idioms:
    if i['num'] in (322, 323, 324, 325):
        print('  ', i['num'], i['idiom'], '|', i['explanation'][:50], '|', i['example'][:50])
json.dump(idioms, open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms_yjbys.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('saved')
