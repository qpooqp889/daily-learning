# -*- coding: utf-8 -*-
"""Fix specific quality issues found in QA."""
import json

PATH = r'C:\Users\twric\.qclaw\workspace\daily-learning\data\idioms.json'
ids = json.load(open(PATH, encoding='utf-8'))

FIX = {
    "不屈不撓": {
        "explanation": "形容在困難或壓力面前不退縮、不妥協，意志堅定，堅持到底。",
    },
    "同心同德": {
        "explanation": "指大家為了同一個心願、同一個目標而齊心協力，團結一致。多用於褒義。",
    },
    "天荒地老": {
        "explanation": "形容時間極其久遠，也比喻愛情或誓言永遠不變。",
    },
    "花好月圓": {
        "explanation": "花開得好，月亮正圓。比喻生活美滿、團圓幸福，常用來祝賀新婚或喬遷。",
    },
    "艴然不悅": {
        "explanation": "形容臉色大變，非常生氣的樣子。",
    },
    "狼狽為奸": {
        "explanation": "比喻兩個人或兩方互相勾結，一起做壞事。",
    },
    "蛟龍得水": {
        "explanation": "傳說蛟龍得到水就能興雲作雨、飛騰上天。比喻有才能的人獲得施展本領的機會。",
    },
    "情比金堅": {
        "explanation": "形容感情非常堅定，比黃金還要堅固，不會改變。",
    },
    "大千世界": {
        "explanation": "佛教用語，泛指廣大無邊、豐富多樣的世界。",
    },
}

# fix 一日十行 example typo
for i in ids:
    if i['idiom'] == '一日十行' and '一十行' in i.get('example',''):
        i['example'] = i['example'].replace('一十行', '一目十行')
        print('fixed 一日十行 example ->', i['example'][:30])

n = 0
for i in ids:
    if i['idiom'] in FIX:
        fx = FIX[i['idiom']]
        if 'explanation' in fx:
            i['explanation'] = fx['explanation']
        n += 1
        print('fixed:', i['id'], i['idiom'], '->', i['explanation'][:35])

json.dump(ids, open(PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('fixed total:', n, '| saved, total idioms:', len(ids))
