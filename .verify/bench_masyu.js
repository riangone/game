"use strict";
const eng = require('./masyu_engine.js');

function bench(P, reduceFraction, trials, opts){
  const times = [];
  let fails = 0;
  for(let i=0;i<trials;i++){
    const t0 = Date.now();
    const res = eng.generatePuzzle(P, Object.assign({ reduceFraction }, opts));
    const t1 = Date.now();
    if(!res){ fails++; continue; }
    times.push(t1-t0);
  }
  times.sort((a,b)=>a-b);
  const sum = times.reduce((a,b)=>a+b,0);
  const avg = times.length ? (sum/times.length).toFixed(1) : 'n/a';
  const max = times.length ? times[times.length-1] : 'n/a';
  const p95 = times.length ? times[Math.floor(times.length*0.95)] : 'n/a';
  console.log(`P=${P} reduceFrac=${reduceFraction} trials=${trials} fails=${fails} avg=${avg}ms p95=${p95}ms max=${max}ms`);
  return { avg, max, fails };
}

console.log('=== Masyu generation benchmark (solveBudget=250000, pruneBudget=120000) ===');
for(const P of [5,7,9]){
  for(const rf of [0.25, 0.55, 0.9]){ // easy / normal / hard reduction amounts
    bench(P, rf, P>=9 ? 10 : 20);
  }
}

console.log('\n=== Stress test: larger node budgets to see worst-case behavior ===');
for(const P of [9]){
  bench(P, 0.9, 15, { solveBudget: 400000, pruneBudget: 200000 });
}

console.log('\n=== Solver-only worst case: no-clue small grids (should stay bounded by nodeBudget) ===');
for(const P of [5,7,9]){
  const clueGrid = Array.from({length:P},()=>Array(P).fill(0));
  const t0=Date.now();
  const res = eng.countSolutions(P, clueGrid, 2, 300000);
  const t1=Date.now();
  console.log(`P=${P} no-clue countSolutions: count=${res.count} nodes=${res.nodes} time=${t1-t0}ms`);
}
