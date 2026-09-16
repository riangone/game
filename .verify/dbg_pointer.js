const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 400, height: 800 } });
  page.on('console', m => { if (m.type()==='error') console.log('CE', m.text()); });
  const filePath = 'file://' + path.resolve('/home/ubuntu/ws/jump-jump-game', 'helix.html');
  await page.goto(filePath);
  await page.waitForTimeout(200);
  await page.click('#startBtn');
  await page.waitForTimeout(600);
  await page.evaluate(() => {
    window.__evt = [];
    window.addEventListener('pointerdown', e => window.__evt.push('pd'+e.pointerId+':'+Math.round(e.clientX)));
    window.addEventListener('pointerup', e => window.__evt.push('pu'+e.pointerId));
    window.addEventListener('mousedown', () => window.__evt.push('md'));
  });
  const box = await page.locator('#game').boundingBox();
  await page.mouse.move(box.x + box.width - 25, box.y + box.height * 0.5);
  await page.mouse.down();
  await page.waitForTimeout(280);
  const h = await page.evaluate(() => ({evt: window.__evt, st: window.__hx.getState()}));
  await page.mouse.up();
  console.log('events:', JSON.stringify(h.evt));
  console.log('state:', JSON.stringify(h.st));
  await browser.close();
})();
