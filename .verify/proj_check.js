const ISO_A = Math.PI / 8;
const CAM_ANCHOR_X_RATIO = 0.5;
const CAM_ANCHOR_Y_RATIO = 0.64;

function makeProject(W, H, camScale, cameraOffset) {
  return function project(x, y, z) {
    const rx = x - cameraOffset.x;
    const ry = y - cameraOffset.y;
    const rz = z - cameraOffset.z;
    const sx = (rx - ry) * Math.cos(ISO_A);
    const sy = -(rx + ry) * Math.sin(ISO_A) - rz;
    return { x: W * CAM_ANCHOR_X_RATIO + sx * camScale, y: H * CAM_ANCHOR_Y_RATIO + sy * camScale };
  };
}

const LANE_X = [-90, 0, 90];
const ROW_GAP = 110;

for (const W of [320, 768, 1280, 1920]) {
  const H = Math.round(W * 0.6);
  const camScale = 1.0;
  const playerHeight = 660; // simulate player 6 rows up
  const cameraOffset = { x: 0, y: 0, z: playerHeight - 150 };
  const project = makeProject(W, H, camScale, cameraOffset);

  console.log(`\n=== W=${W} H=${H} ===`);
  for (let row = 0; row <= 8; row++) {
    const z = row * ROW_GAP;
    const pts = LANE_X.map((lx) => project(lx, 0, z));
    console.log(
      `row ${row} (z=${z}): ` +
      pts.map((p, i) => `lane${i}=(${p.x.toFixed(0)},${p.y.toFixed(0)})`).join('  ')
    );
  }
}
