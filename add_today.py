# -*- coding: utf-8 -*-
"""每日學習內容批次新增：呼叫 add.py 加入單字/句子/成語"""
import subprocess, sys, json, urllib.parse, os
sys.stdout.reconfigure(encoding='utf-8')

BASE = os.path.dirname(os.path.abspath(__file__))
ADD = os.path.join(BASE, 'add.py')

def gurl(sentence):
    # 空格用 %20、撇號用 %E2%80%99，其餘做 URL 編碼
    s = sentence.replace(' ', '%20').replace("'", '%E2%80%99')
    return "https://translate.google.com/?hl=zh-TW&eotf=0&sl=en&tl=zh-TW&text={}&op=translate".format(s)

def cambridge(word):
    return "https://dictionary.cambridge.org/zht/詞典/英語-漢語-繁體/{}".format(word)

def run(args):
    r = subprocess.run([sys.executable, ADD] + args, capture_output=True, text=True, encoding='utf-8')
    out = (r.stdout or '').strip() or (r.stderr or '').strip()
    print(out)
    return r.returncode

# ============ 今日內容 ============
words = [
    ("rescue", "v.", "拯救；營救"),
    ("kindness", "n.", "善良；仁慈"),
    ("breathe", "v.", "呼吸"),
    ("finally", "adv.", "最後；終於"),
    ("voyage", "n.", "航行；航海"),
    ("harvest", "n./v.", "收穫；收割"),
    ("compass", "n.", "指南針；羅盤"),
]

sentences = [
    ("rescue", "The firefighter helped rescue the cat from the tree.", "消防員幫忙從樹上救下那隻貓。"),
    ("kindness", "Her kindness made everyone feel welcome.", "她的善良讓每個人都感到受歡迎。"),
    ("breathe", "Please breathe slowly and deeply.", "請慢慢地深呼吸。"),
    ("finally", "We finally finished our homework.", "我們終於完成了功課。"),
    ("voyage", "The ship began its long voyage across the sea.", "那艘船開始了橫越海洋的漫長航行。"),
    ("harvest", "Farmers harvest the rice in autumn.", "農夫在秋天收割稻米。"),
    ("compass", "A compass helps us find our way in the forest.", "指南針幫助我們在森林裡找到方向。"),
]

idioms = [
    ("一鳴驚人", "比喻平時沒有特殊表現，一有舉動就令人吃驚。", "他平常很少說話，這次演講比賽卻一鳴驚人，得了全校第一名。"),
    ("春暖花開", "春天氣候溫暖，百花盛開，形容春天的美景。", "春暖花開的時候，我們全家到陽明山賞花。"),
    ("苦口婆心", "形容勸說別人時非常懇切、有耐心。", "老師苦口婆心地勸我們要好好用功，不要浪費時間。"),
    ("得心應手", "心裡怎麼想，手就能怎麼做，形容做事非常熟練。", "她練習鋼琴多年，彈奏這首曲子已經得心應手。"),
    ("望梅止渴", "比喻用空想來安慰自己，無法解決實際問題。", "他沒錢買遊戲機，只好看著圖片望梅止渴。"),
    ("聚沙成塔", "把細沙堆積成高塔，比喻積少成多。", "每天存十塊錢，聚沙成塔，一年後也是一筆不小的數目。"),
    ("鶴立雞群", "比喻一個人的才能或儀表在眾人中特別突出。", "小明長得高又帥，站在人群裡就像鶴立雞群。"),
]

# ============ 執行 ============
print("=== 單字 ===")
for w, pos, meaning in words:
    run(["word", w, "--pos", pos, "--meaning", meaning, "--cambridge", cambridge(w)])

print("=== 句子 ===")
for w, en, zh in sentences:
    run(["sentence", w, "--en", en, "--zh", zh, "--gtranslate", gurl(en)])

print("=== 成語 ===")
for i, ex, eg in idioms:
    run(["idiom", i, "--explain", ex, "--example", eg])

print("=== 完成 ===")
