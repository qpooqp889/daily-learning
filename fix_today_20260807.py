# -*- coding: utf-8 -*-
"""修正：移除 recycle 誤加的句子，改以全新單字 solar 取代；補上 2 個新成語"""
import json, os, sys
base = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base)
import add

results = []

# 1. 移除 recycle 的今日句子
path = os.path.join(base, "data", "words.json")
w = json.load(open(path, encoding="utf-8"))
target = "We can recycle paper and bottles to help the earth."
for x in w:
    if x["word"] == "recycle":
        before = len(x.get("sentences", []))
        x["sentences"] = [s for s in x.get("sentences", []) if s["sentence"] != target]
        results.append("recycle 句子清理：" + str(before - len(x["sentences"])) + " 句已移除")
json.dump(w, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# 2. 新增單字 solar
results.append(add.add_word("solar", "adj.", "太陽的；太陽能的",
    "https://dictionary.cambridge.org/zht/詞典/英語-漢語-繁體/solar")[1])
solar_en = "The solar panels on our roof give us clean energy."
solar_zh = "我們屋頂上的太陽能板為我們提供乾淨的能源。"
gurl = "https://translate.google.com/?hl=zh-TW&eotf=0&sl=en&tl=zh-TW&text={}&op=translate".format(
    solar_en.replace(" ", "%20").replace("'", "%E2%80%99"))
results.append(add.add_sentence("solar", solar_en, solar_zh, gurl)[1])

# 3. 新增 2 個新成語
results.append(add.add_idiom("望塵莫及", "比喻遠遠落後，怎麼追也追不上。",
    "他跑得實在太快了，我怎麼追都望塵莫及。")[1])
results.append(add.add_idiom("完璧歸趙", "比喻把物品原封不動地歸還給原主。",
    "我向他借的書已經看完，現在完璧歸趙，還給你。")[1])

with open(os.path.join(base, "add_result2.txt"), "w", encoding="utf-8") as f:
    for r in results:
        f.write(r + "\n")
print("DONE")
