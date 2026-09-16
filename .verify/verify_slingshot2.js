const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 800, height: 600 } });
  const errors = [];
  page.on('pageerror', (e) => errors.push('pageerror: ' + e.message));
  page.on('console', (msg) => { if (msg.type() === 'error') errors.push('console.error: ' + msg.text()); });

  const filePath = 'file://' + path.resolve(__dirname, '..', 'slingshot.html');
  await page.goto(filePath);
  await page.click('#startBtn');
  await page.waitForTimeout(200);

  const box = await page.locator('#game').boundingBox();
  const anchorScreenX = box.width * 0.22;
  const groundY = box.height * 0.78;
  const s = Math.min(Math.max(box.width / 900, 0.55), 1.3);
  const startX = anchorScreenX;
  const startY = groundY - 60 * s;

  await page.mouse.move(startX, startY);
  await page.mouse.down();
  await page.mouse.move(startX - 56.5, startY + 56.5, { steps: 10 });
  await page.waitForTimeout(100);
  await page.mouse.up();
  await page.waitForTimeout(1500);
  await page.screenshot({ path: path.resolve(__dirname, 'sling_05_targeted_result.png') });

  const hud = await page.evaluate(() => ({
    level: document.getElementById('levelEl').textContent,
    stars: document.getElementById('starsEl').textContent,
    attempts: document.getElementById('attemptsEl').textContent,
    overlayShown: document.getElementById('overlay').classList.contains('show'),
    resultTitle: document.getElementById('resultTitle').textContent,
    starsRow: document.getElementById('starsRow').textContent,
  }));
  console.log(JSON.stringify({ errors, hud }, null, 2));
  await browser.close();
})();
