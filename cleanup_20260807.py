# -*- coding: utf-8 -*-
"""移除今天誤加到既有單字的 7 句（這些單字本來就存在，今天新增的句子應撤銷）"""
import json, os
base = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(base, "data", "words.json")
w = json.load(open(path, encoding="utf-8"))

remove_sents = {
    "courage": "She showed great courage when she gave a speech in front of the whole school.",
    "celebrate": "We will celebrate my birthday with a big cake and lots of friends.",
    "environment": "We should recycle more to protect the environment.",
    "science": "I learned a lot of interesting things in my science class today.",
    "discover": "Scientists discover new things about the ocean every year.",
    "important": "It is important to drink enough water every day.",
    "dictionary": "I looked up the new word in my dictionary.",
}

removed = 0
for x in w:
    if x["word"] in remove_sents:
        target = remove_sents[x["word"]]
        before = len(x.get("sentences", []))
        x["sentences"] = [s for s in x.get("sentences", []) if s["sentence"] != target]
        removed += before - len(x["sentences"])

json.dump(w, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("removed sentences:", removed)
