const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 800, height: 600 } });
  const errors = [];
  page.on('pageerror', (e) => errors.push('pageerror: ' + e.message));
  page.on('console', (msg) => { if (msg.type() === 'error') errors.push('console.error: ' + msg.text()); });

  const filePath = 'file://' + path.resolve(__dirname, '..', 'rhythmparadise.html');
  await page.goto(filePath);
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.resolve(__dirname, 'rp_00_start.png') });

  await page.click('#startBtn');
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.resolve(__dirname, 'rp_01_intro_stage1.png') });

  // Click "准备!" and immediately begin the precisely-scheduled key events in the
  // SAME evaluate call, so t0 (our schedule origin) aligns with the exact moment
  // startStage() sets trackStartPerf, instead of drifting behind it via a separate
  // page.click() + waitForTimeout() round trip (which was causing false misses).
  await page.evaluate(async () => {
    document.getElementById('introBtn').click();
    const bpm = 104, spb = 60 / bpm;
    const bars = [
      [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3, 3.5], [0, 1.5, 2, 3],
      [0, 1, 2, 3], [0, 1, 1.5, 2, 3], [0, 0.5, 1, 2, 3], [0, 2],
    ];
    const events = [];
    bars.forEach((arr, i) => arr.forEach((o) => events.push({ t: (i * 4 + o) * spb, dur: 0.05 })));
    events.push({ t: (7 * 4 + 3.5) * spb, dur: 1.5 * spb }); // finishing hold
    const t0 = performance.now();
    function dispatch(type) { window.dispatchEvent(new KeyboardEvent(type, { code: 'Space', bubbles: true })); }
    for (const ev of events) {
      const pressAt = t0 + ev.t * 1000;
      const releaseAt = pressAt + ev.dur * 1000;
      const waitTo = (ms) => new Promise((res) => { const d = ms - performance.now(); d > 0 ? setTimeout(res, d) : res(); });
      await waitTo(pressAt);
      dispatch('keydown');
      await waitTo(releaseAt);
      dispatch('keyup');
    }
  });
  await page.screenshot({ path: path.resolve(__dirname, 'rp_02_playing_drum.png') });

  const blankCheck = await page.evaluate(() => {
    const c = document.getElementById('game');
    const ctx = c.getContext('2d');
    const data = ctx.getImageData(0, 0, c.width, c.height).data;
    let nonBlack = 0;
    for (let i = 0; i < data.length; i += 40) {
      if (data[i] > 10 || data[i + 1] > 10 || data[i + 2] > 10) nonBlack++;
    }
    return nonBlack;
  });
  console.log('non-black pixel samples (drum stage):', blankCheck);
  const midStats = await page.evaluate(() => ({
    score: document.getElementById('scoreEl').textContent,
    acc: document.getElementById('accEl').textContent,
    combo: document.getElementById('comboEl').textContent,
  }));
  console.log('mid stats right after press loop:', JSON.stringify(midStats));

  await page.waitForTimeout(1200);
  await page.screenshot({ path: path.resolve(__dirname, 'rp_03_stage1_result.png') });

  const stage1ResultVisible = await page.evaluate(() => document.getElementById('stageResultScreen').classList.contains('show'));
  console.log('stage1 result visible:', stage1ResultVisible);
  const resultGradeText = await page.evaluate(() => document.getElementById('resultGrade').textContent);
  console.log('stage1 grade:', resultGradeText);

  await page.click('#resultBtn');
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.resolve(__dirname, 'rp_04_intro_stage2.png') });

  const introTitle = await page.evaluate(() => document.getElementById('introTitle').textContent);
  console.log('intro title after resultBtn:', introTitle);

  // Regression check for the stageIdx bug: click "准备!" and confirm the badge/name
  // during play matches whatever stage the intro card just announced.
  await page.click('#introBtn');
  await page.waitForTimeout(400);
  const playingStageName = await page.evaluate(() => document.getElementById('stageName').textContent);
  console.log('playing stage name after introBtn:', playingStageName, '(expect match with intro title above)');
  await page.screenshot({ path: path.resolve(__dirname, 'rp_05_playing_stage2.png') });

  console.log('errors:', JSON.stringify(errors));
  await browser.close();
})();
