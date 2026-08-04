# -*- coding: utf-8 -*-
"""Fix broken getPet (async got separated by helper insertion)."""
import io

p = r'C:\Users\twric\.qclaw\workspace\daily-learning\index.html'
html = io.open(p, encoding='utf-8').read()

bad = """async 
function xpMultiplier(p) {"""
good = """function xpMultiplier(p) {"""
if bad in html:
    html = html.replace(bad, good, 1)
    print('fixed async split #1')

bad2 = "async \nfunction getPet() {"
if bad2 in html:
    html = html.replace(bad2, "async function getPet() {", 1)
    print('fixed async split #2')

# also check for any other stray "async \nfunction"
import re
stray = re.findall(r'async\s*\n\s*function', html)
print('stray async splits:', len(stray))

io.open(p, 'w', encoding='utf-8', newline='').write(html)

# verify getPet region
i = html.find('function xpMultiplier')
print(html[i-30:i+320])
