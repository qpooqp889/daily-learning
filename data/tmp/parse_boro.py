# -*- coding: utf-8 -*-
"""Re-parse correctly-downloaded boroenglish HTML and re-import into words.json."""
import re, json, html, urllib.parse, datetime

SRC = r'C:\Users\twric\.qclaw\workspace\daily-learning\data\boro_gept.html'
DATA = r'C:\Users\twric\.qclaw\workspace\daily-learning\data\words.json'

html_src = open(SRC, encoding='utf-8').read()
m = re.search(r'<div[^>]*class="[^"]*entry-content[^"]*"[^>]*>(.*?)</div>\s*(?:<footer|</article)', html_src, re.S)
if not m:
    m = re.search(r'<div[^>]*class="[^"]*entry-content[^"]*"[^>]*>(.*)', html_src, re.S)
content = m.group(1) if m else html_src

tables = re.findall(r'<table.*?</table>', content, re.S)
print('tables:', len(tables))

POS_MAP = {
    '名詞': 'n.', '動詞': 'v.', '形容詞': 'a.', '副詞': 'ad.',
    '介系詞': 'prep.', '連接詞': 'conj.', '代名詞': 'pron.',
    '冠詞': 'art.', '感嘆詞': 'interj.', '縮寫': 'abbr.',
    '數字': 'num.', '限定詞': 'det.',
}

def norm_pos(pos_raw):
    pos_raw = pos_raw.strip().rstrip('．.')
    if not pos_raw:
        return ''
    parts = re.split(r'[/／、]', pos_raw)
    out = []
    for p in parts:
        p = p.strip()
        out.append(POS_MAP.get(p, p))
    return '/'.join(out)

rows = []
for t in tables[1:]:
    for r in re.findall(r'<tr[^>]*>(.*?)</tr>', t, re.S):
        cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', r, re.S)
        cells = [html.unescape(re.sub(r'<[^>]+>', '', c)).strip() for c in cells]
        if len(cells) < 4:
            continue
        word, pos, phon, meaning = cells[0], cells[1], cells[2], cells[3]
        if word in ('單字', '詞性', '音標', '解釋') or not word:
            continue
        rows.append({'word': word, 'pos': norm_pos(pos), 'phonetic': phon, 'meaning': meaning})

print('parsed rows:', len(rows))
# sanity check sample
for w in rows[:3]:
    print('  ', w)
for w in rows[-3:]:
    print('  ', w)

# Merge multi-pos rows
merged = {}
for w in rows:
    key = w['word'].strip().lower()
    if key not in merged:
        merged[key] = dict(w)
    else:
        m2 = merged[key]
        if w['pos'] and w['pos'] not in m2['pos'].split('/'):
            m2['pos'] = (m2['pos'] + '/' + w['pos']) if m2['pos'] else w['pos']
        if w['meaning'] and w['meaning'] not in m2['meaning'].split('；'):
            m2['meaning'] = (m2['meaning'] + '；' + w['meaning']) if m2['meaning'] else w['meaning']
print('unique words:', len(merged))

# Save merged as boro_words.json (fixed)
with open(r'C:\Users\twric\.qclaw\workspace\daily-learning\data\boro_words.json', 'w', encoding='utf-8') as f:
    json.dump(list(merged.values()), f, ensure_ascii=False, indent=1)
print('saved boro_words.json (fixed)')
