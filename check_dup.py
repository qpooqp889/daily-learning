# -*- coding: utf-8 -*-
import json, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
WORDS_FILE = os.path.join(DATA_DIR, "words.json")
IDIOMS_FILE = os.path.join(DATA_DIR, "idioms.json")

def load(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def norm(s):
    import unicodedata
    s = unicodedata.normalize("NFC", (s or "").strip())
    s = s.replace(" ", "").replace("\u3000", "")
    return s.casefold()

words = load(WORDS_FILE)
idioms = load(IDIOMS_FILE)
existing_w = {norm(w['word']) for w in words}
existing_i = {norm(i['idiom']) for i in idioms}

cand_words = ['splendid', 'recycle', 'ecology', 'generous', 'curious', 'adventure', 'protect', 'pollution', 'collect', 'donate', 'rescue', 'discover', 'imagine', 'courage', 'polite', 'responsible', 'scientist', 'astronaut', 'library', 'knowledge']
print("== WORDS ==")
for w in cand_words:
    print(w, "-> EXISTS" if norm(w) in existing_w else "-> NEW")

cand_idioms = ['精益求精', '不恥下問', '胸有成竹', '一帆風順', '心想事成', '水滴石穿', '愚公移山', '半途而廢', '鍥而不捨', '畫龍點睛', '井井有條', '專心致志', '勤能補拙', '溫故知新', '學以致用', '百折不撓', '廢寢忘食', '手不釋卷', '舉一反三', '融會貫通', '全神貫注', '循序漸進', '日積月累', '腳踏實地']
print("== IDIOMS ==")
for i in cand_idioms:
    print(i, "-> EXISTS" if norm(i) in existing_i else "-> NEW")
