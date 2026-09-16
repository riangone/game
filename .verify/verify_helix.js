const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 400, height: 800 } });
  const errors = [];

  page.on('pageerror', (e) => errors.push('pageerror: ' + e.message));
  page.on('console', (msg) => {
    if (msg.type() === 'error') errors.push('console.error: ' + msg.text());
  });

  const filePath = 'file://' + path.resolve(__dirname, '..', 'helix.html');
  await page.goto(filePath);
  await page.waitForTimeout(250);

  const startToggles = await page.evaluate(() => ({
    guide: document.getElementById('startGuideToggle').checked,
    sound: document.getElementById('startSoundToggle').checked
  }));
  console.log('Start toggles:', startToggles);
  if (!startToggles.guide || !startToggles.sound) throw new Error('default toggles off');

  await page.screenshot({ path: path.resolve(__dirname, 'helix_00_start.png') });

  await page.click('#startBtn');
  await page.waitForTimeout(150);
  let st = await page.evaluate(() => window.__hx.getState());
  console.log('State after start:', st);
  if (st.state !== 'playing') throw new Error('did not enter playing');

  await page.screenshot({ path: path.resolve(__dirname, 'helix_01_playing.png') });

  await page.waitForTimeout(900);
  st = await page.evaluate(() => window.__hx.getState());
  console.log('After first descent:', st);
  if (st.score < 1) throw new Error('expected >=1 plane passed after start descent, got ' + st.score);

  console.log('Rings info:', await page.evaluate(() => window.__hx.ringsInfo()));

  console.log('Enabling autoplay, waiting to climb to score>=15...');
  await page.evaluate(() => window.__hx.auto(true));
  await page.waitForFunction(() => window.__hx.getState().score >= 15, null, { timeout: 30000 });
  st = await page.evaluate(() => window.__hx.getState());
  console.log('Autoplay reached:', st);
  if (st.state !== 'playing') throw new Error('died during autoplay, state=' + st.state);

  await page.screenshot({ path: path.resolve(__dirname, 'helix_02_midplay.png') });

  console.log('Real pointer rotation test...');
  const box = await page.locator('#game').boundingBox();
  await page.evaluate(() => window.__hx.auto(false));
  const before = await page.evaluate(() => window.__hx.getState().tower);
  await page.mouse.move(box.x + box.width - 25, box.y + box.height * 0.5);
  await page.mouse.down();
  await page.waitForTimeout(280);
  const held = await page.evaluate(() => window.__hx.getState());
  await page.mouse.up();
  await page.waitForTimeout(120);
  const released = await page.evaluate(() => window.__hx.getState());
  const deltaR = Math.abs(held.tower - before);
  const stableDelta = Math.abs(released.tower - held.tower);
  console.log('rotation delta while held:', deltaR.toFixed(3), 'rotDir during:', held.rotDir, 'drift after release:', stableDelta.toFixed(3));
  if (deltaR < 0.3) throw new Error('pointer hold did not rotate tower');
  if (held.rotDir !== 1) throw new Error('expected rotDir 1 for right-half hold, got ' + held.rotDir);
  if (released.rotDir !== 0) throw new Error('rotDir should reset to 0 on release');
  if (stableDelta > 0.01) throw new Error('tower keeps moving after release');

  console.log('Left-half hold check...');
  const beforeL = await page.evaluate(() => window.__hx.getState().tower);
  await page.mouse.move(box.x + 25, box.y + box.height * 0.5);
  await page.mouse.down();
  await page.waitForTimeout(250);
  const heldL = await page.evaluate(() => window.__hx.getState());
  await page.mouse.up();
  const deltaL = Math.abs(heldL.tower - beforeL);
  console.log('left rotation delta:', deltaL.toFixed(3), 'rotDir:', heldL.rotDir);
  if (deltaL < 0.3) throw new Error('left hold did not rotate');
  if (heldL.rotDir !== -1) throw new Error('expected rotDir -1 for left-half hold, got ' + heldL.rotDir);

  await page.screenshot({ path: path.resolve(__dirname, 'helix_03_rotating.png') });

  console.log('Forcing red-sector death...');
  const redSid = await page.evaluate(() => window.__hx.seekRed());
  console.log('seeded red sector index:', redSid);
  if (redSid == null || redSid < 0) throw new Error('no red sector found to seed death');
  await page.waitForFunction(() => window.__hx.getState().state === 'dead' || window.__hx.getState().state === 'over', null, { timeout: 5000 });
  await page.waitForTimeout(750);
  const deadState = await page.evaluate(() => window.__hx.getState());
  const overlayVisible = await page.evaluate(() => document.getElementById('overlay').classList.contains('show'));
  console.log('dead state:', deadState, 'overlay shown:', overlayVisible);
  if (!overlayVisible) throw new Error('game over overlay did not appear');
  if (deadState.state !== 'over') throw new Error('expected over state');
  if (deadState.best < deadState.score) throw new Error('best score not persisted');

  await page.screenshot({ path: path.resolve(__dirname, 'helix_04_gameover.png') });

  console.log('Restart test...');
  await page.click('#restartBtn');
  await page.waitForTimeout(200);
  const rs = await page.evaluate(() => window.__hx.getState());
  console.log('restarted state:', rs);
  if (rs.state !== 'playing') throw new Error('restart did not resume game');
  if (rs.score !== 0) throw new Error('score not reset');

  await page.screenshot({ path: path.resolve(__dirname, 'helix_05_restart.png') });

  console.log('Verification finished. Captured errors:');
  console.log(errors.length ? errors : 'NONE');
  if (errors.length) process.exitCode = 1;
  await browser.close();
})();