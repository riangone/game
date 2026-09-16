const { chromium } = require('/home/ubuntu/ws/jump-jump-game/.verify/node_modules/playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/home/ubuntu/.cache/ms-playwright/chromium-1234/chrome-linux/chrome'
  });
  const page = await browser.newPage({ viewport: { width: 420, height: 840 } });
  const errors = [];

  page.on('pageerror', (e) => {
    console.error('PAGE ERROR:', e.message);
    errors.push('pageerror: ' + e.message);
  });
  page.on('console', (msg) => {
    if (msg.type() === 'error') {
      console.error('CONSOLE ERROR:', msg.text());
      errors.push('console.error: ' + msg.text());
    }
  });

  const filePath = 'file:///home/ubuntu/ws/jump-jump-game/masyu.html';
  console.log('Navigating to:', filePath);
  await page.goto(filePath);
  await page.waitForTimeout(500);

  console.log('1. Checking Adventure Map render...');
  await page.screenshot({ path: '/home/ubuntu/ws/jump-jump-game/.verify/masyu_01_map.png' });

  // 2. Check tutorial modal
  console.log('2. Testing Tutorial modal...');
  await page.click('#tutorialBtn');
  await page.waitForTimeout(250);
  const isTutVisible = await page.evaluate(() => document.getElementById('tutorialModal').classList.contains('active'));
  if (!isTutVisible) throw new Error('Tutorial modal did not show');
  await page.screenshot({ path: '/home/ubuntu/ws/jump-jump-game/.verify/masyu_02_tutorial.png' });
  await page.click('#closeTutorialBtn');
  await page.waitForTimeout(200);

  // 3. Click on Stage 1
  console.log('3. Starting Stage 1...');
  const firstStage = await page.$('.stage-card:not(.locked)');
  if (!firstStage) throw new Error('No unlocked stages found');
  await firstStage.click();
  await page.waitForTimeout(400);
  await page.screenshot({ path: '/home/ubuntu/ws/jump-jump-game/.verify/masyu_03_gameplay_start.png' });

  // 4. Test theme switch
  console.log('4. Testing theme switches...');
  await page.click('#themeBtn'); // classic
  await page.waitForTimeout(250);
  await page.screenshot({ path: '/home/ubuntu/ws/jump-jump-game/.verify/masyu_04_classic_theme.png' });

  await page.click('#themeBtn'); // forest
  await page.waitForTimeout(250);
  await page.screenshot({ path: '/home/ubuntu/ws/jump-jump-game/.verify/masyu_05_forest_theme.png' });

  await page.click('#themeBtn'); // back to pastel
  await page.waitForTimeout(200);

  // 5. Test Smart Hint
  console.log('5. Testing smart hint...');
  await page.click('#hintBtn');
  await page.waitForTimeout(300);
  await page.screenshot({ path: '/home/ubuntu/ws/jump-jump-game/.verify/masyu_06_hint_used.png' });

  // 6. Solve the rest of Stage 1 to test Victory modal
  console.log('6. Solving Stage 1 with applySolution()...');
  await page.evaluate(() => {
    window.game.applySolution();
  });
  await page.waitForTimeout(1000);

  const isWinShow = await page.evaluate(() => document.getElementById('victoryModal').classList.contains('active'));
  console.log('Victory modal shown:', isWinShow);
  if (!isWinShow) throw new Error('Victory modal not shown after solving');
  await page.screenshot({ path: '/home/ubuntu/ws/jump-jump-game/.verify/masyu_07_victory.png' });

  // 7. Click Next Stage
  console.log('7. Testing Next Stage...');
  await page.click('#winNextBtn');
  await page.waitForTimeout(400);
  const stageBadgeText = await page.$eval('#hudStageBadge', el => el.textContent);
  console.log('Current stage after Next:', stageBadgeText);
  if (!stageBadgeText.includes('STAGE 2')) throw new Error('Did not advance to Stage 2');

  // 8. Go to Free Play
  console.log('8. Testing Free Play generator (6x6)...');
  await page.click('#backToMapBtn');
  await page.waitForTimeout(250);
  await page.click('#tabFree');
  await page.waitForTimeout(200);

  // Select 6x6
  const opt6 = await page.$('.opt-btn[data-size="6"]');
  if (opt6) await opt6.click();
  await page.click('#startFreeBtn');
  await page.waitForTimeout(500);

  const freeBadge = await page.$eval('#hudStageBadge', el => el.textContent);
  console.log('Free play badge:', freeBadge);
  if (!freeBadge.includes('FREE 6×6')) throw new Error('Free play did not start 6x6');
  await page.screenshot({ path: '/home/ubuntu/ws/jump-jump-game/.verify/masyu_08_freeplay_6x6.png' });

  if (errors.length > 0) {
    throw new Error('Errors encountered: ' + errors.join('; '));
  }

  console.log('ALL MASYU TESTS PASSED SUCCESSFULLY!');
  await browser.close();
})();
