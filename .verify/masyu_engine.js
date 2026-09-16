"use strict";
/* ============================================================
   Masyu (数珠链) core engine: board model, generator, CSP solver.
   Pure JS, no DOM. Designed to be copy-pasted into masyu.html's
   <script> block verbatim, and independently load-tested under Node.

   Board: P x P lattice points (P = 5, 7, 9 ...). Player draws edges
   between orthogonally-adjacent points to form a single simple closed
   loop (every point has degree 0 or 2, no self-intersection).
   ============================================================ */

function shuffle(arr){ for(let i=arr.length-1;i>0;i--){ const j=(Math.random()*(i+1))|0; const t=arr[i]; arr[i]=arr[j]; arr[j]=t; } return arr; }
function randInt(n){ return (Math.random()*n)|0; }

/* ================= Union-Find with rollback (no path compression,
   so a union can be undone by simply restoring the child's parent
   pointer and the parent's size -- required for backtracking search) ================= */
class DSU {
  constructor(n){ this.parent = new Int32Array(n); for(let i=0;i<n;i++) this.parent[i]=i; this.size = new Int32Array(n).fill(1); this.stack = []; }
  find(x){ while(this.parent[x]!==x) x = this.parent[x]; return x; }
  union(a,b){
    let ra = this.find(a), rb = this.find(b);
    if(ra===rb){ this.stack.push(0); return false; } // would close a cycle; no structural change
    if(this.size[ra] < this.size[rb]){ const t=ra; ra=rb; rb=t; }
    this.stack.push(1 | (rb<<8) | (ra<<24)); // not used; keep explicit object below instead
    this.stack[this.stack.length-1] = { rb, ra, raSizeBefore: this.size[ra] };
    this.parent[rb] = ra;
    this.size[ra] += this.size[rb];
    return true;
  }
  undo(){
    const rec = this.stack.pop();
    if(rec === 0) return; // was a no-op (cycle-detected) union
    this.parent[rec.rb] = rec.rb;
    this.size[rec.ra] = rec.raSizeBefore;
  }
}

/* ================= Region-blob -> boundary-loop generator =================
   A random simply-connected polyomino (no holes, no diagonal "pinch"
   points) grown on the (P-1)x(P-1) cell grid always has a boundary that
   is a single simple closed loop on the P x P point lattice -- this
   sidesteps having to hand-write a self-avoiding-walk loop grower. */
function causesPinch(inside, r, c, H, W){
  for(const [dr,dc] of [[-1,-1],[-1,1],[1,-1],[1,1]]){
    const rr=r+dr, cc=c+dc;
    if(rr<0||rr>=H||cc<0||cc>=W) continue;
    if(!inside[rr][cc]) continue;
    const b1r=r+dr, b1c=c;
    const b2r=r, b2c=c+dc;
    const b1in = (b1r>=0&&b1r<H&&b1c>=0&&b1c<W) ? inside[b1r][b1c] : false;
    const b2in = (b2r>=0&&b2r<H&&b2c>=0&&b2c<W) ? inside[b2r][b2c] : false;
    if(!b1in && !b2in) return true; // diagonal touch with no orthogonal bridge -> boundary would pinch
  }
  return false;
}

function tryGrowBlob(W, H, target){
  const inside = Array.from({length:H}, () => Array(W).fill(false));
  const sr = randInt(H), sc = randInt(W);
  inside[sr][sc] = true;
  let count = 1;
  const frontier = [];
  function addFrontierAround(r,c){
    for(const [dr,dc] of [[-1,0],[1,0],[0,-1],[0,1]]){
      const nr=r+dr, nc=c+dc;
      if(nr>=0&&nr<H&&nc>=0&&nc<W&&!inside[nr][nc]) frontier.push([nr,nc]);
    }
  }
  addFrontierAround(sr,sc);
  let guard = 0;
  while(count<target && frontier.length>0 && guard++ < target*50){
    const i = randInt(frontier.length);
    const [r,c] = frontier[i];
    frontier[i] = frontier[frontier.length-1]; frontier.pop();
    if(inside[r][c]) continue;
    if(causesPinch(inside,r,c,H,W)) continue;
    inside[r][c] = true; count++;
    addFrontierAround(r,c);
  }
  if(count < target*0.5) return null;
  return inside;
}

function hasHoleOrTouchesFrame(inside, W, H){
  // BFS the outside region from all border cells; if any non-inside cell
  // is unreachable, the blob encloses a hole (would create a 2nd loop).
  const seen = Array.from({length:H}, () => Array(W).fill(false));
  const q = [];
  function tryPush(r,c){ if(!inside[r][c] && !seen[r][c]){ seen[r][c]=true; q.push([r,c]); } }
  for(let c=0;c<W;c++){ tryPush(0,c); tryPush(H-1,c); }
  for(let r=0;r<H;r++){ tryPush(r,0); tryPush(r,W-1); }
  while(q.length){
    const [r,c] = q.pop();
    for(const [dr,dc] of [[-1,0],[1,0],[0,-1],[0,1]]){
      const nr=r+dr, nc=c+dc;
      if(nr<0||nr>=H||nc<0||nc>=W) continue;
      if(inside[nr][nc]||seen[nr][nc]) continue;
      seen[nr][nc]=true; q.push([nr,nc]);
    }
  }
  for(let r=0;r<H;r++) for(let c=0;c<W;c++) if(!inside[r][c] && !seen[r][c]) return true;
  return false;
}

// Extracts the boundary as an ordered cyclic list of lattice points [r,c]
// (P x P point coordinates, P = W+1 = H+1) by walking the loop edges.
function extractBoundaryPath(inside, W, H){
  const P = W+1;
  const cellIn = (r,c) => (r>=0&&r<H&&c>=0&&c<W) ? inside[r][c] : false;
  // Build boundary edge set between lattice points.
  const edgeKey = (r1,c1,r2,c2) => (r1<r2||(r1===r2&&c1<c2)) ? `${r1},${c1}-${r2},${c2}` : `${r2},${c2}-${r1},${c1}`;
  const adj = new Map(); // point key -> [neighbor point keys]
  const pk = (r,c) => r*P+c;
  function addEdge(r1,c1,r2,c2){
    const a=pk(r1,c1), b=pk(r2,c2);
    if(!adj.has(a)) adj.set(a,[]);
    if(!adj.has(b)) adj.set(b,[]);
    adj.get(a).push(b); adj.get(b).push(a);
  }
  for(let r=0;r<H;r++){
    for(let c=0;c<W;c++){
      if(!inside[r][c]) continue;
      if(!cellIn(r-1,c)) addEdge(r,c, r,c+1);       // top side of cell (r,c)
      if(!cellIn(r+1,c)) addEdge(r+1,c, r+1,c+1);   // bottom side
      if(!cellIn(r,c-1)) addEdge(r,c, r+1,c);       // left side
      if(!cellIn(r,c+1)) addEdge(r,c+1, r+1,c+1);   // right side
    }
  }
  if(adj.size===0) return null;
  // Walk the cycle starting from any point; every point must have degree 2.
  for(const [,nbrs] of adj) if(nbrs.length!==2) return null;
  const start = adj.keys().next().value;
  const path = [start];
  let prev = -1, cur = start;
  while(true){
    const nbrs = adj.get(cur);
    const next = nbrs[0]===prev ? nbrs[1] : nbrs[0];
    if(next===start) break;
    path.push(next);
    prev = cur; cur = next;
  }
  if(path.length !== adj.size) return null; // sanity: should equal total boundary points (single cycle)
  return path.map(k => [ (k/P)|0, k%P ]);
}

function growRegionLoop(P, targetFrac, attempts){
  const W = P-1, H = P-1;
  attempts = attempts || 30;
  for(let a=0;a<attempts;a++){
    const inside = tryGrowBlob(W, H, Math.max(3, Math.round(W*H*targetFrac)));
    if(!inside) continue;
    if(hasHoleOrTouchesFrame(inside, W, H)) continue;
    const path = extractBoundaryPath(inside, W, H);
    if(!path || path.length < Math.max(8, P)) continue;
    return path;
  }
  return null;
}

/* ================= Loop analysis -> pearl candidate derivation ================= */
function analyzeLoop(P, path){
  const L = path.length;
  const straight = new Array(L);
  const dirOf = (a,b) => (b[0]===a[0]) ? (b[1]>a[1]?'R':'L') : (b[0]>a[0]?'D':'U');
  for(let i=0;i<L;i++){
    const prev = path[(i-1+L)%L], cur = path[i], next = path[(i+1)%L];
    const din = dirOf(prev,cur), dout = dirOf(cur,next);
    straight[i] = (din===dout);
  }
  return straight;
}

function deriveCandidates(P, path){
  const L = path.length;
  const straight = analyzeLoop(P, path);
  const whites = [], blacks = [];
  for(let i=0;i<L;i++){
    const prevS = straight[(i-1+L)%L], nextS = straight[(i+1)%L];
    if(straight[i]){
      if(!prevS || !nextS) whites.push(path[i]);
    } else {
      if(prevS && nextS) blacks.push(path[i]);
    }
  }
  return { whites, blacks };
}

/* ================= CSP solver =================
   Decides edges in strict point-major order (r,c) row by row; for point
   (r,c) the "left" and "up" edges are always already decided by the time
   we reach it (they were the "right"/"down" edges of earlier points), so
   each point only ever branches on its own right/down edges -- giving a
   branching factor of at most 2. Degree (0/2) and each clue's own
   straight/turn requirement are checked immediately at every point;
   single-loop-ness is tracked via a DSU that counts closed cycles (must
   equal exactly 1 for a legal Masyu loop); white/black "neighbor must
   (not) be straight" conditions are checked once per full assignment
   (cheap, only O(#clues), so deferring them to the leaf is fine). */
function countSolutions(P, clueGrid, limit, nodeBudget){
  nodeBudget = nodeBudget || 300000;
  const total = P*P;
  const Hedge = Array.from({length:P}, () => new Int8Array(Math.max(P-1,0)));
  const Vedge = Array.from({length:Math.max(P-1,0)}, () => new Int8Array(P));
  const dsu = new DSU(total);
  const idx = (r,c) => r*P+c;

  let loopClosedCount = 0;
  let nodes = 0, solutions = 0, aborted = false;
  let firstSolutionEdges = null;

  function straightOfPoint(r,c){
    const l = c>0 ? Hedge[r][c-1] : 0;
    const u = r>0 ? Vedge[r-1][c] : 0;
    const rr = c<P-1 ? Hedge[r][c] : 0;
    const d = r<P-1 ? Vedge[r][c] : 0;
    return (l && rr) || (u && d);
  }

  function verifyDeferred(){
    for(let r=0;r<P;r++){
      for(let c=0;c<P;c++){
        const clue = clueGrid[r][c];
        if(!clue) continue;
        const l = c>0 ? Hedge[r][c-1] : 0;
        const u = r>0 ? Vedge[r-1][c] : 0;
        const rr = c<P-1 ? Hedge[r][c] : 0;
        const d = r<P-1 ? Vedge[r][c] : 0;
        const nbrs = [];
        if(l) nbrs.push([r,c-1]);
        if(u) nbrs.push([r-1,c]);
        if(rr) nbrs.push([r,c+1]);
        if(d) nbrs.push([r+1,c]);
        if(nbrs.length !== 2) return false; // shouldn't happen: clue forces degree2
        const s1 = straightOfPoint(nbrs[0][0], nbrs[0][1]);
        const s2 = straightOfPoint(nbrs[1][0], nbrs[1][1]);
        if(clue===1){ if(s1 && s2) return false; }        // white needs >=1 turning neighbor
        else { if(!s1 || !s2) return false; }              // black needs both neighbors straight
      }
    }
    return true;
  }

  function snapshot(){
    const h = Hedge.map(row=>Array.from(row));
    const v = Vedge.map(row=>Array.from(row));
    return { h, v };
  }

  function dfs(i){
    if(solutions>=limit || aborted) return;
    if(i===total){
      if(loopClosedCount===1 && verifyDeferred()){
        solutions++;
        if(!firstSolutionEdges) firstSolutionEdges = snapshot();
      }
      return;
    }
    nodes++;
    if(nodes>nodeBudget){ aborted=true; return; }
    const r = (i/P)|0, c = i%P;
    const leftVal = c>0 ? Hedge[r][c-1] : 0;
    const upVal = r>0 ? Vedge[r-1][c] : 0;
    const rightExists = c<P-1, downExists = r<P-1;
    const clue = clueGrid[r][c];
    const rOpts = rightExists ? [0,1] : [0];
    const dOpts = downExists ? [0,1] : [0];
    for(const rv of rOpts){
      for(const dv of dOpts){
        const degree = leftVal+upVal+rv+dv;
        if(degree!==0 && degree!==2) continue;
        if(degree===2){
          const isStraight = (leftVal && rv) || (upVal && dv);
          if(clue===1 && !isStraight) continue;
          if(clue===2 && isStraight) continue;
        } else if(clue) continue; // clue point must have degree 2
        if(rightExists) Hedge[r][c] = rv;
        if(downExists) Vedge[r][c] = dv;
        let closedNow = 0, u1 = false, u2 = false;
        if(rv===1){ u1 = true; if(!dsu.union(idx(r,c), idx(r,c+1))) closedNow++; }
        if(dv===1){ u2 = true; if(!dsu.union(idx(r,c), idx(r+1,c))) closedNow++; }
        if(loopClosedCount+closedNow <= 1){
          loopClosedCount += closedNow;
          dfs(i+1);
          loopClosedCount -= closedNow;
        }
        if(u2) dsu.undo();
        if(u1) dsu.undo();
        if(rightExists) Hedge[r][c] = 0;
        if(downExists) Vedge[r][c] = 0;
        if(solutions>=limit || aborted) return;
      }
    }
  }

  dfs(0);
  return { count: aborted ? -1 : solutions, nodes, solutionEdges: firstSolutionEdges };
}

/* ================= Puzzle generation (generate-then-derive) ================= */
function makeClueGrid(P, whites, blacks){
  const grid = Array.from({length:P}, () => new Array(P).fill(0));
  for(const [r,c] of whites) grid[r][c] = 1;
  for(const [r,c] of blacks) grid[r][c] = 2;
  return grid;
}

function generatePuzzle(P, opts){
  opts = opts || {};
  const areaFrac = opts.areaFrac != null ? opts.areaFrac : 0.55;
  const reduceFraction = opts.reduceFraction != null ? opts.reduceFraction : 0.7; // portion of candidates attempted for removal
  const solveBudget = opts.solveBudget || 250000;
  const pruneBudget = opts.pruneBudget || 120000;
  const maxOuterAttempts = opts.maxOuterAttempts || 30;
  const reduceNodeBudgetTotal = opts.reduceNodeBudgetTotal || 1500000;

  for(let attempt=0; attempt<maxOuterAttempts; attempt++){
    const path = growRegionLoop(P, areaFrac, 30);
    if(!path) continue;
    const { whites, blacks } = deriveCandidates(P, path);
    const minClues = Math.max(4, Math.floor(P*0.7));
    if(whites.length + blacks.length < minClues) continue;

    let clueGrid = makeClueGrid(P, whites, blacks);
    const baseline = countSolutions(P, clueGrid, 2, solveBudget);
    if(baseline.count !== 1) continue; // not unique with full candidate set (or budget exceeded) -> retry

    // Simplification / reduction phase: try to drop clues while staying unique,
    // bounded by both a per-candidate list fraction and a cumulative node budget.
    let allCandidates = shuffle(whites.map(p=>({p, type:1})).concat(blacks.map(p=>({p, type:2}))));
    const attemptCount = Math.round(allCandidates.length * reduceFraction);
    let usedNodes = 0;
    let keptWhites = whites.slice(), keptBlacks = blacks.slice();
    for(let k=0; k<attemptCount && k<allCandidates.length; k++){
      if(usedNodes > reduceNodeBudgetTotal) break;
      const cand = allCandidates[k];
      const trialWhites = cand.type===1 ? keptWhites.filter(p=>p!==cand.p) : keptWhites;
      const trialBlacks = cand.type===2 ? keptBlacks.filter(p=>p!==cand.p) : keptBlacks;
      const trialGrid = makeClueGrid(P, trialWhites, trialBlacks);
      const res = countSolutions(P, trialGrid, 2, pruneBudget);
      usedNodes += res.nodes;
      if(res.count === 1){ keptWhites = trialWhites; keptBlacks = trialBlacks; }
      // res.count===0 impossible (removing a clue can't invalidate the existing solution);
      // res.count===2 (non-unique) or -1 (budget) => keep the clue, don't remove.
    }
    return { P, whites: keptWhites, blacks: keptBlacks, loopPath: path, candidateCount: allCandidates.length };
  }
  return null;
}

if(typeof module !== 'undefined'){
  module.exports = { DSU, growRegionLoop, deriveCandidates, analyzeLoop, countSolutions, generatePuzzle, makeClueGrid, causesPinch: causesPinch, hasHoleOrTouchesFrame };
}
