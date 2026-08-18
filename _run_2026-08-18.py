# -*- coding: utf-8 -*-
"""Driver: 呼叫 add.py 新增 2026-08-18 每日學習資料"""
import subprocess, sys, io

PY = sys.executable
ADD = r"C:\Users\twric\.qclaw\workspace\daily-learning\add.py"

def run(args):
    r = subprocess.run([PY, ADD] + args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return (r.stdout or r.stderr).strip()

out = io.StringIO()

# ---------- 一、英文單字 7 個 ----------
words = [
    ("concert",    "n.", "音樂會；演奏會"),
    ("rhythm",     "n.", "節奏；韻律"),
    ("melody",     "n.", "旋律；曲調"),
    ("chorus",     "n.", "合唱團；（歌曲的）副歌"),
    ("banner",     "n.", "橫幅；旗幟"),
    ("mural",      "n.", "壁畫"),
    ("campaign",   "n.", "活動；宣傳運動"),
]
for w, pos, mean in words:
    cb = f"https://dictionary.cambridge.org/zht/詞典/英語-漢語-繁體/{w}"
    out.write(f"[word] {run(['word', w, '--pos', pos, '--meaning', mean, '--cambridge', cb])}\n")

# ---------- 二、英文例句 7 句 ----------
sentences = [
    ("concert",  "We went to a music concert on Saturday night.",
     "我們星期六晚上去聽了一場音樂會。",
     "https://translate.google.com/?hl=zh-TW&eotf=0&sl=en&tl=zh-TW&text=We%20went%20to%20a%20music%20concert%20on%20Saturday%20night.&op=translate"),
    ("rhythm",   "She can dance to the rhythm of the song.",
     "她能跟著這首歌的節奏跳舞。",
     "https://translate.google.com/?hl=zh-TW&eotf=0&sl=en&tl=zh-TW&text=She%20can%20dance%20to%20the%20rhythm%20of%20the%20song.&op=translate"),
    ("melody",   "I like the melody of this piano piece.",
     "我喜歡這首鋼琴曲的旋律。",
     "https://translate.google.com/?hl=zh-TW&eotf=0&sl=en&tl=zh-TW&text=I%20like%20the%20melody%20of%20this%20piano%20piece.&op=translate"),
    ("chorus",   "The whole class sang the chorus together.",
     "全班一起唱了副歌的部分。",
     "https://translate.google.com/?hl=zh-TW&eotf=0&sl=en&tl=zh-TW&text=The%20whole%20class%20sang%20the%20chorus%20together.&op=translate"),
    ("banner",   "The students made a big banner for the school festival.",
     "學生們為學校園遊會做了一面大橫幅。",
     "https://translate.google.com/?hl=zh-TW&eotf=0&sl=en&tl=zh-TW&text=The%20students%20made%20a%20big%20banner%20for%20the%20school%20festival.&op=translate"),
    ("mural",    "There is a beautiful mural on the wall of our school.",
     "我們學校的牆上有一幅美麗的壁畫。",
     "https://translate.google.com/?hl=zh-TW&eotf=0&sl=en&tl=zh-TW&text=There%20is%20a%20beautiful%20mural%20on%20the%20wall%20of%20our%20school.&op=translate"),
    ("campaign", "Our class joined the clean-up campaign in the park.",
     "我們班參加了公園的清潔活動。",
     "https://translate.google.com/?hl=zh-TW&eotf=0&sl=en&tl=zh-TW&text=Our%20class%20joined%20the%20clean-up%20campaign%20in%20the%20park.&op=translate"),
]
for w, en, zh, gurl in sentences:
    out.write(f"[sentence] {run(['sentence', w, '--en', en, '--zh', zh, '--gtranslate', gurl])}\n")

# ---------- 三、國語成語 7 則 ----------
idioms = [
    ("杯水車薪", "用一杯水去救一車著火的柴草。比喻力量太小，解決不了問題。",
     "他一個月只有一百元零用錢，卻想存錢買一台電腦，真是杯水車薪。"),
    ("百步穿楊", "形容射箭或射擊的技術十分高明，百發百中。",
     "他的箭術高超，百步穿楊，百發百中，贏得大家的喝采。"),
    ("獨當一面", "一個人單獨負責某一方面的工作或事務。",
     "姊姊長大後已經可以獨當一面，獨自打理店裡所有的訂單。"),
    ("實至名歸", "有真正的學問或本領，名聲自然隨之而來；形容名聲與實際相符。",
     "他苦練多年終於奪冠，這座獎盃可說是實至名歸。"),
    ("妙筆生花", "形容文筆極佳，能寫出精彩動人的文章。",
     "作家妙筆生花，把平凡的小鎮寫得令人十分嚮往。"),
    ("出神入化", "形容技藝已達到非常高超、精妙的境界。",
     "魔術師的表演出神入化，觀眾看得目瞪口呆。"),
    ("心無旁騖", "專心一意，心中沒有其他雜念。",
     "考試前一週，他心無旁騖地複習，果然考出好成績。"),
]
for i, exp, ex in idioms:
    out.write(f"[idiom] {run(['idiom', i, '--explain', exp, '--example', ex])}\n")

with open(r"C:\Users\twric\.qclaw\workspace\daily-learning\_run_2026-08-18.txt", "w", encoding="utf-8") as f:
    f.write(out.getvalue())
print("ALL DONE")
