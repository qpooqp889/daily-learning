import json, unicodedata
def norm(s):
    s = unicodedata.normalize("NFC", (s or "").strip()); s = s.replace(" ","").replace("\u3000",""); return s.casefold()
words = json.load(open("data/words.json",encoding="utf-8"))
idioms = json.load(open("data/idioms.json",encoding="utf-8"))
wset = {norm(w["word"]) for w in words}
iset = {norm(i["idiom"]) for i in idioms}
cand_w = ["imagine","courage","climate","recycle","protect","discover","patient","gentle","honest","polite","journey","suddenly","curious","adventure","volunteer","preserve","reduce","global","earth","environment","resource","science","scientist","future","promise","respect","share","together","team","win","spirit","focus","memory","camera","postcard","festival","firework","parade","celebrate","tradition","culture","temple","bridge","harbor","palace","castle"]
cand_i = ["鐵杵磨針","懸樑刺股","虛心求教","專心致志","自強不息","勤能補拙","百折不撓","積少成多","不屈不撓","神機妙算","一帆風順","按部就班","腳踏實地","鍥而不捨","集思廣益","聞雞起舞","日積月累","精益求精","廢寢忘食","全力以赴","有志竟成","水滴石穿","熟能生巧","持之以恆","聚精會神","愚公移山","乘風破浪","馬到成功","一諾千金","雪中送炭","同舟共濟","眾志成城","手不釋卷","虛懷若谷","謙沖自牧","見賢思齊","善解人意","樂於助人","尊師重道","彬彬有禮","滿腔熱忱","百尺竿頭","更上一層樓","登高望遠","志同道合","同心協力","萬眾一心"]
print("WORDS NOT IN DB:")
for w in cand_w:
    if norm(w) not in wset: print("  MISS", w)
print("IDIOMS NOT IN DB:")
for i in cand_i:
    if norm(i) not in iset: print("  MISS", i)
print("DONE")
