# -*- coding: utf-8 -*-
import subprocess, sys, json
from urllib.parse import quote

# ---- 7 words (all verified new) ----
words = [
    ("battery",   "n.", "電池"),
    ("pilot",     "n.", "飛行員"),
    ("shell",     "n.", "貝殼；外殼"),
    ("giraffe",   "n.", "長頸鹿"),
    ("whisper",   "v.", "低聲說；耳語"),
    ("recipe",    "n.", "食譜；配方"),
    ("tornado",   "n.", "龍捲風"),
]

# ---- 7 sentences (each uses its word) ----
sentences = [
    ("battery",  "The remote control stopped working because the battery was dead.",
               "遙控器因為電池沒電而停止運作。"),
    ("pilot",    "The pilot flew the plane safely through the storm.",
               "飛行員安全地駕駛飛機穿過暴風雨。"),
    ("shell",    "We collected a colorful shell on the beach.",
               "我們在海灘上收集了一個色彩繽紛的貝殼。"),
    ("giraffe",  "The giraffe stretched its long neck to eat the leaves.",
               "長頸鹿伸長牠的長脖子去吃樹葉。"),
    ("whisper",  "Please whisper so you don't wake the baby.",
               "請小聲說話，這樣才不會吵醒寶寶。"),
    ("recipe",   "Mom followed a simple recipe to bake chocolate cookies.",
               "媽媽照著簡單的食譜烤巧克力餅乾。"),
    ("tornado",  "The tornado destroyed several houses in the small town.",
               "龍捲風摧毀了小鎮上幾間房子。"),
]

# ---- 7 idioms (all verified new) ----
idioms = [
    ("邯鄲學步", "比喻盲目模仿別人，反而失去自己原有的長處。",
     "他學別人說話的腔調，結果邯鄲學步，連原本自然的樣子都沒了。"),
    ("夜郎自大", "比喻人見識短淺，卻自以為了不起。",
     "他沒出過國就說自己最厲害，真是夜郎自大。"),
    ("圖窮匕見", "比喻事情發展到最後，真相或本意終於暴露出來。",
     "經過仔細調查，他的謊言圖窮匕見，再也瞞不住了。"),
    ("朝三暮四", "比喻心意不定，反覆無常，常常改變主意。",
     "他對任何興趣都朝三暮四，學什麼都學不久。"),
    ("囊螢映雪", "形容在艱苦的環境中仍然勤奮讀書。",
     "古人囊螢映雪的苦學精神，值得我們好好學習。"),
    ("精衛填海", "比喻意志堅定，不畏艱難，立志完成大事。",
     "他像精衛填海一樣每天堅持練習，最後終於成功了。"),
    ("掩人耳目", "比喻用假象欺騙別人，掩蓋真正的真相。",
     "他想用謊言掩人耳目，卻瞞不過細心的老師。"),
]

def cambridge(word):
    return "https://dictionary.cambridge.org/zht/詞典/英語-漢語-繁體/" + word

def gtranslate(sentence):
    return "https://translate.google.com/?hl=zh-TW&eotf=0&sl=en&tl=zh-TW&text={}&op=translate".format(
        quote(sentence))

cambridge_links = {}
gtranslate_links = {}

def run(args):
    r = subprocess.run([sys.executable, "add.py"] + args,
                       capture_output=True, text=True, encoding="utf-8")
    return (r.stdout or "").strip() + (r.stderr or "").strip()

results = []
for w, pos, meaning in words:
    link = cambridge(w)
    cambridge_links[w] = link
    results.append(run(["word", w, "--pos", pos, "--meaning", meaning, "--cambridge", link]))

for w, en, zh in sentences:
    link = gtranslate(en)
    gtranslate_links[w] = link
    results.append(run(["sentence", w, "--en", en, "--zh", zh, "--gtranslate", link]))

for idi, exp, ex in idioms:
    results.append(run(["idiom", idi, "--explain", exp, "--example", ex]))

with open("run_result_2026-08-14.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(results))

# save links for the output step
json.dump({"cambridge": cambridge_links, "gtranslate": gtranslate_links},
          open("links_2026-08-14.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print("\n".join(results))
