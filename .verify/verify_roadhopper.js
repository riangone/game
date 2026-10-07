const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 420, height: 800 } });
  const errors = [];
  page.on('console', (msg) => { if (msg.type() === 'error') errors.push(msg.text()); });
  page.on('pageerror', (err) => errors.push('pageerror: ' + err.message));

  const filePath = 'file://' + path.resolve(__dirname, '..', 'roadhopper.html');
  await page.goto(filePath);
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.resolve(__dirname, 'roadhopper_00_start.png') });

  await page.click('#startBtn');
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.resolve(__dirname, 'roadhopper_01_playing.png') });

  for (let i = 0; i < 20; i++) {
    await page.keyboard.press('ArrowUp');
    await page.waitForTimeout(170);
  }
  await page.screenshot({ path: path.resolve(__dirname, 'roadhopper_02_progress.png') });

  let died = false;
  for (let i = 0; i < 300 && !died; i++) {
    await page.keyboard.press('ArrowUp');
    await page.waitForTimeout(90);
    died = await page.evaluate(() => document.getElementById('overlay').classList.contains('show'));
  }
  await page.screenshot({ path: path.resolve(__dirname, 'roadhopper_03_gameover.png') });

  await page.click('#restartBtn');
  await page.waitForTimeout(250);
  await page.screenshot({ path: path.resolve(__dirname, 'roadhopper_04_restart.png') });

  console.log('died within budget:', died);
  console.log('console/page errors:', JSON.stringify(errors));
  if (errors.length) process.exitCode = 1;
  await browser.close();
})();
