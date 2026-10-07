const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 900, height: 1200 } });
  const errors = [];
  page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
  page.on('pageerror', err => errors.push('pageerror: ' + err.message));

  console.log('Testing kana.html...');
  await page.goto('file://' + path.resolve(__dirname, '..', 'kana.html'));
  await page.waitForTimeout(500);

  // Check initial state
  const title = await page.title();
  console.log('Page Title:', title);

  // Click on か行 unit pill
  const pills = await page.$$('.unit-pill');
  console.log('Total unit pills found:', pills.length);
  if (pills.length >= 2) {
    await pills[1].click(); // click か行
    await page.waitForTimeout(300);
    const unitTitle = await page.$eval('.unit-title', el => el.textContent);
    console.log('Switched to unit:', unitTitle);
  }

  // Test switching to Chart tab
  await page.click('#tabChart');
  await page.waitForTimeout(300);
  const chartVisible = await page.$eval('#viewChart', el => el.style.display !== 'none');
  console.log('Chart tab visible:', chartVisible);

  // Test switching to Confusable Pairs tab
  await page.click('#tabPairs');
  await page.waitForTimeout(300);
  const pairsCount = await page.$$eval('.confusable-card', els => els.length);
  console.log('Confusable cards count:', pairsCount);

  // Switch back to units
  await page.click('#tabMainUnits');
  await page.waitForTimeout(300);

  // Screenshot
  await page.screenshot({ path: path.resolve(__dirname, 'kana_textbook.png') });
  console.log('Screenshot saved to .verify/kana_textbook.png');

  await browser.close();

  if (errors.length > 0) {
    console.error('Errors encountered:', errors);
    process.exit(1);
  } else {
    console.log('All Playwright browser tests PASSED without console errors!');
  }
})();
