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
from urllib.parse import quote

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

# ---------- 自動分類（新資料自動歸類，無法判斷時用預設） ----------
WORD_TOPIC_KEYWORDS = {
    "動物": ["animal", "cat", "dog", "bird", "fish", "panda", "tiger", "zoo", "farm", "pet"],
    "食物": ["food", "eat", "apple", "banana", "orange", "breakfast", "lunch", "dinner", "fruit", "juice", "snack", "cake", "rice", "milk", "egg", "bread", "hungry", "thirsty"],
    "學校": ["school", "teacher", "student", "homework", "class", "library", "learn", "study", "read", "write", "exam", "test"],
    "家庭生活": ["family", "home", "house", "mom", "dad", "sister", "brother", "neighbor", "clean", "cook", "help", "room"],
    "健康運動": ["run", "swim", "sport", "exercise", "healthy", "doctor", "hospital", "strong", "sleep", "walk", "body"],
    "自然環境": ["tree", "flower", "plant", "mountain", "ocean", "river", "forest", "weather", "sun", "rain", "season", "spring", "summer", "winter"],
    "旅行休閒": ["travel", "trip", "visit", "park", "beach", "holiday", "weekend", "play", "game", "music", "movie", "dance", "sing"],
    "心情感受": ["happy", "sad", "angry", "lucky", "wonderful", "worry", "afraid", "kind", "like", "love", "favorite", "beautiful"],
}
def guess_word_topic(word):
    w = (word or "").lower()
    for topic, kws in WORD_TOPIC_KEYWORDS.items():
        if any(k in w for k in kws):
            return topic
    return "其他"

IDIOM_CAT_KEYWORDS = {
    "勤學": ["學", "書", "習", "讀", "練", "溫故", "專心", "勤", "思"],
    "勵志": ["志", "成", "努", "堅", "勇", "恆", "前進"],
    "為人": ["人", "德", "信", "誠", "助", "謙", "善"],
    "處世": ["事", "謀", "智", "機", "變", "識"],
    "警示": ["莫", "勿", "戒", "防", "危", "錯", "誤", "慎", "忌"],
}
# 已知成語分類對照表（新成語優先查表，查不到才用關鍵字猜）
IDIOM_CAT_MAP = {
    "開卷有益": "勤學", "逆水行舟": "勤學", "捷足先登": "處世", "名列前茅": "勵志",
    "半信半疑": "情境", "從善如流": "為人", "有志竟成": "勵志", "名副其實": "為人",
    "一心一德": "為人", "囫圇吞棗": "警示", "翻山越嶺": "勵志", "點石成金": "處世",
    "聲東擊西": "處世", "舉一反三": "勤學", "臨危不亂": "處世", "豁然開朗": "情境",
    "謙虛謹慎": "為人", "錦上添花": "處世", "隨機應變": "處世", "龍飛鳳舞": "情境",
    "機不可失": "勵志", "獨一無二": "情境", "融會貫通": "勤學", "學以致用": "勤學",
    "熱心助人": "為人", "熟能生巧": "勤學", "滴水穿石": "勤學", "聚精會神": "勤學",
    "精益求精": "勤學", "聞雞起舞": "勤學", "旗鼓相當": "情境", "感恩圖報": "為人",
    "塞翁失馬": "處世", "愚公移山": "勵志", "登峰造極": "勵志", "無中生有": "警示",
    "畫餅充飢": "警示", "異想天開": "警示", "斬草除根": "處世", "掩耳盜鈴": "警示",
    "雪中送炭": "為人", "笨鳥先飛": "勤學", "眼高手低": "警示", "理直氣壯": "為人",
    "欲速則不達": "警示", "紙上談兵": "警示", "笑裡藏刀": "警示", "馬到成功": "勵志",
    "破釜沉舟": "勵志", "乘風破浪": "勵志", "飛黃騰達": "勵志", "赴湯蹈火": "勵志",
    "挖空心思": "勤學", "柳暗花明": "勵志", "南轅北轍": "警示", "迫不得已": "情境",
    "狐假虎威": "警示", "狗急跳牆": "情境", "金玉良言": "為人", "畫龍點睛": "處世",
    "刻舟求劍": "警示", "東施效顰": "警示", "杯弓蛇影": "警示", "拔苗助長": "警示",
    "花言巧語": "警示", "走馬看花": "警示", "見多識廣": "處世", "事倍功半": "勤學",
    "事半功倍": "勤學", "安居樂業": "情境", "老馬識途": "處世", "有口皆碑": "為人",
    "有始有終": "勤學", "百發百中": "勤學", "汗流浹背": "情境", "自相矛盾": "警示",
    "光明正大": "為人", "瓜熟蒂落": "勵志", "出人意料": "情境", "生龍活虎": "情境",
    "打草驚蛇": "警示", "半途而廢": "警示", "水滴石穿": "勤學", "手忙腳亂": "情境",
    "不約而同": "情境", "不可開交": "情境", "小心翼翼": "處世", "大驚小怪": "警示",
    "大公無私": "為人", "三心二意": "警示", "入木三分": "情境", "人山人海": "情境",
    "九牛一毛": "情境", "七上八下": "情境", "一諾千金": "為人", "一言九鼎": "為人",
    "一舉兩得": "處世", "一帆風順": "勵志", "一心一意": "勤學", "一石二鳥": "處世",
    "胸有成竹": "處世", "一箭雙鵰": "處世", "亡羊補牢": "警示", "對牛彈琴": "警示",
    "井底之蛙": "警示", "守株待兔": "警示", "畫蛇添足": "警示",
}

def guess_idiom_cat(idiom, explanation):
    if idiom in IDIOM_CAT_MAP:
        return IDIOM_CAT_MAP[idiom]
    text = (idiom or "") + (explanation or "")
    for cat, kws in IDIOM_CAT_KEYWORDS.items():
        if any(k in text for k in kws):
            return cat
    return "情境"

# ---------- 新增 ----------
def add_word(word, pos, meaning, cambridge_url):
    word = (word or "").strip()
    if not word:
        return False, "單字不能為空"
    if word_exists(word):
        return False, f"單字「{word}」已存在，跳過儲存"
    words = load(WORDS_FILE)
    # 發音連結：Google 翻譯（若未提供劍橋連結，自動生成）
    gurl = "https://translate.google.com/?hl=zh-TW&eotf=0&sl=en&tl=zh-TW&text={}&op=translate".format(quote(word))
    words.insert(0, {
        "id": next_id(words), "word": word, "pos": pos or "", "meaning": meaning or "",
        "gtranslate_url": gurl, "created_at": date.today().isoformat(), "sentences": [],
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
                "topic": guess_word_topic(word),
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
        "category": guess_idiom_cat(idiom, (explanation or "")),
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
