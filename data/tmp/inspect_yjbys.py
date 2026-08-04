# -*- coding: utf-8 -*-
"""Inspect yjbys idioms HTML structure."""
import re

html = open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms_yjbys.html', encoding='utf-8').read()
print('len:', len(html))
# Check charset
m = re.search(r'charset=["\']?([\w-]+)', html[:2000])
print('charset:', m.group(1) if m else '?')
# Find main content
for pat in [r'<div[^>]*class="[^"]*(?:article|content|text)[^"]*"[^>]*>', r'<p[^>]*>']:
    ms = re.findall(pat, html)
    print(pat, '->', len(ms))
# Extract paragraphs sample
ps = re.findall(r'<p[^>]*>(.*?)</p>', html, re.S)
print('p sample:')
for p in ps[:10]:
    t = re.sub(r'<[^>]+>', '', p).strip()
    if t:
        print('  ', t[:80])
