# -*- coding: utf-8 -*-
"""
每日學習資料管理工具（JSON 儲存版）
用法：
  python add.py word <單字> --pos <詞性> --meaning <中文> [--cambridge <網址>]
  python add.py sentence <單字> --en <英文句> --zh <中文> [--gtranslate <網址>]
  python add.py idiom <成語> --explain <解釋> --example <造句>
  python add.py check          # 檢查重複（列出所有重複項目）
  python add.py list           # 列出目前所有資料
每次新增前自動檢查重複（單字不分大小寫、成語完全相同才算重複），重複會跳過。
"""
import json, os, sys, argparse, unicodedata
from datetime import date

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
WORDS_FILE = os.path.join(DATA_DIR, "words.json")
IDIOMS_FILE = os.path.join(DATA_DIR, "idioms.json")

def load(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save(path, data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def norm(s):
    """正規化：去除空白、全形轉半形、統一大小寫，用於比對"""
    s = unicodedata.normalize("NFC", (s or "").strip())
    s = s.replace(" ", "").replace("\u3000", "")
    return s.casefold()

# ---------- 重複檢查 ----------
def find_duplicates():
    words = load(WORDS_FILE)
    idioms = load(IDIOMS_FILE)
    dup_words, dup_idioms = [], []
    seen_w, seen_i = {}, {}
    for w in words:
        key = norm(w["word"])
        if key in seen_w:
            dup_words.append(w["word"])
        else:
            seen_w[key] = w["word"]
    for i in idioms:
        key = norm(i["idiom"])
        if key in seen_i:
            dup_idioms.append(i["idiom"])
        else:
            seen_i[key] = i["idiom"]
    return dup_words, dup_idioms

def word_exists(word):
    return any(norm(w["word"]) == norm(word) for w in load(WORDS_FILE))

def idiom_exists(idiom):
    return any(norm(i["idiom"]) == norm(idiom) for i in load(IDIOMS_FILE))

def next_id(items):
    return max([it.get("id", 0) for it in items], default=0) + 1

# ---------- 新增 ----------
def add_word(word, pos, meaning, cambridge_url):
    word = (word or "").strip()
    if not word:
        return False, "單字不能為空"
    if word_exists(word):
        return False, f"單字「{word}」已存在，跳過儲存"
    words = load(WORDS_FILE)
    words.insert(0, {
        "id": next_id(words), "word": word, "pos": pos or "", "meaning": meaning or "",
        "cambridge_url": cambridge_url or "", "created_at": date.today().isoformat(), "sentences": [],
    })
    save(WORDS_FILE, words)
    return True, f"已儲存單字「{word}」"

def add_sentence(word, sentence, translation, gtranslate_url):
    words = load(WORDS_FILE)
    for w in words:
        if norm(w["word"]) == norm(word):
            w.setdefault("sentences", []).append({
                "id": next_id(w["sentences"]), "sentence": (sentence or "").strip(),
                "translation": (translation or "").strip(),
                "gtranslate_url": gtranslate_url or "", "created_at": date.today().isoformat(),
            })
            save(WORDS_FILE, words)
            return True, f"已儲存句子（單字：{word}）"
    return False, f"找不到單字「{word}」，請先新增單字"

def add_idiom(idiom, explanation, example):
    idiom = (idiom or "").strip()
    if not idiom:
        return False, "成語不能為空"
    if idiom_exists(idiom):
        return False, f"成語「{idiom}」已存在，跳過儲存"
    idioms = load(IDIOMS_FILE)
    idioms.insert(0, {
        "id": next_id(idioms), "idiom": idiom, "explanation": (explanation or "").strip(),
        "example": (example or "").strip(), "created_at": date.today().isoformat(),
    })
    save(IDIOMS_FILE, idioms)
    return True, f"已儲建成語「{idiom}」"

# ---------- CLI ----------
def main():
    p = argparse.ArgumentParser(description="每日學習 JSON 資料管理")
    sub = p.add_subparsers(dest="cmd")

    pw = sub.add_parser("word", help="新增單字")
    pw.add_argument("word")
    pw.add_argument("--pos", default="")
    pw.add_argument("--meaning", default="")
    pw.add_argument("--cambridge", default="")

    ps = sub.add_parser("sentence", help="新增句子")
    ps.add_argument("word")
    ps.add_argument("--en", required=True)
    ps.add_argument("--zh", default="")
    ps.add_argument("--gtranslate", default="")

    pi = sub.add_parser("idiom", help="新增成語")
    pi.add_argument("idiom")
    pi.add_argument("--explain", default="")
    pi.add_argument("--example", default="")

    sub.add_parser("check", help="檢查重複")
    sub.add_parser("list", help="列出資料")

    args = p.parse_args()
    if args.cmd == "word":
        print(add_word(args.word, args.pos, args.meaning, args.cambridge)[1])
    elif args.cmd == "sentence":
        print(add_sentence(args.word, args.en, args.zh, args.gtranslate)[1])
    elif args.cmd == "idiom":
        print(add_idiom(args.idiom, args.explain, args.example)[1])
    elif args.cmd == "check":
        dw, di = find_duplicates()
        if not dw and not di:
            print("✅ 沒有重複項目")
        else:
            if dw: print("重複單字：", dw)
            if di: print("重複成語：", di)
    elif args.cmd == "list":
        words = load(WORDS_FILE)
        idioms = load(IDIOMS_FILE)
        print(f"單字 {len(words)} 筆、成語 {len(idioms)} 筆")
        for w in words:
            print(f"  📝 {w['word']} ({w['pos']}) {w['meaning']} — {len(w.get('sentences', []))} 句")
        for i in idioms:
            print(f"  🀄 {i['idiom']} — {i['explanation']}")
    else:
        p.print_help()

if __name__ == "__main__":
    main()
