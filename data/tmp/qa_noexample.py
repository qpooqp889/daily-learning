# -*- coding: utf-8 -*-
"""Check idioms without example (sentence)."""
import json

ids = json.load(open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms.json', encoding='utf-8'))
print('total idioms:', len(ids))

no_ex = [i for i in ids if not i.get('example') or not i['example'].strip()]
print('no example:', len(no_ex))

# Also check placeholder/template examples
import re
tpl_pat = re.compile(r'(他這樣的做法|這件事讓大家體會到|老師用|面對這種情況|他的表現可說是|最適合形容|的具體寫照|來提醒我們|的道理)')
tpl = [i for i in ids if tpl_pat.search(i.get('example',''))]
print('template/placeholder examples:', len(tpl))

print()
print('=== idioms WITHOUT example ===')
for i in no_ex:
    print('  {} {} | {}'.format(i['id'], i['idiom'], i.get('explanation','')[:30]))

print()
print('=== template examples (needs real sentence) ===')
for i in tpl:
    print('  {} {} | {}'.format(i['id'], i['idiom'], i['example'][:40]))
