// Simulate pet XP logic after revamp
function xpMultiplier(p) { return 1 + (Math.max(1, p.lv) - 1) * 0.1; }

function addXp(p, n) {
  const gain = n * xpMultiplier(p);
  p.xp += gain; p.correct++;
  while (p.xp >= p.lv * 50 && p.lv < 30) { p.xp -= p.lv * 50; p.lv++; }
  if (p.lv >= 30) p.xp = Math.min(p.xp, p.lv * 50);
  return gain;
}

// scenario: lv1 pet answers 5 questions
let p = { lv: 1, xp: 0, correct: 0 };
console.log('Lv1 pet, 5 correct answers:');
for (let i = 0; i < 5; i++) {
  const g = addXp(p, 1);
  console.log(`  Q${i+1}: gain=${g.toFixed(2)} -> lv=${p.lv}, xp=${p.xp.toFixed(1)}`);
}

// scenario: level up behavior — lv10 needs 500 xp per level
p = { lv: 10, xp: 490, correct: 0 };
console.log('\nLv10 pet at 490/500:');
const g = addXp(p, 1); // 1 * 1.9 = 1.9 -> 491.9, no level up
console.log(`  gain=${g.toFixed(2)} -> lv=${p.lv}, xp=${p.xp.toFixed(1)}`);

// max level behavior
p = { lv: 30, xp: 1490, correct: 0 };
console.log('\nLv30 pet (max):');
const g2 = addXp(p, 1);
console.log(`  gain=${g2.toFixed(2)} -> lv=${p.lv}, xp=${p.xp.toFixed(1)} (capped at 1500)`);

// multiplier curve
console.log('\nMultiplier curve:');
for (let lv = 1; lv <= 30; lv += 5) {
  console.log(`  Lv${lv}: x${xpMultiplier({lv}).toFixed(1)} -> +${(1*xpMultiplier({lv})).toFixed(2)} EXP/題`);
}
