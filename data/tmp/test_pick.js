// 模擬 renderPickLists：檢查成語 checkbox 是否真的被渲染
const fs = require('fs');
const vm = require('vm');
const html = fs.readFileSync('_online.html', 'utf-8');
const js = html.match(/<script>([\s\S]*?)<\/script>/)[1];

// 追蹤 innerHTML 賦值
const innerHTMLs = {};
const elements = {};
function makeEl(id) {
  return {
    id, innerHTML: '', value: '', checked: false, onclick: null, dataset: {},
    querySelectorAll: () => [], addEventListener: () => {}, style: {},
    classList: { add: () => {}, remove: () => {}, toggle: () => {} },
    setAttribute: () => {}, getAttribute: () => null, appendChild: () => {}, remove: () => {},
  };
}
['pickWords', 'pickIdioms', 'wordList', 'idiomList', 'alphaBar', 'topicBar', 'catBar'].forEach(id => {
  elements[id] = makeEl(id);
});

const sandbox = {
  console, setTimeout, clearTimeout, Date, Math, JSON, Promise, isNaN, parseInt, parseFloat,
  location: { href: '' },
  localStorage: { getItem: () => null, setItem: () => {}, removeItem: () => {} },
  document: {
    documentElement: { dataset: {}, style: {} },
    getElementById: id => elements[id] || makeEl(id),
    querySelector: () => makeEl('q'),
    querySelectorAll: () => [],
    createElement: () => makeEl('c'),
    addEventListener: () => {},
  },
  $: id => elements[id.replace('#', '')] || makeEl('x'),
};
vm.createContext(sandbox);

let error = null;
try {
  vm.runInContext(js, sandbox);
  // 觸發 renderPickLists（若有 loadAll 自動呼叫）
  if (sandbox.renderPickLists) sandbox.renderPickLists();
} catch (e) {
  error = e;
}
if (error) console.log('執行錯誤:', error.message);
else {
  const words = JSON.parse(fs.readFileSync('data/words.json', 'utf-8'));
  const idioms = JSON.parse(fs.readFileSync('data/idioms.json', 'utf-8'));
  console.log('pickWords checkbox 數:', (elements.pickWords.innerHTML.match(/type="checkbox"/g) || []).length, '期望', words.length);
  console.log('pickIdioms checkbox 數:', (elements.pickIdioms.innerHTML.match(/type="checkbox"/g) || []).length, '期望', idioms.length);
  console.log('pickIdioms 內容前 200 字:', elements.pickIdioms.innerHTML.slice(0, 200));
}
