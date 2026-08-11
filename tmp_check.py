# -*- coding: utf-8 -*-
import sys, json
sys.stdout.reconfigure(encoding='utf-8')
d = json.load(open('data/words.json', encoding='utf-8'))
di = json.load(open('data/idioms.json', encoding='utf-8'))
existing_w = {w['word'].lower() for w in d}
existing_i = {i['idiom'] for i in di}

cands_w = ['earthquake','volcano','rescue','ambulance','museum','planet','costume','celebrate','tradition','harvest','surprised','delicious','protect','environment','island','temple','polite','stranger','memory','brave']
cands_i = ['畫蛇添足','井底之蛙','對牛彈琴','守株待兔','亡羊補牢','拔苗助長','半途而廢','一毛不拔','心想事成','一鳴驚人','再接再厲','精益求精','廢寢忘食','聚沙成塔','水滴石穿','臥薪嘗膽','負荊請罪','望梅止渴','狐假虎威','刻舟求劍']

with open('check_dup_out.txt','w',encoding='utf-8') as f:
    f.write('=== WORDS missing (safe to add) ===\n')
    for w in cands_w:
        f.write(f"{w}: {'EXISTS' if w in existing_w else 'ok'}\n")
    f.write('=== IDIOMS missing (safe to add) ===\n')
    for i in cands_i:
        f.write(f"{i}: {'EXISTS' if i in existing_i else 'ok'}\n")
    f.write('=== LAST 10 WORDS ===\n')
    for w in d[-10:]:
        f.write(f"{w['word']} | {w.get('pos','')} | {w.get('meaning','')}\n")
    f.write('=== LAST 10 IDIOMS ===\n')
    for i in di[-10:]:
        f.write(f"{i['idiom']} | {i.get('explanation','')}\n")
print('done')
