# -*- coding: utf-8 -*-
import json, os, unicodedata
base = os.path.dirname(os.path.abspath(__file__))

def norm(s):
    s = unicodedata.normalize("NFC", (s or "").strip())
    s = s.replace(" ", "").replace("\u3000", "")
    return s.casefold()

w = json.load(open(os.path.join(base, "data", "words.json"), encoding="utf-8"))
i = json.load(open(os.path.join(base, "data", "idioms.json"), encoding="utf-8"))
existing_w = {norm(x["word"]) for x in w}
existing_i = {norm(x["idiom"]) for x in i}

word_cands = """invention, universe, telescope, earthquake, volcano, glacier, treasure, pirate,
courageous, curiousity, knowledge, educate, publish, librarian, principal, certificate,
graduation, university, laboratory, microscope, experiment, gravity, planet, satellite,
orbit, rocket, spaceship, comet, eclipse, species, habitat, pollution, garbage, recycle,
reduce, reuse, energy, solar, battery, machine, engine, factory, tool, material, metal,
plastic, wood, cotton, leather, wool, silk, medicine, disease, healthy, exercise, muscle,
balance, stretch, practice, improve, progress, success, failure, mistake, question, answer,
explain, describe, discuss, agree, disagree, argue, promise, decision, choice, reason,
purpose, goal, plan, future, past, present, century, decade, calendar, schedule, appointment,
invitation, message, letter, envelope, stamp, address, phone, computer, internet, website,
email, keyboard, mouse, screen, camera, photo, picture, painting, drawing, artist, museum,
gallery, concert, theater, actor, actress, singer, band, audience, ticket, stage, curtain,
piano, guitar, violin, drum, flute, melody, rhythm, poem, poet, story, novel, writer,
chapter, character, hero, villain, adventure, mystery, fantasy, science, nature, weather,
storm, thunder, lightning, rainbow, cloud, wind, snow, ice, fog, temperature, degree,
season, spring, summer, autumn, winter, climate, island, beach, coast, mountain, valley,
river, lake, ocean, forest, jungle, desert, cave, waterfall, bridge, tunnel, road, street,
city, town, village, country, capital, government, president, citizen, police, firefighter,
doctor, nurse, teacher, student, farmer, fisherman, cook, waiter, driver, pilot, engineer,
scientist, musician, artist, player, coach, team, game, match, score, win, lose, draw,
champion, trophy, medal, race, runner, swimmer, jumper, throw, catch, kick, pass, shoot,
goal, basket, field, court, gym, stadium, swimming, skating, skiing, climbing, hiking,
camping, fishing, boating, sailing, surfing, diving, snorkeling, picnic, barbecue, party,
festival, holiday, vacation, trip, tour, guide, map, compass, luggage, backpack, suitcase,
passport, airport, station, platform, train, bus, taxi, bicycle, motorcycle, ship, boat,
ferry, cruise, flight, ticket, passenger, driver, safety, helmet, seatbelt, traffic, rule,
sign, signal, crosswalk, sidewalk, bridge, tunnel, accident, injury, first aid, bandage,
hospital, clinic, pharmacy, medicine, pill, fever, cough, cold, flu, headache, stomach,
toothache, allergy, patient, doctor, nurse, treatment, cure, health, healthy, exercise""".split(", ")

idiom_cands = """一見如故, 一鳴驚人, 一諾千金, 一箭雙鵰, 一舉兩得, 一石二鳥, 七上八下, 九牛一毛,
人山人海, 入木三分, 三心二意, 亡羊補牢, 口若懸河, 大公無私, 大驚小怪, 小心翼翼,
川流不息, 不約而同, 不遺餘力, 中流砥柱, 五光十色, 井井有條, 手忙腳亂, 打草驚蛇,
正大光明, 生龍活虎, 全力以赴, 半途而廢, 半信半疑, 有始有終, 有志竟成, 汗流浹背,
自相矛盾, 安居樂業, 老馬識途, 走馬看花, 見多識廣, 事半功倍, 事倍功半, 刻舟求劍,
杯弓蛇影, 東施效顰, 花言巧語, 虎頭蛇尾, 南轅北轍, 迫不得已, 柳暗花明, 破釜沉舟,
馬到成功, 掩耳盜鈴, 欲速則不達, 眼高手低, 雪中送炭, 畫餅充飢, 畫蛇添足, 塞翁失馬,
愚公移山, 斬草除根, 滴水穿石, 聚精會神, 熟能生巧, 融會貫通, 學以致用, 舉一反三,
臨危不亂, 豁然開朗, 謙虛謹慎, 錦上添花, 隨機應變, 龍飛鳳舞, 機不可失, 獨一無二,
聞雞起舞, 精益求精, 感恩圖報, 旗鼓相當, 無中生有, 異想天開, 笑裡藏刀, 紙上談兵,
笨鳥先飛, 理直氣壯, 登峰造極, 挖空心思, 畫龍點睛, 金玉良言, 狐假虎威, 狗急跳牆""".split(", ")

out = []
out.append("新單字候選（不在資料庫中）：")
new_w = [c for c in word_cands if norm(c) not in existing_w]
for c in new_w:
    out.append("OK  " + c)
out.append("")
out.append("新成語候選（不在資料庫中）：")
new_i = [c for c in idiom_cands if norm(c) not in existing_i]
for c in new_i:
    out.append("OK  " + c)
open(os.path.join(base, "tmp_cands2.txt"), "w", encoding="utf-8").write("\n".join(out))
print("new words:", len(new_w), "new idioms:", len(new_i))
