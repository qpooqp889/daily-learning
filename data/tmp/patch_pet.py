# -*- coding: utf-8 -*-
"""Pet system revamp: maxLv 10->30, EXP +1 per correct, weighted multiplier 1+(lv-1)*0.1, retrain button."""
import re, io

PATH = r'C:\Users\twric\.qclaw\workspace\daily-learning\index.html'
html = io.open(PATH, encoding='utf-8').read()
orig = html

# 1. maxLv 10 -> 30
html = html.replace("maxLv: 10", "maxLv: 30")

# 2. Add xpMultiplier helper after stageEmoji
helper = '''
function xpMultiplier(p) {
  // 等級加權：Lv2 = 1.1 倍、Lv3 = 1.2 倍 ... 每升一等 +0.1
  return 1 + (Math.max(1, p.lv) - 1) * 0.1;
}

'''
anchor = "function getPet() {"
assert anchor in html, 'anchor getPet not found'
html = html.replace(anchor, helper + anchor, 1)

# 3. renderPet: xp text update (每題 +1 -> weighted), add retrain button
old_xp_text = "經驗值 ${pet.xp} / ${xpNeed}（答對一題 +10）"
new_xp_text = "經驗值 ${pet.xp.toFixed(1)} / ${xpNeed}（答對 +${xpMultiplier(pet).toFixed(1)} EXP，隨等級加權）"
assert old_xp_text in html, 'xp text not found'
html = html.replace(old_xp_text, new_xp_text, 1)

# 4. pet-actions: add 重新選擇 button
old_actions = """<button class="chip-btn" data-feed>🍗 餵食 +15</button>
            <button class="chip-btn" data-play>🎾 玩 +15</button>
            <button class="chip-btn" data-name>✏️ 改名</button>"""
if old_actions not in html:
    # fallback: generic replace on the three buttons block
    m = re.search(r'(<button class="chip-btn" data-feed>.*?</button>\s*<button class="chip-btn" data-play>.*?</button>\s*<button class="chip-btn" data-name>.*?</button>)', html, re.S)
    assert m, 'pet action buttons not found'
    old_actions = m.group(1)
new_actions = old_actions + """
            <button class="chip-btn" data-retrain style="border-color:var(--danger);color:var(--danger);">🔄 重新選擇</button>"""
html = html.replace(old_actions, new_actions, 1)

# 5. data-retrain handler (after data-name handler)
old_name_h = """root.querySelector('[data-name]').onclick = async () => {
    const p = await getPet();
    const nn = prompt('幫寵物取新名字：', p.name);
    if (nn && nn.trim()) { p.name = nn.trim(); await idbPut(PET_STORE, p, 'pet'); renderPet(); }
  };"""
assert old_name_h in html, 'data-name handler not found'
new_name_h = old_name_h + """
  const retrainBtn = root.querySelector('[data-retrain]');
  if (retrainBtn) retrainBtn.onclick = async () => {
    if (!confirm('確定要重新選擇寵物嗎？目前的進度（等級/經驗/飽食/心情）將全部重置！')) return;
    await idbDelete(PET_STORE, 'pet');
    renderPet();
  };"""
html = html.replace(old_name_h, new_name_h, 1)

# 6. addXp: +1 per question with multiplier, maxLv 30 support
old_addxp = """async function addXp(n) {
  const p = await getPet();
  p.xp += n; p.correct++;
  const t = PET_TYPES[p.type];
  while (p.xp >= p.lv * 50 && p.lv < t.maxLv) { p.xp -= p.lv * 50; p.lv++; }
  if (p.lv >= t.maxLv) p.xp = Math.min(p.xp, p.lv * 50);
  await idbPut(PET_STORE, p, 'pet');
}"""
assert old_addxp in html, 'addXp not found'
new_addxp = """async function addXp(n) {
  const p = await getPet();
  const gain = n * xpMultiplier(p);   // 加權：Lv2=1.1x、Lv3=1.2x...
  p.xp += gain; p.correct++;
  const t = PET_TYPES[p.type];
  while (p.xp >= p.lv * 50 && p.lv < t.maxLv) { p.xp -= p.lv * 50; p.lv++; }
  if (p.lv >= t.maxLv) p.xp = Math.min(p.xp, p.lv * 50);
  await idbPut(PET_STORE, p, 'pet');
}"""
html = html.replace(old_addxp, new_addxp, 1)

# 7. answer: addXp(10) -> addXp(1)
old_ans = "if (ok) { score++; await addXp(10); }"
new_ans = "if (ok) { score++; await addXp(1); }"
assert old_ans in html, 'answer addXp call not found'
html = html.replace(old_ans, new_ans, 1)

# 8. check idbDelete exists
assert 'idbDelete' in html, 'idbDelete missing'

io.open(PATH, 'w', encoding='utf-8', newline='').write(html)
print('changed:', orig != html)
# summary
for pat in ['maxLv: 30', 'xpMultiplier', '重新選擇', 'addXp(1)', 'gain = n * xpMultiplier']:
    print(pat, '->', pat in html)
