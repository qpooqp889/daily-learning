// Extract <script> content from index.html and syntax-check with new Function / node --check
const fs = require('fs');
const html = fs.readFileSync('C:\\Users\\twric\\.qclaw\\workspace\\daily-learning\\index.html', 'utf8');
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if (!m) { console.log('NO SCRIPT FOUND'); process.exit(1); }
fs.writeFileSync('C:\\Users\\twric\\.qclaw\\workspace\\daily-learning\\data\\_extracted.js', m[1]);
console.log('extracted', m[1].length, 'chars');
