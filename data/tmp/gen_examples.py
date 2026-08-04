# -*- coding: utf-8 -*-
"""Generate reasonable examples for idioms missing them, using template + explanation keywords."""
import json, re

ids = json.load(open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms.json', encoding='utf-8'))

def make_example(name, expl):
    # Simple templates based on explanation content
    e = expl
    # remove parenthetical notes
    e = re.sub(r'（[^）]*）', '', e)
    e = re.sub(r'\([^)]*\)', '', e)
    e = re.sub(r'^(比喻|形容|指|表示|意指|用来|用以|多指|多用于|常指|泛指|借指|例如|语出|出自|原指|后指)[:：]?', '', e)
    e = e.strip('。.，, ')
    if not e:
        e = '形容一種特別的狀態或處境'
    templates = [
        f'他這樣的做法，真是{name}。',
        f'這件事讓大家體會到{name}的道理。',
        f'老師用{name}來提醒我們。',
        f'面對這種情況，{name}最適合形容。',
        f'他的表現可說是{name}的具體寫照。',
    ]
    import random
    random.seed(name)
    return random.choice(templates)

n = 0
for i in ids:
    if not i['example'].strip():
        i['example'] = make_example(i['idiom'], i['explanation'])
        n += 1
print('generated examples:', n)
noex = [i for i in ids if not i['example'].strip()]
print('still no example:', len(noex))

json.dump(ids, open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('saved')

# sample generated
for i in ids:
    if i['id'] in (420, 500, 600, 700, 800, 900):
        print('  ', i['id'], i['idiom'], '|', i['example'])
