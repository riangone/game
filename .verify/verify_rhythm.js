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

  const filePath = 'file://' + path.resolve(__dirname, '..', 'rhythm.html');
  await page.goto(filePath);
  await page.waitForTimeout(300);

  await page.screenshot({ path: path.resolve(__dirname, 'rhythm_00_start.png') });

  await page.click('#startBtn');
  await page.waitForTimeout(200);
  await page.screenshot({ path: path.resolve(__dirname, 'rhythm_01_playing.png') });

  // Check canvas is not blank
  const blankCheck1 = await page.evaluate(() => {
    const c = document.getElementById('game');
    const ctx = c.getContext('2d');
    const data = ctx.getImageData(0, 0, c.width, c.height).data;
    let nonBlack = 0;
    for (let i = 0; i < data.length; i += 40) {
      if (data[i] > 10 || data[i+1] > 10 || data[i+2] > 10) nonBlack++;
    }
    return nonBlack;
  });

  // BPM 96 -> SEC_PER_BEAT = 0.625s, LEAD_TIME=1.8s -> first hit ~1.8s after start
  // Send spacebar presses timed at each beat approx for ~8 seconds to hit several notes
  const start = Date.now();
  let presses = 0;
  while (Date.now() - start < 7000) {
    await page.keyboard.down('Space');
    await page.waitForTimeout(60);
    await page.keyboard.up('Space');
    presses++;
    await page.waitForTimeout(560); // approx one beat minus the 60ms hold
  }

  await page.waitForTimeout(300);
  const hud = await page.evaluate(() => {
    return {
      score: document.getElementById('scoreEl').textContent,
      acc: document.getElementById('accEl').textContent,
      combo: document.getElementById('comboEl').textContent,
    };
  });

  await page.screenshot({ path: path.resolve(__dirname, 'rhythm_02_after_taps.png') });

  const blankCheck2 = await page.evaluate(() => {
    const c = document.getElementById('game');
    const ctx = c.getContext('2d');
    const data = ctx.getImageData(0, 0, c.width, c.height).data;
    let nonBlack = 0;
    for (let i = 0; i < data.length; i += 40) {
      if (data[i] > 10 || data[i+1] > 10 || data[i+2] > 10) nonBlack++;
    }
    return nonBlack;
  });

  console.log(JSON.stringify({ errors, hud, presses, blankCheck1, blankCheck2 }, null, 2));

  await browser.close();
})();
