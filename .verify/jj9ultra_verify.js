const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 420, height: 820 } });
  const consoleErrors = [];
  page.on('console', (msg) => {
    if (msg.type() === 'error') consoleErrors.push(msg.text());
  });
  page.on('pageerror', (err) => consoleErrors.push('pageerror: ' + err.message));

  const filePath = 'file://' + path.resolve(__dirname, '../jj9ultra.html');
  await page.goto(filePath);
  await page.waitForTimeout(300);

  await page.screenshot({ path: path.join(__dirname, 'jj9ultra_00_start.png') });

  // Start the game
  await page.click('#startBtn');
  await page.waitForTimeout(200);
  await page.screenshot({ path: path.join(__dirname, 'jj9ultra_01_ready.png') });

  const dbg = () => page.evaluate(() => window.__jj9UltraDebug);

  // Real pointer-driven charge, to confirm the aura rings + charge bar render from actual input
  const canvasBox = await page.locator('#game').boundingBox();
  await page.mouse.move(canvasBox.x + canvasBox.width / 2, canvasBox.y + canvasBox.height / 2);
  await page.mouse.down();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(__dirname, 'jj9ultra_02_charging_aura.png') });
  await page.mouse.up();
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(__dirname, 'jj9ultra_03_after_real_jump.png') });

  let state = await page.evaluate(() => window.__jj9UltraDebug.getState());
  console.log('state after real jump:', state);

  // Drive a streak of forced perfect center hits via the debug hook to reach combo milestones
  let lastCombo = 0;
  let milestoneShotTaken = false;
  for (let i = 0; i < 12; i++) {
    // wait until back in "ready" state (previous jump resolved)
    for (let tries = 0; tries < 40; tries++) {
      const s = await page.evaluate(() => window.__jj9UltraDebug.getState());
      if (s === 'ready') break;
      await page.waitForTimeout(50);
    }
    const ok = await page.evaluate(() => window.__jj9UltraDebug.forceCenterHit());
    if (!ok) { console.log('forceCenterHit failed at i=', i); break; }
    await page.waitForTimeout(180);
    const combo = await page.evaluate(() => window.__jj9UltraDebug.getCombo());
    const score = await page.evaluate(() => window.__jj9UltraDebug.getScore());
    console.log(`hit ${i}: combo=${combo} score=${score}`);
    lastCombo = combo;
    if (combo === 5 && !milestoneShotTaken) {
      await page.waitForTimeout(120); // let the banner animation get into frame
      await page.screenshot({ path: path.join(__dirname, 'jj9ultra_04_combo5_milestone.png') });
      milestoneShotTaken = true;
    }
  }
  console.log('final combo reached:', lastCombo);
  await page.screenshot({ path: path.join(__dirname, 'jj9ultra_05_after_streak.png') });

  const flashAlphaDuringStreak = await page.evaluate(() => window.__jj9UltraDebug.getFlashAlpha());
  console.log('flashAlpha sample (should decay towards 0 shortly after landing):', flashAlphaDuringStreak);

  // Now force a miss to confirm death path + flash still works + no errors, then check game over screen
  for (let tries = 0; tries < 40; tries++) {
    const s = await page.evaluate(() => window.__jj9UltraDebug.getState());
    if (s === 'ready') break;
    await page.waitForTimeout(50);
  }
  await page.evaluate(() => window.__jj9UltraDebug.forceMissHit());
  await page.waitForTimeout(1500);
  await page.screenshot({ path: path.join(__dirname, 'jj9ultra_06_gameover.png') });
  const finalState = await page.evaluate(() => window.__jj9UltraDebug.getState());
  console.log('state after miss:', finalState);

  // Restart flow sanity check
  await page.click('#restartBtn');
  await page.waitForTimeout(200);
  const stateAfterRestart = await page.evaluate(() => window.__jj9UltraDebug.getState());
  console.log('state after restart:', stateAfterRestart);
  await page.screenshot({ path: path.join(__dirname, 'jj9ultra_07_after_restart.png') });

  console.log('=== console/page errors:', consoleErrors.length);
  consoleErrors.forEach((e) => console.log('  ERR:', e));

  await browser.close();
  process.exit(consoleErrors.length > 0 ? 1 : 0);
})();
