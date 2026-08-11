# -*- coding: utf-8 -*-
import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
w = json.load(open("data/words.json", encoding="utf-8"))
out = []
keys = set()
for x in w[:30]:
    keys.update(x.keys())
out.append("keys in recent words: " + str(sorted(keys)))
n_with_cam = sum(1 for x in w if x.get("cambridge_url"))
out.append("entries with cambridge_url: %d / %d" % (n_with_cam, len(w)))
n_with_gt = sum(1 for x in w if x.get("gtranslate_url"))
out.append("entries with gtranslate_url: %d / %d" % (n_with_gt, len(w)))
open("_check_cam.txt", "w", encoding="utf-8").write("\n".join(out))
print("done")
