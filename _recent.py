# -*- coding: utf-8 -*-
import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
w = json.load(open("data/words.json", encoding="utf-8"))
i = json.load(open("data/idioms.json", encoding="utf-8"))
out = ["recent words:"]
for x in w[:25]:
    out.append(f"{x['word']} | {x['pos']} | {x['meaning']} | {x['created_at']}")
out.append("recent idioms:")
for x in i[:25]:
    out.append(f"{x['idiom']} | {x['created_at']}")
open("_recent.txt", "w", encoding="utf-8").write("\n".join(out))
print("done")
