# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import add
dw, di = add.find_duplicates()
out = []
if not dw and not di:
    out.append("NO DUP: 沒有重複項目")
else:
    if dw: out.append("重複單字：" + ", ".join(dw))
    if di: out.append("重複成語：" + ", ".join(di))
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp_dupcheck.txt"), "w", encoding="utf-8").write("\n".join(out))
print("done")
