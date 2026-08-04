# -*- coding: utf-8 -*-
"""Extract GEPT Elementary word list from PDF."""
import sys, json, re
from pypdf import PdfReader

src = r'C:\Users\twric\.qclaw\workspace\daily-learning\data\gtec_raw.bin'
out_txt = r'C:\Users\twric\.qclaw\workspace\daily-learning\data\gtec_full.txt'

reader = PdfReader(src)
print('pages:', len(reader.pages))
lines = []
for i, page in enumerate(reader.pages):
    try:
        t = page.extract_text() or ''
    except Exception as e:
        print('page', i, 'error:', e)
        t = ''
    lines.append(t)

full = '\n'.join(lines)
with open(out_txt, 'w', encoding='utf-8') as f:
    f.write(full)
print('chars:', len(full))
print('--- first 1500 chars ---')
print(full[:1500])
