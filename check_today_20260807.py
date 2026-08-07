# -*- coding: utf-8 -*-
import json, os
base = os.path.dirname(os.path.abspath(__file__))
w = json.load(open(os.path.join(base, "data", "words.json"), encoding="utf-8"))
targets = ["courage", "celebrate", "environment", "science", "discover", "important", "dictionary"]
out = []
for t in targets:
    for x in w:
        if x["word"] == t:
            sents = [s["sentence"] for s in x.get("sentences", [])]
            out.append(t + " (" + str(len(sents)) + " 句): " + " || ".join(sents))
            break
# 檢查今日句子是否重複
today_sents = [
    "She showed great courage when she gave a speech in front of the whole school.",
    "We will celebrate my birthday with a big cake and lots of friends.",
    "We should recycle more to protect the environment.",
    "I learned a lot of interesting things in my science class today.",
    "Scientists discover new things about the ocean every year.",
    "It is important to drink enough water every day.",
    "I looked up the new word in my dictionary.",
]
out.append("")
out.append("今日句子重複檢查：")
all_sents = [s["sentence"] for x in w for s in x.get("sentences", [])]
for s in today_sents:
    out.append(("重複!" if s in all_sents else "OK") + " :: " + s[:60])
open(os.path.join(base, "tmp_sents.txt"), "w", encoding="utf-8").write("\n".join(out))
print("done")
