# -*- coding: utf-8 -*-
"""Driver: run add.py CLI to insert today's (2026-08-05) learning content."""
import subprocess, sys, os

BASE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
env = dict(os.environ, PYTHONIOENCODING='utf-8')

def run(args):
    r = subprocess.run([PY, 'add.py'] + args, capture_output=True, text=True,
                       encoding='utf-8', cwd=BASE, env=env)
    return (r.stdout or '').strip() + ((' ERR:' + r.stderr.strip()) if r.stderr.strip() else '')

out = []

# ---------- 1. Words ----------
words = [
    ('community', '名詞', '社區；社群'),
    ('preserve', '動詞', '保護；保存'),
    ('plastic', '名詞', '塑膠'),
    ('electricity', '名詞', '電；電力'),
    ('astronaut', '名詞', '太空人'),
    ('mystery', '名詞', '謎；神秘的事'),
    ('unusual', '形容詞', '不尋常的；罕見的'),
]
for w, pos, mean in words:
    camb = 'https://dictionary.cambridge.org/zht/詞典/英語-漢語-繁體/{}'.format(w)
    out.append('WORD {}: {}'.format(w, run(['word', w, '--pos', pos, '--meaning', mean, '--cambridge', camb])))

# ---------- 2. Sentences ----------
sentences = [
    ('community', 'Our community has a big park for everyone to enjoy.',
     '我們社區有一個大公園讓大家享用。'),
    ('preserve', 'We should preserve clean water for the future.',
     '我們應該為未來保護乾淨的水資源。'),
    ('plastic', 'Please put the plastic bottles in the recycling bin.',
     '請把塑膠瓶放進回收桶裡。'),
    ('electricity', 'Remember to turn off the lights to save electricity.',
     '記得關燈以節省電力。'),
    ('astronaut', 'The astronaut travels to space in a rocket.',
     '太空人搭乘火箭前往太空。'),
    ('mystery', 'The missing cat is a mystery to the whole family.',
     '那隻失蹤的貓對全家人來說是個謎。'),
    ('unusual', 'It is unusual to see snow in Taiwan in summer.',
     '在台灣夏天看到雪很不尋常。'),
]
for w, en, zh in sentences:
    enc = en.replace(' ', '%20')
    gurl = 'https://translate.google.com/?hl=zh-TW&eotf=0&sl=en&tl=zh-TW&text={}&op=translate'.format(enc)
    out.append('SENT {}: {}'.format(w, run(['sentence', w, '--en', en, '--zh', zh, '--gtranslate', gurl])))

# ---------- 3. Idioms ----------
idioms = [
    ('如魚得水', '好像魚得到水一樣，比喻得到跟自己很投合的人或很適合的環境。',
     '小明轉到新的籃球隊後，就像如魚得水，打得越來越出色。'),
    ('有志者事竟成', '只要有堅定的決心與毅力，事情終究會成功。',
     '姊姊每天努力練習鋼琴，果然有志者事竟成，贏得了比賽冠軍。'),
    ('九牛二虎之力', '形容花費很大的力氣。',
     '弟弟費了九牛二虎之力，才把沉重的書包搬上樓。'),
    ('大顯身手', '充分展現自己的本領與才華。',
     '運動會上，選手們個個大顯身手，贏得觀眾熱烈的掌聲。'),
    ('耳目一新', '形容所見所聞都令人感到新鮮，與以往不同。',
     '教室經過重新布置後，讓人覺得耳目一新。'),
    ('念念不忘', '牢記在心，時時刻刻都想著。',
     '那趟旅行看到的壯麗風景，讓我念念不忘。'),
    ('相輔相成', '互相配合、互相幫助，使效果更好。',
     '讀書和運動相輔相成，讓我們的學習更有活力。'),
]
for i, exp, ex in idioms:
    out.append('IDIOM {}: {}'.format(i, run(['idiom', i, '--explain', exp, '--example', ex])))

with open('add_result.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print('ALL DONE')
