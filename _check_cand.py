# -*- coding: utf-8 -*-
import json, io, sys, unicodedata
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

def norm(s):
    s = unicodedata.normalize("NFC", (s or "").strip())
    return s.replace(" ", "").replace("\u3000", "").casefold()

w = json.load(open("data/words.json", encoding="utf-8"))
i = json.load(open("data/idioms.json", encoding="utf-8"))
wset = {norm(x["word"]) for x in w}
iset = {norm(x["idiom"]) for x in i}

word_cands = ["ambulance", "calendar", "crayon", "scissors", "envelope", "glue",
              "whistle", "flashlight", "blanket", "pillow", "towel", "curtain",
              "comb", "basket", "ladder", "hammer", "screwdriver", "rope",
              "wallet", "glove", "scarf", "boots", "apron", "helmet", "goggles",
              "lifeguard", "treasure", "pirate", "anchor", "lighthouse",
              "desert", "waterfall", "canyon", "glacier", "swamp", "pond",
              "stream", "cliff", "meadow", "bamboo", "rose", "lily", "daisy",
              "root", "trunk", "insect", "dragonfly", "grasshopper", "caterpillar",
              "cocoon", "feather", "claw", "horn", "fur", "octopus", "squid",
              "shrimp", "lobster", "oyster", "lizard", "eagle", "crow", "sparrow",
              "swan", "goose", "turkey", "pigeon", "peacock", "parrot", "ostrich",
              "kangaroo", "koala", "zebra", "camel", "wolf", "squirrel", "hamster",
              "goldfish", "kitten", "puppy", "beaver", "raccoon", "otter", "seal",
              "walrus", "battery", "button", "needle", "thread", "chopsticks",
              "bowl", "plate", "kettle", "thermos", "lantern", "candle",
              "match", "wax", "ink", "paintbrush", "ruler", "stapler", "clip"]

idiom_cands = ["大器晚成", "三顧茅廬", "初出茅廬", "樂不思蜀", "望梅止渴",
               "負荊請罪", "約法三章", "背水一戰", "邯鄲學步", "買櫝還珠",
               "鷸蚌相爭", "螳螂捕蟬", "朝三暮四", "杯水車薪", "癡人說夢",
               "黃粱一夢", "海市蜃樓", "世外桃源", "山窮水盡", "真相大白",
               "一網打盡", "甕中捉鱉", "釜底抽薪", "落井下石", "兔死狐悲",
               "脣齒相依", "風雨同舟", "肝膽相照", "推心置腹", "開誠布公",
               "志同道合", "心心相印", "心有靈犀", "異口同聲", "殊途同歸",
               "異曲同工", "大相逕庭", "天壤之別", "滄海桑田", "光陰似箭",
               "日月如梭", "轉瞬即逝", "曇花一現", "心想事成", "如願以償",
               "事與願違", "弄巧成拙", "過猶不及", "物極必反", "否極泰來",
               "苦盡甘來", "化險為夷", "逢凶化吉", "因禍得福", "因小失大",
               "得不償失", "一鳴驚人", "對症下藥", "如虎添翼", "調虎離山",
               "放虎歸山", "畫虎類犬", "三人成虎", "初生之犢", "牛刀小試",
               "汗牛充棟", "鶴立雞群", "狗仗人勢", "狼心狗肺", "兔死狗烹",
               "過街老鼠", "貓哭耗子", "馬不停蹄", "蛛絲馬跡", "招兵買馬",
               "人仰馬翻", "羊腸小徑", "歧路亡羊", "虎虎生風", "龍馬精神"]

print("=== WORD CANDIDATES ===")
for c in word_cands:
    print(("EXISTS " if norm(c) in wset else "OK     ") + c)
print("=== IDIOM CANDIDATES ===")
for c in idiom_cands:
    print(("EXISTS " if norm(c) in iset else "OK     ") + c)
