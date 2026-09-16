"use strict";
const eng = require('./masyu_engine.js');

function assert(cond, msg){ if(!cond){ console.error('FAIL:', msg); process.exitCode = 1; } else { console.log('ok:', msg); } }

// ---- 1. Sanity: loop generation produces a valid simple closed loop ----
(function testLoopValidity(){
  for(const P of [5,7,9]){
    let okCount = 0;
    for(let i=0;i<20;i++){
      const path = eng.growRegionLoop(P, 0.55, 30);
      if(!path) continue;
      // check all points distinct
      const seen = new Set();
      let distinct = true;
      for(const [r,c] of path){ const k=r+','+c; if(seen.has(k)){ distinct=false; break; } seen.add(k); }
      // check consecutive points are grid-adjacent, including wraparound
      let adjacentOk = true;
      for(let j=0;j<path.length;j++){
        const a = path[j], b = path[(j+1)%path.length];
        const dist = Math.abs(a[0]-b[0]) + Math.abs(a[1]-b[1]);
        if(dist !== 1){ adjacentOk = false; break; }
      }
      if(distinct && adjacentOk) okCount++;
    }
    assert(okCount >= 15, `P=${P}: at least 15/20 loop generations valid (got ${okCount})`);
  }
})();

// ---- 2. Candidate derivation sanity: candidates lie on loop, no overlap ----
(function testCandidates(){
  const P = 7;
  const path = eng.growRegionLoop(P, 0.6, 40);
  assert(!!path, 'P=7 loop generated for candidate test');
  if(!path) return;
  const { whites, blacks } = eng.deriveCandidates(P, path);
  const onLoop = new Set(path.map(([r,c])=>r+','+c));
  let allOnLoop = true;
  for(const [r,c] of whites.concat(blacks)) if(!onLoop.has(r+','+c)) allOnLoop = false;
  assert(allOnLoop, 'all candidate clues lie on the generated loop');
  const whiteKeys = new Set(whites.map(([r,c])=>r+','+c));
  let noOverlap = true;
  for(const [r,c] of blacks) if(whiteKeys.has(r+','+c)) noOverlap = false;
  assert(noOverlap, 'white and black candidates never overlap');
})();

// ---- 3. Solver correctness on a tiny hand-built 3x3-point puzzle ----
// A 2x2 unit square loop (points 0,0 - 0,1 - 1,1 - 1,0) on a 3x3 point grid
// with NO clues should have MANY solutions (any sub-square/rectangle loop
// qualifies), so count should quickly exceed the limit.
(function testTinyNoClue(){
  const P = 3;
  const clueGrid = Array.from({length:P},()=>Array(P).fill(0));
  const res = eng.countSolutions(P, clueGrid, 5, 50000);
  assert(res.count >= 2, `3x3 grid with no clues has multiple loop solutions (got ${res.count})`);
})();

// ---- 4. Solver correctness: brute-force cross-check on a small generated puzzle ----
function bruteForceCount(P, clueGrid){
  // Enumerate all edge subsets directly (only feasible for very small P).
  const hCount = P*(P-1), vCount = (P-1)*P;
  const totalEdges = hCount+vCount;
  if(totalEdges > 20) throw new Error('too big for brute force');
  let count = 0;
  const H = Array.from({length:P},()=>new Int8Array(P-1));
  const V = Array.from({length:P-1},()=>new Int8Array(P));
  for(let mask=0; mask < (1<<totalEdges); mask++){
    let bit=0;
    for(let r=0;r<P;r++) for(let c=0;c<P-1;c++) H[r][c] = (mask>>bit++)&1;
    for(let r=0;r<P-1;r++) for(let c=0;c<P;c++) V[r][c] = (mask>>bit++)&1;
    // degree check
    let ok = true;
    for(let r=0;r<P && ok;r++) for(let c=0;c<P && ok;c++){
      const l = c>0?H[r][c-1]:0, u = r>0?V[r-1][c]:0, rr = c<P-1?H[r][c]:0, d = r<P-1?V[r][c]:0;
      const deg = l+u+rr+d;
      if(deg!==0 && deg!==2) ok=false;
      const clue = clueGrid[r][c];
      if(clue){
        if(deg!==2){ ok=false; }
        else {
          const straight = (l&&rr)||(u&&d);
          if(clue===1 && !straight) ok=false;
          if(clue===2 && straight) ok=false;
        }
      }
    }
    if(!ok) continue;
    // connectivity: exactly one cycle covering all degree>0 points
    const pts = [];
    for(let r=0;r<P;r++) for(let c=0;c<P;c++){
      const l = c>0?H[r][c-1]:0, u = r>0?V[r-1][c]:0, rr = c<P-1?H[r][c]:0, d = r<P-1?V[r][c]:0;
      if(l+u+rr+d>0) pts.push(r*P+c);
    }
    if(pts.length===0) continue;
    const parent = {}; pts.forEach(p=>parent[p]=p);
    function find(x){ while(parent[x]!==x) x=parent[x]; return x; }
    function union(a,b){ const ra=find(a),rb=find(b); if(ra!==rb) parent[ra]=rb; }
    for(let r=0;r<P;r++) for(let c=0;c<P-1;c++) if(H[r][c]) union(r*P+c, r*P+c+1);
    for(let r=0;r<P-1;r++) for(let c=0;c<P;c++) if(V[r][c]) union(r*P+c, (r+1)*P+c);
    const roots = new Set(pts.map(find));
    if(roots.size !== 1) continue;
    // white/black neighbor conditions
    let deferOk = true;
    for(let r=0;r<P && deferOk;r++) for(let c=0;c<P && deferOk;c++){
      const clue = clueGrid[r][c]; if(!clue) continue;
      const l = c>0?H[r][c-1]:0, u = r>0?V[r-1][c]:0, rr = c<P-1?H[r][c]:0, d = r<P-1?V[r][c]:0;
      const nbrs=[]; if(l)nbrs.push([r,c-1]); if(u)nbrs.push([r-1,c]); if(rr)nbrs.push([r,c+1]); if(d)nbrs.push([r+1,c]);
      const straightOf=(pr,pc)=>{ const ll=pc>0?H[pr][pc-1]:0, uu=pr>0?V[pr-1][pc]:0, rrr=pc<P-1?H[pr][pc]:0, dd=pr<P-1?V[pr][pc]:0; return (ll&&rrr)||(uu&&dd); };
      const s1=straightOf(nbrs[0][0],nbrs[0][1]), s2=straightOf(nbrs[1][0],nbrs[1][1]);
      if(clue===1 && s1 && s2) deferOk=false;
      if(clue===2 && (!s1||!s2)) deferOk=false;
    }
    if(!deferOk) continue;
    count++;
  }
  return count;
}

(function testBruteForceCrossCheck(){
  // P=3 grid: hCount=3*2=6, vCount=2*3=6, total 12 edges -> 4096 combos, feasible.
  const P = 3;
  for(let trial=0; trial<6; trial++){
    const path = eng.growRegionLoop(P, 0.6, 30);
    if(!path) continue;
    const { whites, blacks } = eng.deriveCandidates(P, path);
    const clueGrid = eng.makeClueGrid(P, whites, blacks);
    const solverRes = eng.countSolutions(P, clueGrid, 10, 100000);
    const bruteRes = bruteForceCount(P, clueGrid);
    assert(solverRes.count === bruteRes, `P=3 trial${trial}: solver(${solverRes.count}) matches brute force(${bruteRes})`);
  }
  // Also test with a couple of random partial clue-subsets (not just full-candidate sets)
  for(let trial=0; trial<6; trial++){
    const path = eng.growRegionLoop(P, 0.6, 30);
    if(!path) continue;
    const { whites, blacks } = eng.deriveCandidates(P, path);
    // randomly drop some candidates
    const w2 = whites.filter(()=>Math.random()<0.6);
    const b2 = blacks.filter(()=>Math.random()<0.6);
    const clueGrid = eng.makeClueGrid(P, w2, b2);
    const solverRes = eng.countSolutions(P, clueGrid, 10, 100000);
    const bruteRes = bruteForceCount(P, clueGrid);
    assert(solverRes.count === bruteRes, `P=3 partial-clue trial${trial}: solver(${solverRes.count}) matches brute force(${bruteRes})`);
  }
})();

console.log('\n--- correctness tests complete ---\n');
