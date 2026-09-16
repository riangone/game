"use strict";
/* ============================================================
   Masyu (pearl-loop) core engine: board model, generator, solver.
   Pure JS, no DOM — designed to be copy-pasted verbatim into
   masyu.html's <script> block, and independently load-testable
   under Node.
   ============================================================ */

function shuffle(arr){ for(let i=arr.length-1;i>0;i--){ const j=(Math.random()*(i+1))|0; const t=arr[i]; arr[i]=arr[j]; arr[j]=t; } return arr; }
function randInt(n){ return (Math.random()*n)|0; }

/* ---------------- Board model ---------------- */
function buildBoard(N){
  const numPoints = N*N;
  const idx=(r,c)=>r*N+c;
  const edges=[];
  const pointEdgeList = Array.from({length:numPoints},()=>[]);
  const pointEdgeDir = Array.from({length:numPoints},()=>({}));
  const hLookup = Array.from({length:N}, ()=>Array(N-1).fill(-1));
  const vLookup = Array.from({length:N-1}, ()=>Array(N).fill(-1));
  for(let r=0;r<N;r++){
    for(let c=0;c<N-1;c++){
      const id=edges.length;
      edges.push({p1:idx(r,c), p2:idx(r,c+1), horiz:true, r, c});
      pointEdgeList[idx(r,c)].push(id); pointEdgeDir[idx(r,c)][id]='R';
      pointEdgeList[idx(r,c+1)].push(id); pointEdgeDir[idx(r,c+1)][id]='L';
      hLookup[r][c]=id;
    }
  }
  for(let r=0;r<N-1;r++){
    for(let c=0;c<N;c++){
      const id=edges.length;
      edges.push({p1:idx(r,c), p2:idx(r+1,c), horiz:false, r, c});
      pointEdgeList[idx(r,c)].push(id); pointEdgeDir[idx(r,c)][id]='D';
      pointEdgeList[idx(r+1,c)].push(id); pointEdgeDir[idx(r+1,c)][id]='U';
      vLookup[r][c]=id;
    }
  }
  return { N, numPoints, edges, pointEdgeList, pointEdgeDir, hLookup, vLookup, idx };
}

/* ---------------- Random simply-connected region -> boundary loop ---------------- */
function causesPinch(inside,r,c,H,W){
  for(const [dr,dc] of [[-1,-1],[-1,1],[1,-1],[1,1]]){
    const rr=r+dr, cc=c+dc;
    if(rr<0||rr>=H||cc<0||cc>=W) continue;
    if(!inside[rr][cc]) continue;
    const b1r=r+dr, b1c=c;
    const b2r=r, b2c=c+dc;
    const b1in = (b1r>=0&&b1r<H&&b1c>=0&&b1c<W) ? inside[b1r][b1c] : false;
    const b2in = (b2r>=0&&b2r<H&&b2c>=0&&b2c<W) ? inside[b2r][b2c] : false;
    if(!b1in && !b2in) return true;
  }
  return false;
}

function tryGrow(W,H,target){
  const inside = Array.from({length:H},()=>Array(W).fill(false));
  const sr=randInt(H), sc=randInt(W);
  inside[sr][sc]=true;
  let count=1;
  const frontier=[];
  function addFrontierAround(r,c){
    for(const [dr,dc] of [[-1,0],[1,0],[0,-1],[0,1]]){
      const nr=r+dr,nc=c+dc;
      if(nr>=0&&nr<H&&nc>=0&&nc<W&&!inside[nr][nc]) frontier.push([nr,nc]);
    }
  }
  addFrontierAround(sr,sc);
  let guard=0;
  while(count<target && frontier.length>0 && guard++<target*40){
    const i=randInt(frontier.length);
    const [r,c]=frontier[i];
    frontier[i]=frontier[frontier.length-1]; frontier.pop();
    if(inside[r][c]) continue;
    if(causesPinch(inside,r,c,H,W)) continue;
    inside[r][c]=true; count++;
    addFrontierAround(r,c);
  }
  if(count < target*0.55) return null;
  return inside;
}

function hasHole(inside,W,H){
  const seen = Array.from({length:H},()=>Array(W).fill(false));
  const q=[];
  for(let c=0;c<W;c++){
    if(!inside[0][c]&&!seen[0][c]){seen[0][c]=true;q.push([0,c]);}
    if(!inside[H-1][c]&&!seen[H-1][c]){seen[H-1][c]=true;q.push([H-1,c]);}
  }
  for(let r=0;r<H;r++){
    if(!inside[r][0]&&!seen[r][0]){seen[r][0]=true;q.push([r,0]);}
    if(!inside[r][W-1]&&!seen[r][W-1]){seen[r][W-1]=true;q.push([r,W-1]);}
  }
  while(q.length){
    const [r,c]=q.pop();
    for(const [dr,dc] of [[-1,0],[1,0],[0,-1],[0,1]]){
      const nr=r+dr,nc=c+dc;
      if(nr<0||nr>=H||nc<0||nc>=W) continue;
      if(inside[nr][nc]||seen[nr][nc]) continue;
      seen[nr][nc]=true; q.push([nr,nc]);
    }
  }
  for(let r=0;r<H;r++) for(let c=0;c<W;c++) if(!inside[r][c] && !seen[r][c]) return true;
  return false;
}

function extractBoundary(inside,W,H){
  const list=[];
  const cellIn=(r,c)=> (r>=0&&r<H&&c>=0&&c<W) ? inside[r][c] : false;
  for(let r=0;r<H;r++){
    for(let c=0;c<W;c++){
      if(!inside[r][c]) continue;
      if(!cellIn(r-1,c)) list.push({isH:true, r:r, c:c});
      if(!cellIn(r+1,c)) list.push({isH:true, r:r+1, c:c});
      if(!cellIn(r,c-1)) list.push({isH:false, r:r, c:c});
      if(!cellIn(r,c+1)) list.push({isH:false, r:r, c:c+1});
    }
  }
  return list;
}

function growRegionLoop(N, targetFrac, attempts){
  const W=N-1, H=N-1;
  attempts = attempts||25;
  for(let a=0;a<attempts;a++){
    const inside = tryGrow(W,H, Math.max(3,Math.round(W*H*targetFrac)));
    if(!inside) continue;
    if(hasHole(inside,W,H)) continue;
    const list = extractBoundary(inside,W,H);
    if(list.length < Math.max(8,N)) continue;
    return list;
  }
  return null;
}

/* ---------------- Loop analysis -> pearl candidate derivation ---------------- */
function analyzeLoop(board, solutionSet){
  const deg = new Array(board.numPoints).fill(0);
  const dirIn = Array.from({length:board.numPoints}, ()=>[]);
  const neighborPt = Array.from({length:board.numPoints}, ()=>[]);
  for(const e of solutionSet){
    const edge = board.edges[e];
    deg[edge.p1]++; deg[edge.p2]++;
    dirIn[edge.p1].push(board.pointEdgeDir[edge.p1][e]);
    dirIn[edge.p2].push(board.pointEdgeDir[edge.p2][e]);
    neighborPt[edge.p1].push(edge.p2);
    neighborPt[edge.p2].push(edge.p1);
  }
  function isStraight(p){
    const d = dirIn[p];
    if(d.length!==2) return null;
    const s = new Set(d);
    return (s.has('L')&&s.has('R')) || (s.has('U')&&s.has('D'));
  }
  return { deg, dirIn, neighborPt, isStraight };
}

function deriveCandidates(board, solutionSet){
  const info = analyzeLoop(board, solutionSet);
  const candidates = [];
  for(let p=0;p<board.numPoints;p++){
    if(info.deg[p]!==2) continue;
    const straight = info.isStraight(p);
    const nb = info.neighborPt[p];
    const n1s = info.isStraight(nb[0]), n2s = info.isStraight(nb[1]);
    if(straight){
      if(n1s===false || n2s===false) candidates.push({p, type:'w'});
    } else {
      if(n1s===true && n2s===true) candidates.push({p, type:'b'});
    }
  }
  return candidates;
}

/* ---------------- Constraint-propagation + backtracking solver ---------------- */
function createSolver(board, pearlMap){
  const numEdges = board.edges.length;
  const numPoints = board.numPoints;
  const edgeState = new Int8Array(numEdges);
  const parent = new Int32Array(numPoints);
  const rnk = new Int32Array(numPoints);
  for(let i=0;i<numPoints;i++) parent[i]=i;
  function find(x){ while(parent[x]!==x) x=parent[x]; return x; }
  let loopClosed=false;
  const trailEdges=[]; const trailUnions=[];
  let aborted=false, nodeCount=0, nodeBudget=300000;
  let solutionCount=0;
  const solutions=[];

  function assignEdge(e,val){
    const cur=edgeState[e];
    if(cur===val) return true;
    if(cur!==0) return false;
    edgeState[e]=val;
    trailEdges.push(e);
    if(val===1){
      const edge=board.edges[e];
      const ru=find(edge.p1), rv=find(edge.p2);
      if(ru===rv){ loopClosed=true; }
      else {
        let a=ru,b=rv;
        if(rnk[a]<rnk[b]){ const t=a;a=b;b=t; }
        parent[b]=a;
        let bumped=false;
        if(rnk[a]===rnk[b]){ rnk[a]++; bumped=true; }
        trailUnions.push({child:b, parentNode:a, bumped});
      }
    }
    return true;
  }
  function undoTo(markE,markU,markClosed){
    while(trailEdges.length>markE){ const e=trailEdges.pop(); edgeState[e]=0; }
    while(trailUnions.length>markU){ const u=trailUnions.pop(); parent[u.child]=u.child; if(u.bumped) rnk[u.parentNode]--; }
    loopClosed=markClosed;
  }

  function dirsOf(p){
    const edges=board.pointEdgeList[p]; const dir=board.pointEdgeDir[p];
    let up=-1,down=-1,left=-1,right=-1;
    for(const e of edges){ const d=dir[e]; if(d==='U')up=e; else if(d==='D')down=e; else if(d==='L')left=e; else right=e; }
    return {up,down,left,right};
  }

  function enforceWhite(p){
    const {up,down,left,right} = dirsOf(p);
    const st=e=> e<0? null : edgeState[e];
    if((left>=0&&st(left)===1)||(right>=0&&st(right)===1)){
      if(left<0||right<0) return false;
      if(!assignEdge(left,1)) return false;
      if(!assignEdge(right,1)) return false;
      if(up>=0 && !assignEdge(up,-1)) return false;
      if(down>=0 && !assignEdge(down,-1)) return false;
    }
    if((up>=0&&st(up)===1)||(down>=0&&st(down)===1)){
      if(up<0||down<0) return false;
      if(!assignEdge(up,1)) return false;
      if(!assignEdge(down,1)) return false;
      if(left>=0 && !assignEdge(left,-1)) return false;
      if(right>=0 && !assignEdge(right,-1)) return false;
    }
    const hBlocked = left<0||right<0|| st(left)===-1||st(right)===-1;
    const vBlocked = up<0||down<0|| st(up)===-1||st(down)===-1;
    if(hBlocked){
      if(up<0||down<0) return false;
      if(st(up)!==1 && !assignEdge(up,1)) return false;
      if(st(down)!==1 && !assignEdge(down,1)) return false;
      if(left>=0 && st(left)!==-1 && !assignEdge(left,-1)) return false;
      if(right>=0 && st(right)!==-1 && !assignEdge(right,-1)) return false;
    }
    if(vBlocked){
      if(left<0||right<0) return false;
      if(st(left)!==1 && !assignEdge(left,1)) return false;
      if(st(right)!==1 && !assignEdge(right,1)) return false;
      if(up>=0 && st(up)!==-1 && !assignEdge(up,-1)) return false;
      if(down>=0 && st(down)!==-1 && !assignEdge(down,-1)) return false;
    }
    return true;
  }

  function enforceBlack(p){
    const {up,down,left,right} = dirsOf(p);
    const hArr=[left,right].filter(e=>e>=0);
    const vArr=[up,down].filter(e=>e>=0);
    if(hArr.length===0||vArr.length===0) return false;
    const hIn=hArr.filter(e=>edgeState[e]===1), hUnk=hArr.filter(e=>edgeState[e]===0);
    const vIn=vArr.filter(e=>edgeState[e]===1), vUnk=vArr.filter(e=>edgeState[e]===0);
    if(hIn.length>1||vIn.length>1) return false;
    if(hIn.length===1){ for(const e of hUnk) if(!assignEdge(e,-1)) return false; }
    else if(hIn.length===0){
      if(hUnk.length===0) return false;
      if(hUnk.length===1 && !assignEdge(hUnk[0],1)) return false;
    }
    if(vIn.length===1){ for(const e of vUnk) if(!assignEdge(e,-1)) return false; }
    else if(vIn.length===0){
      if(vUnk.length===0) return false;
      if(vUnk.length===1 && !assignEdge(vUnk[0],1)) return false;
    }
    return true;
  }

  const whiteList=[], blackList=[];
  for(const [p,t] of pearlMap) (t==='w'?whiteList:blackList).push(p);

  function propagate(){
    let guard=0;
    while(true){
      guard++;
      if(guard>2000) return true;
      const before = trailEdges.length;
      if(loopClosed){
        for(let e=0;e<numEdges;e++){
          if(edgeState[e]===0){ if(!assignEdge(e,-1)) return false; }
        }
      }
      for(let p=0;p<numPoints;p++){
        const edges=board.pointEdgeList[p];
        let cin=0; const unk=[];
        for(const e of edges){ if(edgeState[e]===1) cin++; else if(edgeState[e]===0) unk.push(e); }
        if(cin>2) return false;
        if(pearlMap.has(p)){
          if(cin+unk.length<2) return false;
          if(cin===2){ for(const e of unk) if(!assignEdge(e,-1)) return false; }
          else if(cin+unk.length===2){ for(const e of unk) if(!assignEdge(e,1)) return false; }
        } else {
          if(cin===1){
            if(unk.length===0) return false;
            if(unk.length===1 && !assignEdge(unk[0],1)) return false;
          } else if(cin===0){
            if(unk.length===1 && !assignEdge(unk[0],-1)) return false;
          } else if(cin===2){
            for(const e of unk) if(!assignEdge(e,-1)) return false;
          }
        }
      }
      for(const p of whiteList) if(!enforceWhite(p)) return false;
      for(const p of blackList) if(!enforceBlack(p)) return false;
      if(trailEdges.length===before) return true;
    }
  }

  function isStraightFinal(p){
    const edges=board.pointEdgeList[p]; const dir=board.pointEdgeDir[p];
    const ds=[];
    for(const e of edges) if(edgeState[e]===1) ds.push(dir[e]);
    if(ds.length!==2) return false;
    const s=new Set(ds);
    return (s.has('L')&&s.has('R'))||(s.has('U')&&s.has('D'));
  }
  function neighborsOf(p){
    const edges=board.pointEdgeList[p];
    const res=[];
    for(const e of edges) if(edgeState[e]===1){ const edge=board.edges[e]; res.push(edge.p1===p?edge.p2:edge.p1); }
    return res;
  }
  function validateFullSolution(){
    for(const p of whiteList){
      if(!isStraightFinal(p)) return false;
      const nb=neighborsOf(p);
      if(nb.length!==2) return false;
      if(isStraightFinal(nb[0]) && isStraightFinal(nb[1])) return false;
    }
    for(const p of blackList){
      if(isStraightFinal(p)) return false;
      const nb=neighborsOf(p);
      if(nb.length!==2) return false;
      if(!isStraightFinal(nb[0]) || !isStraightFinal(nb[1])) return false;
    }
    return true;
  }

  function chooseBranchEdge(){
    for(const p of pearlMap.keys()){
      for(const e of board.pointEdgeList[p]) if(edgeState[e]===0) return e;
    }
    for(let e=0;e<numEdges;e++) if(edgeState[e]===0) return e;
    return -1;
  }

  function search(limit){
    if(aborted) return;
    nodeCount++;
    if(nodeCount>nodeBudget){ aborted=true; return; }
    if(!propagate()) return;
    if(loopClosed){
      if(validateFullSolution()){
        solutionCount++;
        if(solutions.length<1) solutions.push(edgeState.slice());
      }
      return;
    }
    const e=chooseBranchEdge();
    if(e===-1) return;
    const order = Math.random()<0.5?[1,-1]:[-1,1];
    for(const val of order){
      const markE=trailEdges.length, markU=trailUnions.length, markClosed=loopClosed;
      if(assignEdge(e,val)) search(limit);
      undoTo(markE,markU,markClosed);
      if(solutionCount>=limit || aborted) return;
    }
  }

  function countSolutions(limit, budget){
    nodeBudget = budget||300000;
    nodeCount=0; aborted=false; solutionCount=0; solutions.length=0;
    search(limit);
    return aborted ? -1 : solutionCount;
  }
  return { countSolutions, getFirstSolution:()=>solutions[0]||null, get nodeCount(){return nodeCount;} };
}

/* ---------------- Full puzzle generator ---------------- */
function generatePuzzle(N, opts){
  opts = opts||{};
  const areaFrac = opts.areaFrac || 0.55;
  const keepFrac = opts.keepFrac != null ? opts.keepFrac : 0.75;
  const solveBudget = opts.solveBudget || 220000;
  const pruneBudget = opts.pruneBudget || 60000;
  const maxOuterAttempts = opts.maxOuterAttempts || 25;
  const board = buildBoard(N);
  let fallback = null;
  for(let attempt=0; attempt<maxOuterAttempts; attempt++){
    const descs = growRegionLoop(N, areaFrac, 25);
    if(!descs) continue;
    const solutionSet = new Set();
    let bad=false;
    for(const d of descs){
      const id = d.isH ? board.hLookup[d.r][d.c] : board.vLookup[d.r][d.c];
      if(id==null||id<0){ bad=true; break; }
      solutionSet.add(id);
    }
    if(bad) continue;
    const candidates = deriveCandidates(board, solutionSet);
    if(candidates.length < Math.max(4, Math.floor(N*0.8))) continue;
    const pearlMap = new Map(candidates.map(c=>[c.p,c.type]));
    const solver = createSolver(board, pearlMap);
    const cnt = solver.countSolutions(2, solveBudget);
    if(cnt!==1){
      if(cnt===1 && !fallback) fallback = { N, pearls:new Map(pearlMap), solutionEdges:solutionSet, board };
      continue;
    }
    if(!fallback) fallback = { N, pearls:new Map(pearlMap), solutionEdges:solutionSet, board };
    const targetCount = Math.max(4, Math.round(candidates.length*keepFrac));
    const order = shuffle(candidates.slice());
    let current = new Map(pearlMap);
    let calls = Math.min(order.length, 260);
    for(const cand of order){
      if(current.size<=targetCount) break;
      if(calls-- <=0) break;
      const trial = new Map(current);
      trial.delete(cand.p);
      const s2 = createSolver(board, trial);
      const c2 = s2.countSolutions(2, pruneBudget);
      if(c2===1){ current = trial; }
    }
    return { N, pearls: current, solutionEdges: solutionSet, board, candidateCount: candidates.length };
  }
  return fallback;
}

module.exports = {
  buildBoard, growRegionLoop, deriveCandidates, analyzeLoop, createSolver, generatePuzzle,
  causesPinch, hasHole, extractBoundary, tryGrow
};
