const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 800, height: 600 } });
  const errors = [];
  page.on('pageerror', (e) => errors.push('pageerror: ' + e.message));
  page.on('console', (msg) => {
    if (msg.type() === 'error') errors.push('console.error: ' + msg.text());
  });

  const filePath = 'file://' + path.resolve(__dirname, '..', 'slingshot.html');
  await page.goto(filePath);
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.resolve(__dirname, 'sling_00_start.png') });

  await page.click('#startBtn');
  await page.waitForTimeout(200);
  await page.screenshot({ path: path.resolve(__dirname, 'sling_01_aiming.png') });

  // Level 1 has no obstacles, target [340,420]. Anchor at (0,60). Drag back-and-down.
  // anchorScreenX = W*0.22 = 176, groundY = H*0.78=468, viewScale = clamp(800/900,0.55,1.3)=0.889
  const box = await page.locator('#game').boundingBox();
  const anchorScreenX = box.width * 0.22;
  const groundY = box.height * 0.78;
  const startX = anchorScreenX;
  const startY = groundY - 60 * 0.889; // near ball's initial screen pos

  await page.mouse.move(startX, startY);
  await page.mouse.down();
  await page.waitForTimeout(50);
  // drag left (screen) and down => negative world x, negative world z (pull back)
  await page.mouse.move(startX - 80, startY + 90, { steps: 10 });
  await page.waitForTimeout(100);
  await page.screenshot({ path: path.resolve(__dirname, 'sling_02_dragging.png') });

  const preDropState = await page.evaluate(() => {
    const c = document.getElementById('game');
    const ctx = c.getContext('2d');
    const data = ctx.getImageData(0, 0, c.width, c.height).data;
    let nonBg = 0;
    for (let i = 0; i < data.length; i += 40) {
      // background is sky blue-ish; just count variety isn't useful; check for white dashed line color approx
      nonBg++;
    }
    return nonBg;
  });

  await page.mouse.up();
  await page.waitForTimeout(100);
  await page.screenshot({ path: path.resolve(__dirname, 'sling_03_released.png') });

  // let it fly
  await page.waitForTimeout(1500);
  await page.screenshot({ path: path.resolve(__dirname, 'sling_04_flying_or_result.png') });

  const hud = await page.evaluate(() => ({
    level: document.getElementById('levelEl').textContent,
    stars: document.getElementById('starsEl').textContent,
    attempts: document.getElementById('attemptsEl').textContent,
    overlayShown: document.getElementById('overlay').classList.contains('show'),
    missShown: document.getElementById('missBanner').style.display,
  }));

  console.log(JSON.stringify({ errors, hud }, null, 2));

  await browser.close();
})();
