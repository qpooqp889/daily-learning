# -*- coding: utf-8 -*-
import json, os, unicodedata
base = os.path.dirname(os.path.abspath(__file__))

def norm(s):
    s = unicodedata.normalize("NFC", (s or "").strip())
    s = s.replace(" ", "").replace("\u3000", "")
    return s.casefold()

w = json.load(open(os.path.join(base, "data", "words.json"), encoding="utf-8"))
i = json.load(open(os.path.join(base, "data", "idioms.json"), encoding="utf-8"))
existing_w = {norm(x["word"]) for x in w}
existing_i = {norm(x["idiom"]) for x in i}

word_cands = ["generous", "patient", "prepare", "protect", "imagine", "succeed", "memory",
              "ancient", "explore", "future", "knowledge", "compare", "achieve", "encourage",
              "invention", "journey", "opportunity", "believe", "famous", "different",
              "history", "language", "maybe", "together"]
idiom_cands = ["風和日麗", "天衣無縫", "三顧茅廬", "臥薪嘗膽", "五十步笑百步", "杯水車薪",
               "完璧歸趙", "負荊請罪", "望塵莫及", "朝三暮四", "鷸蚌相爭", "螳螂捕蟬",
               "雪中送炭", "名副其實", "樂極生悲", "一箭雙鵰", "入木三分", "打草驚蛇",
               "亡羊補牢", "守株待兔", "揠苗助長", "畫蛇添足", "井底之蛙", "對牛彈琴",
               "破釜沉舟", "鐵杵磨針", "不恥下問", "一諾千金", "廢寢忘食", "奮不顧身"]

out = []
out.append("新單字候選（不在資料庫中）：")
for c in word_cands:
    out.append(("OK  " if norm(c) not in existing_w else "已有") + " " + c)
out.append("")
out.append("新成語候選（不在資料庫中）：")
for c in idiom_cands:
    out.append(("OK  " if norm(c) not in existing_i else "已有") + " " + c)
open(os.path.join(base, "tmp_cands.txt"), "w", encoding="utf-8").write("\n".join(out))
print("done")
