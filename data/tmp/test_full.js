// 完整模擬：注入真實資料，執行 loadAll，檢查 renderPickLists 是否執行、有無錯誤
const fs = require('fs');
const vm = require('vm');
const html = fs.readFileSync('index.html', 'utf-8');
const js = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const words = JSON.parse(fs.readFileSync('data/words.json', 'utf-8'));
const idioms = JSON.parse(fs.readFileSync('data/idioms.json', 'utf-8'));

const innerHTMLs = {};
const els = {};
function makeEl(id) {
  return {
    id, innerHTML: '', value: '', checked: false, onclick: null, dataset: {},
    querySelectorAll: () => [], addEventListener: () => {}, style: {}, textContent: '',
    classList: { add: () => {}, remove: () => {}, toggle: () => {} },
    setAttribute: () => {}, getAttribute: () => null, appendChild: () => {}, remove: () => {},
  };
}
const ids = ['pickWords','pickIdioms','wordList','idiomList','alphaBar','topicBar','catBar','searchWord','searchIdiom','createMsg','btnCreatePlan','planList','petCard','petQuiz'];
ids.forEach(id => els[id] = makeEl(id));
const allEls = new Map();
function getEl(id) { if (!allEls.has(id)) allEls.set(id, makeEl(id)); return allEls.get(id); }

const sandbox = {
  console, setTimeout: (fn) => 0, clearTimeout, Date, Math, JSON, Promise, isNaN, parseInt, parseFloat,
  location: { href: '' },
  localStorage: { getItem: () => null, setItem: () => {}, removeItem: () => {} },
  indexedDB: undefined,
  fetch: (url) => {
    if (url.includes('words.json')) return Promise.resolve({ json: () => Promise.resolve(words), ok: true });
    if (url.includes('idioms.json')) return Promise.resolve({ json: () => Promise.resolve(idioms), ok: true });
    return Promise.resolve({ json: () => Promise.resolve([]), ok: true });
  },
  document: {
    documentElement: { dataset: {}, style: {} },
    getElementById: id => { if (id === 'pickWords') return els.pickWords; if (id === 'pickIdioms') return els.pickIdioms; return getEl(id); },
    querySelector: () => getEl('q'),
    querySelectorAll: () => [],
    createElement: () => getEl('c'),
    addEventListener: () => {},
  },
  $: id => { const key = id.replace('#',''); return els[key] || getEl(key); },
};
vm.createContext(sandbox);

let error = null;
try {
  vm.runInContext(js, sandbox);
} catch (e) { error = e; }

if (error) {
  console.log('SCRIPT 執行錯誤:', error.message);
  console.log(error.stack.split('\n').slice(0, 4).join('\n'));
} else {
  // 手動呼叫 loadAll（fetch 是 async）
  sandbox.loadAll && sandbox.loadAll().then(() => {
    setTimeout(() => {
      const wc = (els.pickWords.innerHTML.match(/type="checkbox"/g) || []).length;
      const ic = (els.pickIdioms.innerHTML.match(/type="checkbox"/g) || []).length;
      console.log('pickWords:', wc, 'pickIdioms:', ic);
      console.log('wordList 渲染:', els.wordList.innerHTML.slice(0, 100));
      console.log('idiomList 渲染:', els.idiomList.innerHTML.slice(0, 100));
    }, 100);
  }).catch(e => console.log('loadAll 錯誤:', e.message));
}
