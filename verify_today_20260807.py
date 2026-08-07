# -*- coding: utf-8 -*-
import json, os
base = os.path.dirname(os.path.abspath(__file__))
w = json.load(open(os.path.join(base, "data", "words.json"), encoding="utf-8"))
i = json.load(open(os.path.join(base, "data", "idioms.json"), encoding="utf-8"))

today_words = ["invention", "earthquake", "experiment", "laboratory", "spaceship", "solar", "generate"]
today_idioms = ["一見如故", "口若懸河", "中流砥柱", "五光十色", "樂極生悲", "望塵莫及", "完璧歸趙"]

out = []
out.append("=== 今日單字 ===")
for t in today_words:
    for x in w:
        if x["word"] == t:
            sents = x.get("sentences", [])
            out.append(f"{x['word']} ({x['pos']}) {x['meaning']} | 例句 {len(sents)} 句 | gtranslate: {x.get('gtranslate_url','')[:80]}")
            for s in sents:
                out.append(f"    - {s['sentence']} / {s['translation']}")
            break

out.append("=== 今日成語 ===")
for t in today_idioms:
    for x in i:
        if x["idiom"] == t:
            out.append(f"{x['idiom']} [{x.get('category','')}] {x['explanation']} | 例：{x['example']}")
            break

open(os.path.join(base, "tmp_verify.txt"), "w", encoding="utf-8").write("\n".join(out))
print("done")
