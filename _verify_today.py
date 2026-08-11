# -*- coding: utf-8 -*-
import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
w = json.load(open("data/words.json", encoding="utf-8"))
i = json.load(open("data/idioms.json", encoding="utf-8"))
out = []
out.append("TOTAL words=%d idioms=%d" % (len(w), len(i)))
for x in w[:7]:
    s = x["sentences"][0] if x.get("sentences") else {}
    out.append(f"{x['word']} | {x['pos']} | {x['meaning']} | {x['created_at']} | cam={x.get('cambridge_url','')[:60]}")
    if s:
        out.append(f"    EN: {s['sentence']}")
        out.append(f"    ZH: {s['translation']}")
        out.append(f"    GT: {s['gtranslate_url'][:80]}")
for x in i[:7]:
    out.append(f"{x['idiom']} | {x['category']} | {x['created_at']}")
    out.append(f"    解釋: {x['explanation']}")
    out.append(f"    造句: {x['example']}")
open("_verify_2026-08-11.txt", "w", encoding="utf-8").write("\n".join(out))
print("done")
