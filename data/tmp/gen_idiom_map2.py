# -*- coding: utf-8 -*-
"""Regenerate IDIOM_CAT_MAP in add.py from idioms.json (full 892-entry table)."""
import json, re, io

IDS = r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms.json'
ADD = r'C:\Users\twric\.qclaw\workspace\daily-learning\add.py'

ids = json.load(open(IDS, encoding='utf-8'))
pairs = [(i['idiom'], i['category']) for i in ids if i.get('category')]
print('pairs:', len(pairs))

# build map literal text
lines = ['IDIOM_CAT_MAP = {']
for n in range(0, len(pairs), 4):
    chunk = pairs[n:n+4]
    line = ', '.join(f'"{a}": "{b}"' for a, b in chunk)
    lines.append('    ' + line + (',' if n + 4 < len(pairs) else ''))
lines.append('}')
new_map = '\n'.join(lines)

add = io.open(ADD, encoding='utf-8').read()

# find existing IDIOM_CAT_MAP block and replace
m = re.search(r'IDIOM_CAT_MAP = \{[^}]*\}', add, re.S)
assert m, 'IDIOM_CAT_MAP not found'
print('old map size:', len(m.group(0)))
add = add[:m.start()] + new_map + add[m.end():]
io.open(ADD, 'w', encoding='utf-8', newline='').write(add)
print('new map size:', len(new_map))

# sanity: import add and check a few
import importlib.util
spec = importlib.util.spec_from_file_location('add', ADD)
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
print('map entries:', len(a.IDIOM_CAT_MAP))
for k in ['開卷有益', '浮光掠影', '石破天驚', '狗急跳牆', '朝三暮四']:
    print(' ', k, '->', a.guess_idiom_cat(k, ''))
