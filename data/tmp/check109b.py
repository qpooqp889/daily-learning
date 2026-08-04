# -*- coding: utf-8 -*-
import json
ws = json.load(open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\words.json', encoding='utf-8'))
byid = {w['id']: w for w in ws}
out = []
for i in (109, 110, 111, 112):
    w = byid.get(i)
    if not w:
        continue
    out.append('id=%d word=%r codepoints=%s' % (i, w['word'], [hex(ord(c)) for c in w['word']]))
    out.append('   pos=%r meaning=%r' % (w['pos'], w['meaning']))
open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\report109.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('ok')
