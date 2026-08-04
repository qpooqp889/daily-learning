# -*- coding: utf-8 -*-
"""Show raw paragraphs near the tail (320+) to fix parsing."""
import re, json

html = open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms_yjbys.html', encoding='utf-8').read()
ps = re.findall(r'<p[^>]*>(.*?)</p>', html, re.S)
ps = [re.sub(r'<[^>]+>', '', p).strip() for p in ps]
ps = [p for p in ps if p]
print('total paragraphs:', len(ps))
for i, p in enumerate(ps):
    if re.match(r'^3(1[5-9]|2[0-5])[､、]', p) or '豺狼' in p or '张灯结彩' in p or '水滴石穿' in p:
        print(f'--- p[{i}] ---')
        print(p[:300])
