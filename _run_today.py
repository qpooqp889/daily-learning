# -*- coding: utf-8 -*-
"""2026-08-11 每日學習資料新增 runner"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import add

lines = []

def log(msg):
    lines.append(msg)
    print(msg)

# ---------- 一、英文單字 ----------
words = [
    ("scissors", "n.", "剪刀", "https://dictionary.cambridge.org/zht/詞典/英語-漢語-繁體/scissors"),
    ("whistle", "n.", "哨子；口哨", "https://dictionary.cambridge.org/zht/詞典/英語-漢語-繁體/whistle"),
    ("ladder", "n.", "梯子", "https://dictionary.cambridge.org/zht/詞典/英語-漢語-繁體/ladder"),
    ("apron", "n.", "圍裙", "https://dictionary.cambridge.org/zht/詞典/英語-漢語-繁體/apron"),
    ("helmet", "n.", "安全帽；頭盔", "https://dictionary.cambridge.org/zht/詞典/英語-漢語-繁體/helmet"),
    ("lighthouse", "n.", "燈塔", "https://dictionary.cambridge.org/zht/詞典/英語-漢語-繁體/lighthouse"),
    ("bamboo", "n.", "竹子", "https://dictionary.cambridge.org/zht/詞典/英語-漢語-繁體/bamboo"),
]
for word, pos, meaning, cam in words:
    ok, msg = add.add_word(word, pos, meaning, cam)
    log(f"[WORD] {msg}")

# ---------- 二、英文例句 ----------
sentences = [
    ("scissors", "Please cut the paper with the scissors.", "請用剪刀剪紙。"),
    ("whistle", "The referee blew the whistle to stop the game.", "裁判吹哨子停止比賽。"),
    ("ladder", "My father used a ladder to fix the roof.", "我爸爸用梯子修理屋頂。"),
    ("apron", "Mom wears an apron when she cooks.", "媽媽煮飯時穿圍裙。"),
    ("helmet", "You must wear a helmet when you ride a bike.", "騎腳踏車時必須戴安全帽。"),
    ("lighthouse", "The lighthouse guides the ships at night.", "燈塔在夜裡為船隻指引方向。"),
    ("bamboo", "The panda likes to eat fresh bamboo.", "貓熊喜歡吃新鮮的竹子。"),
]
from urllib.parse import quote
for word, en, zh in sentences:
    enc = quote(en).replace("%20", "%20")
    gurl = f"https://translate.google.com/?hl=zh-TW&eotf=0&sl=en&tl=zh-TW&text={enc}&op=translate"
    ok, msg = add.add_sentence(word, en, zh, gurl)
    log(f"[SENT] {msg}")

# ---------- 三、國語成語 ----------
idioms = [
    ("三顧茅廬", "比喻誠心誠意一再邀請，就像劉備三次拜訪諸葛亮一樣。", "為了請李老師來演講，校長三顧茅廬，終於感動了他。"),
    ("負荊請罪", "主動向對方認錯賠罪，請求原諒。", "他知道自己誤會了好朋友，立刻負荊請罪，請求原諒。"),
    ("背水一戰", "比喻沒有退路，只能下定決心奮力一搏。", "比賽進入最後一局，兩隊都背水一戰，全力以赴。"),
    ("大器晚成", "比喻能擔當大事的人，成就往往來得比較晚。", "他小時候成績平平，如今事業有成，真是大器晚成。"),
    ("鷸蚌相爭", "比喻雙方相爭不下，反而讓第三者得到好處。", "兩家店惡性競爭，結果鷸蚌相爭，漁翁得利。"),
    ("對症下藥", "比喻針對問題所在，採取有效的解決方法。", "老師對症下藥，幫小明解決了數學上的困難。"),
    ("志同道合", "形容彼此志向相同、理念相合。", "我和小華志同道合，都想當醫生幫助病人。"),
]
for idiom, explain, example in idioms:
    ok, msg = add.add_idiom(idiom, explain, example)
    log(f"[IDIOM] {msg}")

with open("_run_result_2026-08-11.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("ALL DONE")
