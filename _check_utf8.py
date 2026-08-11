# -*- coding: utf-8 -*-
import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
w = json.load(open("data/words.json", encoding="utf-8"))
samples = w[:5]
ok = all(any("\u4e00" <= ch <= "\u9fff" for ch in (x.get("meaning") or "")) for x in samples)
out = ["chinese ok: " + str(ok)]
for x in samples:
    out.append(repr(x["word"]) + " | " + repr(x["meaning"]))
open("_check_utf8.txt", "w", encoding="utf-8").write("\n".join(out))
print("done")
