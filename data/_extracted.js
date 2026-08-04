
const $ = s => document.querySelector(s);
const statsEl = $('#stats'), wordsList = $('#wordsList'), idiomsList = $('#idiomsList');
let allWords = [], allIdioms = [];

/* ================= 主題 ================= */
const savedTheme = localStorage.getItem('theme') || 'light';
document.documentElement.dataset.theme = savedTheme;
$('#themeToggle').textContent = savedTheme === 'dark' ? '☀️ 白天模式' : '🌙 黑夜模式';
$('#themeToggle').onclick = () => {
  const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
  document.documentElement.dataset.theme = next;
  localStorage.setItem('theme', next);
  $('#themeToggle').textContent = next === 'dark' ? '☀️ 白天模式' : '🌙 黑夜模式';
};

/* ================= 分頁 ================= */
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.onclick = () => {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    $('#page-' + btn.dataset.tab).classList.add('active');
    if (btn.dataset.tab === 'plan') loadPlans();
    if (btn.dataset.tab === 'pet') renderPet();
  };
});

/* ================= 搜尋（模糊）+ A-Z / 主題 / 分類篩選 ================= */
let searchQ = '';
let alphaFilter = '';   // A-Z 字母篩選
let topicFilter = '';   // 句子主題篩選
let catFilter = '';     // 成語分類篩選

$('#searchInput').addEventListener('input', e => {
  searchQ = e.target.value.trim().toLowerCase();
  renderWords(allWords);
  renderIdioms(allIdioms);
});

/* A-Z 快查列 */
function renderAlphaBar() {
  const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
  const available = new Set(allWords.map(w => w.word[0].toUpperCase()));
  $('#alphaBar').innerHTML =
    `<span class="filter-label">🔠 字母快查：</span>
     <button class="alpha-btn ${!alphaFilter ? 'active' : ''}" data-a="">全</button>` +
    letters.map(l =>
      `<button class="alpha-btn ${alphaFilter === l ? 'active' : ''}" data-a="${l}" ${available.has(l) ? '' : 'style="opacity:.35"'}>${l}</button>`
    ).join('');
  $('#alphaBar').querySelectorAll('.alpha-btn').forEach(b => b.onclick = () => {
    alphaFilter = b.dataset.a;
    renderAlphaBar();
    renderWords(allWords);
  });
}

/* 句子主題 chips */
function renderTopicBar() {
  const counts = {};
  allWords.forEach(w => (w.sentences || []).forEach(s => {
    const t = s.topic || '未分類';
    counts[t] = (counts[t] || 0) + 1;
  }));
  $('#topicChips').innerHTML = Object.keys(counts).map(t =>
    `<button class="topic-chip ${topicFilter === t ? 'active' : ''}" data-topic="${esc(t)}">${esc(t)} ${counts[t]}</button>`
  ).join('');
  $('#topicBar').querySelectorAll('.topic-chip').forEach(b => b.onclick = () => {
    topicFilter = b.dataset.topic;
    document.querySelectorAll('#topicBar .topic-chip').forEach(c => c.classList.toggle('active', c.dataset.topic === topicFilter));
    renderWords(allWords);
  });
}

/* 成語分類 chips */
function renderCatBar() {
  const counts = {};
  allIdioms.forEach(i => {
    const c = i.category || '未分類';
    counts[c] = (counts[c] || 0) + 1;
  });
  $('#catChips').innerHTML = Object.keys(counts).map(c =>
    `<button class="cat-chip ${catFilter === c ? 'active' : ''}" data-cat="${esc(c)}">${esc(c)} ${counts[c]}</button>`
  ).join('');
  $('#catBar').querySelectorAll('.cat-chip').forEach(b => b.onclick = () => {
    catFilter = b.dataset.cat;
    document.querySelectorAll('#catBar .cat-chip').forEach(c => c.classList.toggle('active', c.dataset.cat === catFilter));
    renderIdioms(allIdioms);
  });
}

function matchFields(q, ...fields) {
  return fields.some(f => (f || '').toLowerCase().includes(q));
}
function highlight(text, q) {
  const s = String(text == null ? '' : text);
  if (!q) return esc(s);
  const idx = s.toLowerCase().indexOf(q);
  if (idx < 0) return esc(s);
  return esc(s.slice(0, idx)) + '<span class="hit">' + esc(s.slice(idx, idx + q.length)) + '</span>' + esc(s.slice(idx + q.length));
}

/* ================= 資料載入 ================= */
async function loadAll() {
  try {
    const ts = '?t=' + Date.now();   // cache-busting：避免 CDN/瀏覽器快取舊版資料
    const [words, idioms] = await Promise.all([
      fetch('data/words.json' + ts).then(r => r.json()),
      fetch('data/idioms.json' + ts).then(r => r.json())
    ]);
    allWords = words; allIdioms = idioms;
    renderAlphaBar(); renderTopicBar(); renderCatBar();
    renderWords(words); renderIdioms(idioms); renderPickLists();
    const nSent = words.reduce((n, w) => n + (w.sentences || []).length, 0);
    statsEl.textContent = `單字 ${words.length} · 句子 ${nSent} · 成語 ${idioms.length}`;
    loadPlans();
    renderPet();
  } catch (e) {
    wordsList.innerHTML = `<div class="empty">載入失敗：${esc(e.message)}</div>`;
  }
}

function renderWords(words) {
  const q = searchQ;
  let filtered = words;
  // 搜尋
  if (q) filtered = filtered.filter(w =>
    matchFields(q, w.word, w.pos, w.meaning) ||
    (w.sentences || []).some(s => matchFields(q, s.sentence, s.translation))
  );
  // A-Z 字母篩選
  if (alphaFilter) filtered = filtered.filter(w => w.word[0].toUpperCase() === alphaFilter);
  // 句子主題篩選
  if (topicFilter) filtered = filtered.filter(w => (w.sentences || []).some(s => (s.topic || '未分類') === topicFilter));
  if (!filtered.length) { wordsList.innerHTML = '<div class="empty">沒有符合的單字～</div>'; return; }
  wordsList.innerHTML = filtered.map(w => {
    const sents = (w.sentences || []).map(s => `
      <div class="sentence">
        <div class="en">${highlight(s.sentence, q)} ${s.gtranslate_url ? `<a class="link-btn" href="${esc(s.gtranslate_url)}" target="_blank">🔊 聽整句</a>` : ''}${s.topic ? `<span class="topic-badge">${esc(s.topic)}</span>` : ''}</div>
        <div class="zh">${highlight(s.translation, q)}</div>
      </div>`).join('');
    return `
    <div class="card">
      <div class="word-head">
        <span class="word">${highlight(w.word, q)}</span>
        ${w.pos ? `<span class="pos">${esc(w.pos)}</span>` : ''}
        <span class="meaning">${highlight(w.meaning, q)}</span>
        ${w.gtranslate_url ? `<a class="link-btn" href="${esc(w.gtranslate_url)}" target="_blank">🔊 發音</a>` : ''}
      </div>
      ${sents}
    </div>`;
  }).join('');
}

function renderIdioms(idioms) {
  const q = searchQ;
  let filtered = idioms;
  // 搜尋
  if (q) filtered = filtered.filter(i => matchFields(q, i.idiom, i.explanation, i.example));
  // 分類篩選
  if (catFilter) filtered = filtered.filter(i => (i.category || '未分類') === catFilter);
  if (!filtered.length) { idiomsList.innerHTML = '<div class="empty">沒有符合的成語～</div>'; return; }
  idiomsList.innerHTML = filtered.map(i => `
    <div class="card">
      <div class="idiom-head"><span class="idiom">${highlight(i.idiom, q)}</span>${i.category ? `<span class="cat-badge">${esc(i.category)}</span>` : ''}</div>
      <div class="explanation">📖 ${highlight(i.explanation, q)}</div>
      ${i.example ? `<div class="example">${highlight(i.example, q)}</div>` : ''}
    </div>`).join('');
}

/* ================= 學習計畫（IndexedDB） ================= */
const DB_NAME = 'daily-learning', DB_VER = 2;
function openDB() {
  return new Promise((res, rej) => {
    const req = indexedDB.open(DB_NAME, DB_VER);
    req.onupgradeneeded = e => {
      const db = e.target.result;
      if (!db.objectStoreNames.contains('plans'))
        db.createObjectStore('plans', { keyPath: 'id' });
      if (!db.objectStoreNames.contains('pet'))
        db.createObjectStore('pet');
    };
    req.onsuccess = () => res(req.result);
    req.onerror = () => rej(req.error);
  });
}
async function idbGetAll(store) {
  const db = await openDB();
  return new Promise((res, rej) => {
    const tx = db.transaction(store, 'readonly');
    const rq = tx.objectStore(store).getAll();
    rq.onsuccess = () => res(rq.result || []);
    rq.onerror = () => rej(rq.error);
  });
}
async function idbPut(store, val, key) {
  const db = await openDB();
  return new Promise((res, rej) => {
    const tx = db.transaction(store, 'readwrite');
    if (key !== undefined) tx.objectStore(store).put(val, key);
    else tx.objectStore(store).put(val);
    tx.oncomplete = () => res();
    tx.onerror = () => rej(tx.error);
  });
}
async function idbDelete(store, key) {
  const db = await openDB();
  return new Promise((res, rej) => {
    const tx = db.transaction(store, 'readwrite');
    tx.objectStore(store).delete(key);
    tx.oncomplete = () => res();
    tx.onerror = () => rej(tx.error);
  });
}

function todayStr() {
  const d = new Date();
  return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
}
function addDays(dateStr, n) {
  const d = new Date(dateStr + 'T00:00:00');
  d.setDate(d.getDate() + n);
  return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
}
function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function renderPickLists() {
  $('#pickWords').innerHTML = allWords.map(w =>
    `<label><input type="checkbox" value="${esc(w.word)}"> ${esc(w.word)} <span style="color:var(--muted)">(${esc(w.meaning || '')})</span></label>`).join('');
  $('#pickIdioms').innerHTML = allIdioms.map(i =>
    `<label><input type="checkbox" value="${esc(i.idiom)}"> ${esc(i.idiom)}</label>`).join('');
}
document.querySelectorAll('.mini-btn').forEach(btn => {
  btn.onclick = () => {
    const list = btn.dataset.sel === 'en' ? '#pickWords' : '#pickIdioms';
    document.querySelectorAll(list + ' input').forEach(c => c.checked = btn.dataset.clear ? false : true);
  };
});

function buildPlan(name, startDate, days, selWords, selIdioms) {
  const entries = [];
  for (let d = 0; d < days; d++) entries.push({ date: addDays(startDate, d), words: [], idioms: [] });
  // 隨機分配、不重複：打亂後輪流放入每一天
  shuffle(selWords).forEach((wd, i) => entries[i % days].words.push({ word: wd, done: false }));
  shuffle(selIdioms).forEach((idm, i) => entries[i % days].idioms.push({ idiom: idm, done: false }));
  return {
    id: 'plan_' + Date.now() + '_' + Math.floor(Math.random() * 1e6),
    name, startDate, days,
    createdAt: new Date().toISOString(),
    entries
  };
}

$('#btnCreatePlan').onclick = async () => {
  const name = $('#planName').value.trim() || '學習計畫';
  const start = $('#planStart').value || todayStr();
  const days = Math.min(90, Math.max(1, parseInt($('#planDays').value) || 30));
  const selWords = [...document.querySelectorAll('#pickWords input:checked')].map(c => c.value);
  const selIdioms = [...document.querySelectorAll('#pickIdioms input:checked')].map(c => c.value);
  if (!selWords.length && !selIdioms.length) {
    $('#createMsg').textContent = '⚠️ 請至少勾選一個單字或成語';
    return;
  }
  const plan = buildPlan(name, start, days, selWords, selIdioms);
  await idbPut('plans', plan);
  $('#createMsg').textContent = `✅ 已建立「${name}」：${days} 天，單字 ${selWords.length} 個、成語 ${selIdioms.length} 則（隨機分配・不重複）`;
  loadPlans();
};

async function loadPlans() {
  const plans = (await idbGetAll('plans')).sort((a, b) => b.createdAt.localeCompare(a.createdAt));
  const el = $('#plansList');
  if (!plans.length) {
    el.innerHTML = '<div class="plan-empty">還沒有學習計畫～ 上方建立一個吧！</div>';
    return;
  }
  el.innerHTML = plans.map(plan => {
    const total = plan.entries.reduce((n, e) => n + e.words.length + e.idioms.length, 0);
    const done = plan.entries.reduce((n, e) => n + e.words.filter(w => w.done).length + e.idioms.filter(i => i.done).length, 0);
    const pct = total ? Math.round(done / total * 100) : 0;
    const rows = plan.entries.map(e => {
      const items = [
        ...e.words.map(w => ({ key: 'w|' + e.date + '|' + w.word, label: w.word, done: w.done })),
        ...e.idioms.map(i => ({ key: 'i|' + e.date + '|' + i.idiom, label: i.idiom, done: i.done }))
      ];
      if (!items.length) return '';
      return `<div class="day-row">
        <span class="day-date">${e.date}</span>
        <span class="day-items">${items.map(it => `
          <label class="day-item ${it.done ? 'done' : ''}" data-key="${esc(it.key)}">
            <input type="checkbox" ${it.done ? 'checked' : ''} data-key="${esc(it.key)}"> ${esc(it.label)}
          </label>`).join('')}</span>
      </div>`;
    }).join('');
    return `<div class="card plan-card" data-plan="${esc(plan.id)}">
      <div class="plan-head">
        <div>
          <span class="plan-name">${esc(plan.name)}</span>
          <span class="plan-meta">　${esc(plan.startDate)} 起 ${plan.days} 天 ｜ 完成 ${done}/${total}（${pct}%）</span>
        </div>
        <div class="plan-ctrl">
          <button class="ghost-btn" data-exp="${esc(plan.id)}">${plan._open ? '收合' : '展開'}每日進度</button>
          <button class="ghost-btn" data-export="${esc(plan.id)}">⬇️ 匯出 CSV</button>
          <button class="danger-btn" data-del="${esc(plan.id)}">🗑 刪除</button>
        </div>
      </div>
      <div class="progress"><div style="width:${pct}%"></div></div>
      <div class="plan-days" style="${plan._open ? '' : 'display:none'}">${rows}</div>
    </div>`;
  }).join('');

  el.querySelectorAll('[data-exp]').forEach(b => b.onclick = async () => {
    const p = (await idbGetAll('plans')).find(x => x.id === b.dataset.exp);
    p._open = !p._open;
    await idbPut('plans', p);
    loadPlans();
  });
  el.querySelectorAll('[data-export]').forEach(b => b.onclick = () => exportPlanCsv(b.dataset.export));
  el.querySelectorAll('[data-del]').forEach(b => b.onclick = async () => {
    if (!confirm('確定刪除這個學習計畫？')) return;
    await idbDelete('plans', b.dataset.del);
    loadPlans();
  });
  el.querySelectorAll('.day-item input').forEach(cb => cb.onchange = async () => {
    const key = cb.dataset.key; // w|date|word 或 i|date|idiom
    const [type, date, item] = [key.slice(0, 1), key.slice(2).split('|')[0], key.slice(2).split('|').slice(1).join('|')];
    const planId = cb.closest('.plan-card').dataset.plan;
    const plans = await idbGetAll('plans');
    const plan = plans.find(x => x.id === planId);
    const en = plan.entries.find(e => e.date === date);
    if (type === 'w') { const it = en.words.find(w => w.word === item); if (it) it.done = cb.checked; }
    else { const it = en.idioms.find(i => i.idiom === item); if (it) it.done = cb.checked; }
    await idbPut('plans', plan);
    loadPlans();
  });
}

/* ================= 養成遊戲（電子雞/狗/猫） ================= */
const PET_TYPES = {
  chicken: { name: '電子雞', emoji: ['🥚', '🐣', '🐔', '🎉'], maxLv: 30, hungerDecay: 8, funDecay: 10 },
  dog:     { name: '電子狗', emoji: ['🐶', '🐕', '🦮'], maxLv: 30, hungerDecay: 6, funDecay: 8 },
  cat:     { name: '電子貓', emoji: ['🐱', '🐈', '🐈⬛'], maxLv: 30, hungerDecay: 5, funDecay: 7 }
};
const PET_STORE = 'pet';

function defaultPet() {
  return { type: 'chicken', name: '小雞', lv: 1, xp: 0, hunger: 100, fun: 100, fed: 0, played: 0, correct: 0, wrong: 0, createdAt: Date.now() };
}

function stageEmoji(p) {
  const t = PET_TYPES[p.type];
  if (p.lv >= 10) return t.emoji[t.emoji.length - 1];
  if (p.lv >= 5) return t.emoji[Math.min(1, t.emoji.length - 2)];
  return t.emoji[0];
}

function xpMultiplier(p) {
  // 等級加權：Lv2 = 1.1 倍、Lv3 = 1.2 倍 ... 每升一等 +0.1
  return 1 + (Math.max(1, p.lv) - 1) * 0.1;
}

async function getPet() {
  const db = await openDB();
  return new Promise((res, rej) => {
    const tx = db.transaction(PET_STORE, 'readonly');
    const rq = tx.objectStore(PET_STORE).get('pet');
    rq.onsuccess = () => res(rq.result || defaultPet());
    rq.onerror = () => rej(rq.error);
  });
}

async function renderPet() {
  const pet = await getPet();
  const root = $('#petCard');
  // 首次：尚未選擇寵物
  if (!pet.created) {
    root.innerHTML = `
      <div class="card">
        <div style="font-size:18px;font-weight:700;text-align:center;margin-bottom:4px;">🐣 選擇你的寵物夥伴！</div>
        <div style="font-size:13px;color:var(--muted);text-align:center;margin-bottom:8px;">答題得分可以讓牠成長茁壯～</div>
        <div class="pet-choose">
          <button class="pet-choice-btn" data-pick="chicken"><span class="emoji">🐔</span>電子雞</button>
          <button class="pet-choice-btn" data-pick="dog"><span class="emoji">🐶</span>電子狗</button>
          <button class="pet-choice-btn" data-pick="cat"><span class="emoji">🐱</span>電子貓</button>
        </div>
      </div>`;
    $('#petQuiz').innerHTML = '';
    const names = { chicken: '小雞', dog: '小狗', cat: '小貓' };
    root.querySelectorAll('[data-pick]').forEach(btn => btn.onclick = async () => {
      const type = btn.dataset.pick;
      const p = defaultPet();
      p.type = type; p.name = names[type]; p.created = true;
      await idbPut(PET_STORE, p, 'pet');
      renderPet();
    });
    return;
  }
  const t = PET_TYPES[pet.type];
  const xpNeed = pet.lv * 10;
  root.innerHTML = `
    <div class="card">
      <div class="pet-head">
        <div class="pet-stage" title="Lv.${pet.lv}">${stageEmoji(pet)}</div>
        <div class="pet-info">
          <div class="pet-name">${esc(pet.name)} <span style="font-size:13px;color:var(--muted)">(${t.name})</span></div>
          <div class="pet-level">Lv.${pet.lv} / ${t.maxLv}　${pet.lv >= t.maxLv ? '🌟 已滿等！' : ''}</div>
          <div class="pet-xp-text">經驗值 ${pet.xp.toFixed(1)} / ${xpNeed}（答對 +${xpMultiplier(pet).toFixed(1)} EXP，隨等級加權）</div>
          <div class="progress"><div style="width:${Math.min(100, pet.xp / xpNeed * 100)}%"></div></div>
          <div style="font-size:13px;color:var(--muted);margin-top:6px;">
            🍗 飽食度 ${pet.hunger}%　🎾 心情 ${pet.fun}%　|　答對 ${pet.correct} / 答錯 ${pet.wrong}
          </div>
          <div class="pet-actions">
            <button class="chip-btn" data-feed>🍗 餵食 +15</button>
            <button class="chip-btn" data-play>🎾 玩 +15</button>
            <button class="chip-btn" data-name>✏️ 改名</button>
            <button class="chip-btn" data-retrain style="border-color:var(--danger);color:var(--danger);">🔄 重新選擇</button>
          </div>
          <div class="pet-msg" id="petMsg"></div>
        </div>
      </div>
    </div>`;

  root.querySelector('[data-feed]').onclick = async () => {
    const p = await getPet();
    p.hunger = Math.min(100, p.hunger + 15); p.fed++;
    await idbPut(PET_STORE, p, 'pet');
    renderPet();
  };
  root.querySelector('[data-play]').onclick = async () => {
    const p = await getPet();
    p.fun = Math.min(100, p.fun + 15); p.played++;
    await idbPut(PET_STORE, p, 'pet');
    renderPet();
  };
  root.querySelector('[data-name]').onclick = async () => {
    const p = await getPet();
    const nn = prompt('幫寵物取新名字：', p.name);
    if (nn && nn.trim()) { p.name = nn.trim(); await idbPut(PET_STORE, p, 'pet'); renderPet(); }
  };
  const retrainBtn = root.querySelector('[data-retrain]');
  if (retrainBtn) retrainBtn.onclick = async () => {
    if (!confirm('確定要重新選擇寵物嗎？目前的進度（等級/經驗/飽食/心情）將全部重置！')) return;
    await idbDelete(PET_STORE, 'pet');
    renderPet();
  };
  renderQuizPanel();
}

function renderQuizPanel() {
  $('#petQuiz').innerHTML = `
    <div class="card">
      <div style="font-size:16px;font-weight:700;margin-bottom:10px;">❓ 四選一答題</div>
      <div class="plan-form-row">
        <label>題庫
          <select id="quizType" style="padding:7px 10px;border-radius:8px;border:1px solid var(--border);background:var(--card);color:var(--text);font-size:14px;">
            <option value="word">🇺🇸 英文單字（英文→中文）</option>
            <option value="sentence">🇺🇸 英文句子（中文→英文）</option>
            <option value="idiom">🀄 國語成語（解釋→成語）</option>
          </select>
        </label>
        <label>題數
          <input type="number" id="quizCount" min="1" max="50" value="5" style="width:70px;padding:7px 10px;border-radius:8px;border:1px solid var(--border);background:var(--card);color:var(--text);font-size:14px;">
        </label>
        <button class="primary-btn" id="btnStartQuiz">🎯 開始答題</button>
      </div>
      <div id="quizArea"></div>
    </div>`;
  $('#btnStartQuiz').onclick = startQuiz;
}

function buildQuiz(seed) {
  const type = $('#quizType').value;
  const count = Math.min(50, Math.max(1, parseInt($('#quizCount').value) || 5));
  const qs = [];
  if (type === 'word') {
    const pool = shuffle(seed.words);
    for (let i = 0; i < count; i++) {
      const w = pool[i % pool.length];
      const others = shuffle(seed.words.filter(x => x.word !== w.word)).slice(0, 3);
      if (others.length < 3) continue;
      const opts = shuffle([w, ...others]).map(x => x.meaning || x.word);
      qs.push({ q: w.word, opts, ans: w.meaning || w.word, tag: '單字' });
    }
  } else if (type === 'sentence') {
    const sents = [];
    seed.words.forEach(w => (w.sentences || []).forEach(s => sents.push({ s, w })));
    const pool = shuffle(sents);
    for (let i = 0; i < count; i++) {
      const it = pool[i % pool.length];
      const others = shuffle(sents.filter(x => x !== it)).slice(0, 3);
      if (others.length < 3) continue;
      const opts = shuffle([it, ...others]).map(x => x.s.sentence);
      qs.push({ q: it.s.translation, opts, ans: it.s.sentence, tag: '句子' });
    }
  } else {
    const pool = shuffle(seed.idioms);
    for (let i = 0; i < count; i++) {
      const idm = pool[i % pool.length];
      const others = shuffle(seed.idioms.filter(x => x.idiom !== idm.idiom)).slice(0, 3);
      if (others.length < 3) continue;
      const opts = shuffle([idm, ...others]).map(x => x.idiom);
      qs.push({ q: idm.explanation, opts, ans: idm.idiom, tag: '成語' });
    }
  }
  return qs;
}

function showQuiz(qs) {
  let idx = 0, score = 0;
  const area = $('#quizArea');
  function renderQ() {
    if (idx >= qs.length) return showResult(score, qs.length);
    const q = qs[idx];
    area.innerHTML = `
      <div class="quiz-progress"><div style="width:${idx / qs.length * 100}%"></div></div>
      <div style="font-size:13px;color:var(--muted);">第 ${idx + 1} / ${qs.length} 題（${q.tag}）</div>
      <div class="quiz-prompt">${esc(q.q)}</div>
      ${q.opts.map((o, oi) => `<button class="option-btn" data-oi="${oi}">${esc(o)}</button>`).join('')}`;
    area.querySelectorAll('.option-btn').forEach(btn => btn.onclick = async () => {
      const chosen = q.opts[+btn.dataset.oi];
      const ok = chosen === q.ans;
      area.querySelectorAll('.option-btn').forEach(b => b.disabled = true);
      area.querySelectorAll('.option-btn').forEach(b => {
        if (q.opts[+b.dataset.oi] === q.ans) b.classList.add('correct');
        else if (+b.dataset.oi === +btn.dataset.oi) b.classList.add('wrong');
      });
      if (ok) { score++; await addXp(1); }
      else { await addWrong(); }
      setTimeout(() => { idx++; renderQ(); }, 900);
    });
  }
  renderQ();
}

async function addXp(n) {
  const p = await getPet();
  const gain = n * xpMultiplier(p);   // 加權：Lv2=1.1x、Lv3=1.2x...
  p.xp += gain; p.correct++;
  const t = PET_TYPES[p.type];
  while (p.xp >= p.lv * 10 && p.lv < t.maxLv) { p.xp -= p.lv * 10; p.lv++; }
  if (p.lv >= t.maxLv) p.xp = Math.min(p.xp, p.lv * 10);
  await idbPut(PET_STORE, p, 'pet');
}

async function addWrong() {
  const p = await getPet();
  p.wrong++;
  await idbPut(PET_STORE, p, 'pet');
}

async function showResult(score, total) {
  const p = await getPet();
  const t = PET_TYPES[p.type];
  const perfect = score === total && total > 0;
  $('#quizArea').innerHTML = `
    <div class="result-card">
      <div style="font-size:52px;">${perfect ? '🏆' : score >= total * 0.6 ? '🎉' : '💪'}</div>
      <div style="font-size:22px;font-weight:700;margin:8px 0;">${score} / ${total} 題答對</div>
      <div style="font-size:14px;color:var(--muted);margin-bottom:12px;">${perfect ? '太完美了！全對！' : score >= total * 0.6 ? '很棒！繼續加油！' : '別灰心，再試一次！'}</div>
      <button class="primary-btn" id="btnAgain">🔁 再玩一次</button>
    </div>`;
  $('#btnAgain').onclick = startQuiz;
  renderPet();
}

function startQuiz() {
  const qs = buildQuiz({ words: allWords, idioms: allIdioms });
  if (!qs.length) { $('#quizArea').innerHTML = '<div class="empty">題庫不足（至少需要 4 個單字/句子/成語才能出四選一）</div>'; return; }
  showQuiz(qs);
}

/* ================= CSV 匯出 / 匯入 ================= */
function csvEscape(v) {
  v = String(v == null ? '' : v);
  return /[",\r\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v;
}
function downloadCsv(filename, text) {
  const blob = new Blob(['\uFEFF' + text], { type: 'text/csv;charset=utf-8' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = filename;
  a.click();
  URL.revokeObjectURL(a.href);
}
async function exportPlanCsv(planId) {
  const plans = await idbGetAll('plans');
  const plan = plans.find(x => x.id === planId);
  if (!plan) return;
  const rows = [['計畫名稱', '日期', '類型', '項目', '完成']];
  plan.entries.forEach(e => {
    e.words.forEach(w => rows.push([plan.name, e.date, '單字', w.word, w.done ? '是' : '否']));
    e.idioms.forEach(i => rows.push([plan.name, e.date, '成語', i.idiom, i.done ? '是' : '否']));
  });
  downloadCsv('學習計畫_' + plan.name + '.csv', rows.map(r => r.map(csvEscape).join(',')).join('\r\n'));
}

function parseCsv(text) {
  const rows = []; let row = [], cur = '', inQ = false;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (inQ) {
      if (ch === '"') { if (text[i + 1] === '"') { cur += '"'; i++; } else inQ = false; }
      else cur += ch;
    } else if (ch === '"') inQ = true;
    else if (ch === ',') { row.push(cur); cur = ''; }
    else if (ch === '\n') { row.push(cur); rows.push(row); row = []; cur = ''; }
    else if (ch !== '\r') cur += ch;
  }
  if (cur.length || row.length) { row.push(cur); rows.push(row); }
  return rows;
}

$('#btnImportCsv').onclick = () => $('#csvFile').click();
$('#csvFile').onchange = async e => {
  const file = e.target.files[0];
  if (!file) return;
  const text = await file.text();
  try {
    const rows = parseCsv(text).filter(r => r.length >= 4 && r[0].trim() && r[0].trim() !== '計畫名稱');
    if (!rows.length) throw new Error('CSV 內容為空或格式不符');
    const byName = {};
    rows.forEach(r => {
      const name = r[0].trim(), date = (r[1] || '').trim(), type = (r[2] || '').trim(), item = (r[3] || '').trim();
      const done = (r[4] || '').trim() === '是';
      (byName[name] = byName[name] || []).push({ date, type, item, done });
    });
    let count = 0;
    for (const [name, list] of Object.entries(byName)) {
      const dates = [...new Set(list.map(r => r.date))].sort();
      const entries = dates.map(d => ({ date: d, words: [], idioms: [] }));
      list.forEach(r => {
        const en = entries.find(x => x.date === r.date);
        if (r.type === '單字') en.words.push({ word: r.item, done: r.done });
        else en.idioms.push({ idiom: r.item, done: r.done });
      });
      await idbPut('plans', {
        id: 'plan_' + Date.now() + '_' + count,
        name, startDate: dates[0] || todayStr(), days: dates.length,
        createdAt: new Date().toISOString(), entries
      });
      count++;
    }
    $('#importMsg').textContent = `✅ 已匯入 ${count} 個學習計畫`;
    loadPlans();
  } catch (err) {
    $('#importMsg').textContent = '❌ 匯入失敗：' + err.message;
  }
  e.target.value = '';
};

/* ================= 工具 ================= */
function esc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

$('#planStart').value = todayStr();
loadAll();
