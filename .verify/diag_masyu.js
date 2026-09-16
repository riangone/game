"use strict";
const eng = require('./masyu_engine.js');

function diagOnce(P, areaFrac){
  const path = eng.growRegionLoop(P, areaFrac, 30);
  if(!path) return { stage: 'no-loop' };
  const { whites, blacks } = eng.deriveCandidates(P, path);
  const total = whites.length + blacks.length;
  const minClues = Math.max(4, Math.floor(P*0.7));
  if(total < minClues) return { stage: 'too-few-candidates', total, minClues, loopLen: path.length };
  const clueGrid = eng.makeClueGrid(P, whites, blacks);
  const res = eng.countSolutions(P, clueGrid, 2, 250000);
  return { stage: 'solved', count: res.count, nodes: res.nodes, total, loopLen: path.length };
}

for(const P of [5,7,9]){
  const tally = {};
  const samples = [];
  for(let i=0;i<40;i++){
    const d = diagOnce(P, 0.55);
    tally[d.stage] = (tally[d.stage]||0)+1;
    if(samples.length<5) samples.push(d);
  }
  console.log(`P=${P}:`, tally);
  console.log('  samples:', JSON.stringify(samples));
}
