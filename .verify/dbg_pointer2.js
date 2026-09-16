const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 400, height: 800 } });
  page.on('console', m => { if (m.type() === 'error') console.log('CE', m.text()); });
  const filePath = 'file://' + path.resolve('/home/ubuntu/ws/jump-jump-game', 'helix.html');
  await page.goto(filePath);
  await page.waitForTimeout(250);
  await page.click('#startBtn');
  await page.evaluate(() => window.__hx.auto(true));
  await page.waitForFunction(() => window.__hx.getState().score >= 15, null, { timeout: 30000 });
  console.log('pre-hold state:', JSON.stringify(await page.evaluate(() => window.__hx.getState())));
  await page.evaluate(() => window.__hx.auto(false));
  const before = await page.evaluate(() => window.__hx.getState().tower);
  const box = await page.locator('#game').boundingBox();
  console.log('box:', box);
  await page.evaluate(() => {
    window.__evt = [];
    window.addEventListener('pointerdown', e => window.__evt.push('pd' + e.pointerId + '@' + Math.round(e.clientX)));
    window.addEventListener('pointerup', e => window.__evt.push('pu' + e.pointerId));
    window.addEventListener('pointercancel', e => window.__evt.push('pc' + e.pointerId));
  });
  await page.mouse.move(box.x + box.width - 25, box.y + box.height * 0.5);
  await page.mouse.down();
  for (let i = 0; i < 5; i++) {
    await page.waitForTimeout(60);
    const s = await page.evaluate(() => window.__hx.getState());
    console.log(`sample ${i}: rotDir=${s.rotDir} tower=${s.tower.toFixed(3)} state=${s.state} phase=${s.phase} curPlane=${s.curPlane}`);
  }
  await page.mouse.up();
  await page.waitForTimeout(100);
  const fin = await page.evaluate(() => ({ evt: window.__evt, st: window.__hx.getState() }));
  console.log('events:', JSON.stringify(fin.evt));
  console.log('final:', JSON.stringify(fin.st));
  await browser.close();
})();