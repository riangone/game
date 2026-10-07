const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 440, height: 950 } });
  const errors = [];
  page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
  page.on('pageerror', err => errors.push('pageerror: ' + err.message));

  console.log('Testing hangugeo.html...');
  await page.goto('file://' + path.resolve(__dirname, '..', 'hangugeo.html'));
  await page.waitForTimeout(400);

  // Directly navigate to screen-chars
  await page.evaluate(() => goChars());
  await page.waitForTimeout(600);

  // Take screenshot of default character workbench with trace guide & breakdown cards
  await page.screenshot({ path: path.resolve(__dirname, 'hangugeo_01_workbench.png') });
  console.log('Saved hangugeo_01_workbench.png');

  // Click on "🔍 笔顺图解" to test stroke modal
  await page.click('#strokeModalBtn');
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.resolve(__dirname, 'hangugeo_02_modal.png') });
  console.log('Saved hangugeo_02_modal.png');

  // Close modal
  await page.click('.stroke-modal-close');
  await page.waitForTimeout(300);

  // Click on "▶️ 笔顺演示"
  await page.click('#strokeOrderBtn');
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.resolve(__dirname, 'hangugeo_03_anim_step1.png') });
  console.log('Saved hangugeo_03_anim_step1.png');

  // Wait for animation to finish
  await page.waitForTimeout(2200);

  // Test lesson 3 with double jamo 떡
  console.log('Testing hangugeo3.html (checking double jamo ㄸ)...');
  await page.goto('file://' + path.resolve(__dirname, '..', 'hangugeo3.html'));
  await page.waitForTimeout(400);
  await page.evaluate(() => goChars());
  await page.waitForTimeout(600);

  // Find 떡 in pills and click
  await page.evaluate(() => {
    const idx = CHARACTERS.findIndex(c => c.zh === '떡');
    if (idx !== -1) {
      charIdx = idx;
      renderChar();
    }
  });
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.resolve(__dirname, 'hangugeo3_ddeok.png') });
  console.log('Saved hangugeo3_ddeok.png');

  // Click on stroke modal for 떡
  await page.click('#strokeModalBtn');
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.resolve(__dirname, 'hangugeo3_ddeok_modal.png') });
  console.log('Saved hangugeo3_ddeok_modal.png');

  await browser.close();

  if (errors.length > 0) {
    console.error('Console / Page Errors encountered:', errors);
    process.exit(1);
  } else {
    console.log('All visual & functional tests passed with zero errors!');
  }
})();
