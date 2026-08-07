# -*- coding: utf-8 -*-
"""2026-08-07 每日學習內容（全新項目）寫入"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import add

results = []

# ---------- 英文單字 7 個（全新） ----------
words = [
    ("invention", "n.", "發明", "https://dictionary.cambridge.org/zht/詞典/英語-漢語-繁體/invention"),
    ("earthquake", "n.", "地震", "https://dictionary.cambridge.org/zht/詞典/英語-漢語-繁體/earthquake"),
    ("experiment", "n.", "實驗", "https://dictionary.cambridge.org/zht/詞典/英語-漢語-繁體/experiment"),
    ("laboratory", "n.", "實驗室", "https://dictionary.cambridge.org/zht/詞典/英語-漢語-繁體/laboratory"),
    ("spaceship", "n.", "太空船", "https://dictionary.cambridge.org/zht/詞典/英語-漢語-繁體/spaceship"),
    ("recycle", "v.", "回收；再利用", "https://dictionary.cambridge.org/zht/詞典/英語-漢語-繁體/recycle"),
    ("generate", "v.", "產生；發電", "https://dictionary.cambridge.org/zht/詞典/英語-漢語-繁體/generate"),
]
for w, pos, mean, cam in words:
    results.append(add.add_word(w, pos, mean, cam))

# ---------- 英文例句 7 句 ----------
sentences = [
    ("invention", "The telephone was a great invention that changed the world.",
     "電話是一項改變世界的偉大發明。"),
    ("earthquake", "The earthquake shook the whole city, so everyone ran outside.",
     "地震搖晃了整座城市，所以大家都跑到外面。"),
    ("experiment", "We did a science experiment to see how plants grow.",
     "我們做了一個科學實驗，觀察植物如何生長。"),
    ("laboratory", "The scientists work in a big laboratory every day.",
     "科學家們每天都在一間很大的實驗室裡工作。"),
    ("spaceship", "The spaceship flew to the moon and came back safely.",
     "太空船飛到月球，然後安全地回來了。"),
    ("recycle", "We can recycle paper and bottles to help the earth.",
     "我們可以回收紙類和寶特瓶來幫助地球。"),
    ("generate", "Solar panels use sunlight to generate electricity.",
     "太陽能板利用陽光來發電。"),
]
for w, en, zh in sentences:
    gurl = "https://translate.google.com/?hl=zh-TW&eotf=0&sl=en&tl=zh-TW&text={}&op=translate".format(
        en.replace(" ", "%20").replace("'", "%E2%80%99"))
    results.append(add.add_sentence(w, en, zh, gurl))

# ---------- 成語 7 則（全新） ----------
idioms = [
    ("一見如故", "初次見面就像老朋友一樣，形容彼此非常投緣。",
     "新同學跟我一見如故，聊沒幾句就變成好朋友了。"),
    ("口若懸河", "形容說話流利，滔滔不絕，像瀑布傾瀉一樣。",
     "他上台演講時口若懸河，讓台下的同學都聽得入迷。"),
    ("中流砥柱", "比喻在艱難環境中，能支撐大局、扭轉情勢的重要人物。",
     "隊長在球隊最危急的時候挺身而出，是名副其實的中流砥柱。"),
    ("五光十色", "形容色彩鮮豔、花樣繁多。",
     "跨年夜的煙火五光十色，照亮了整個夜空。"),
    ("刻舟求劍", "比喻拘泥固執、不知變通，用老方法解決新問題。",
     "時代一直在改變，如果還用舊觀念做事，就像刻舟求劍一樣可笑。"),
    ("杯弓蛇影", "比喻疑神疑鬼，把不存在的事情當成真的而自相驚擾。",
     "他聽到一點聲響就以為有小偷，真是杯弓蛇影、自己嚇自己。"),
    ("樂極生悲", "快樂到了極點，反而容易發生悲傷的事情。",
     "弟弟在公園玩得太開心，樂極生悲，不小心摔了一跤。"),
]
for i, ex, eg in idioms:
    results.append(add.add_idiom(i, ex, eg))

# ---------- 輸出結果 ----------
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "add_result.txt"), "w", encoding="utf-8") as f:
    for r in results:
        f.write(r[1] + "\n")
print("DONE", len(results), "operations")
