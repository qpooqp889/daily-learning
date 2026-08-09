# -*- coding: utf-8 -*-
"""2026-08-09 每日學習寫入腳本：直接呼叫 add.py 的函式，避免 CLI 編碼問題"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, ".")
import add

CAMBRIDGE = "https://dictionary.cambridge.org/zht/詞典/英語-漢語-繁體/{}"
GTRANSLATE = "https://translate.google.com/?hl=zh-TW&eotf=0&sl=en&tl=zh-TW&text={}&op=translate"

WORDS = [
    ("suddenly", "adv.", "突然地；忽然", "suddenly"),
    ("reduce", "v.", "減少；降低", "reduce"),
    ("global", "adj.", "全球的；全世界的", "global"),
    ("resource", "n.", "資源", "resource"),
    ("firework", "n.", "煙火；煙花", "firework"),
    ("parade", "n.", "遊行", "parade"),
    ("palace", "n.", "皇宮；宮殿", "palace"),
]

SENTENCES = [
    ("suddenly", "Suddenly, it started to rain heavily.", "突然間，天開始下起大雨。",
     "Suddenly,%20it%20started%20to%20rain%20heavily."),
    ("reduce", "We should reduce the use of plastic bags.", "我們應該減少使用塑膠袋。",
     "We%20should%20reduce%20the%20use%20of%20plastic%20bags."),
    ("global", "Global warming is a serious problem.", "全球暖化是一個嚴重的問題。",
     "Global%20warming%20is%20a%20serious%20problem."),
    ("resource", "Water is an important natural resource.", "水是一種重要的自然資源。",
     "Water%20is%20an%20important%20natural%20resource."),
    ("firework", "We watched the fireworks on New Year's Eve.", "我們在除夕夜觀賞煙火。",
     "We%20watched%20the%20fireworks%20on%20New%20Year%E2%80%99s%20Eve."),
    ("parade", "The parade was full of color and music.", "那場遊行充滿了色彩與音樂。",
     "The%20parade%20was%20full%20of%20color%20and%20music."),
    ("palace", "The king lives in a big palace.", "國王住在宏偉的皇宮裡。",
     "The%20king%20lives%20in%20a%20big%20palace."),
]

IDIOMS = [
    ("虛心求教", "謙虛地、誠懇地向別人請教學習。",
     "遇到不懂的問題，他總是虛心求教，所以進步得很快。"),
    ("專心致志", "形容一心一意、集中精神去做某件事。",
     "姊姊專心致志地練習鋼琴，完全沒有注意到窗外下雨了。"),
    ("自強不息", "自己努力向上，永遠不停止、不放棄。",
     "他雖然家境不好，卻能自強不息，最後考上了理想的大學。"),
    ("積少成多", "一點一滴地累積，由少變多。",
     "每天存五十元零用錢，積少成多，一年後就有錢買新腳踏車了。"),
    ("神機妙算", "形容計謀高明，預測準確，令人佩服。",
     "諸葛亮神機妙算，總能料敵機先，讓敵人聞風喪膽。"),
    ("同舟共濟", "比喻大家團結一致，共同克服困難。",
     "颱風過後，村民們同舟共濟，一起重建家園。"),
    ("眾志成城", "大家團結一心，力量就像城牆一樣堅固。",
     "只要全班眾志成城，一定可以在運動會上奪得冠軍。"),
]

print("=== 單字 ===")
for w, pos, meaning, _ in WORDS:
    print(add.add_word(w, pos, meaning, CAMBRIDGE.format(w))[1])
print("=== 句子 ===")
for w, en, zh, enc in SENTENCES:
    print(add.add_sentence(w, en, zh, GTRANSLATE.format(enc))[1])
print("=== 成語 ===")
for i, ex, eg in IDIOMS:
    print(add.add_idiom(i, ex, eg)[1])
print("=== 完成 ===")
