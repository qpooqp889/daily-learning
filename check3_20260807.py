# -*- coding: utf-8 -*-
import json, os, unicodedata
base = os.path.dirname(os.path.abspath(__file__))

def norm(s):
    s = unicodedata.normalize("NFC", (s or "").strip())
    s = s.replace(" ", "").replace("\u3000", "")
    return s.casefold()

w = json.load(open(os.path.join(base, "data", "words.json"), encoding="utf-8"))
i = json.load(open(os.path.join(base, "data", "idioms.json"), encoding="utf-8"))

out = []
# 檢查 recycle 的句子
for x in w:
    if x["word"] == "recycle":
        sents = [s["sentence"] for s in x.get("sentences", [])]
        out.append("recycle sentences: " + " || ".join(sents))
        out.append("count: " + str(len(sents)))
        out.append("has today sentence: " + str("We can recycle paper and bottles to help the earth." in sents))

# 確認替代候選是否存在
existing_w = {norm(x["word"]) for x in w}
existing_i = {norm(x["idiom"]) for x in i}
for c in ["solar", "satellite", "rocket", "comet", "microscope", "telescope"]:
    out.append("word " + c + " in db: " + str(norm(c) in existing_w))
for c in ["望塵莫及", "完璧歸趙", "負荊請罪", "朝三暮四", "鷸蚌相爭", "螳螂捕蟬", "天衣無縫", "三顧茅廬", "臥薪嘗膽", "五十步笑百步", "風和日麗", "一鳴驚人"]:
    out.append("idiom " + c + " in db: " + str(norm(c) in existing_i))

open(os.path.join(base, "tmp_check3.txt"), "w", encoding="utf-8").write("\n".join(out))
print("done")
