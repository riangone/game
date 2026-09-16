const { chromium } = require('/home/ubuntu/ws/jump-jump-game/.verify/node_modules/playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/home/ubuntu/.cache/ms-playwright/chromium-1234/chrome-linux/chrome'
  });
  const page = await browser.newPage({ viewport: { width: 420, height: 840 } });
  const errors = [];

  page.on('pageerror', (e) => errors.push('pageerror: ' + e.message));
  page.on('console', (msg) => {
    if (msg.type() === 'error') errors.push('console.error: ' + msg.text());
  });

  const filePath = 'file:///home/ubuntu/ws/jump-jump-game/nonogram.html';
  console.log('Navigating to:', filePath);
  await page.goto(filePath);
  await page.waitForTimeout(400);

  console.log('1. Checking Adventure Map render...');
  await page.screenshot({ path: '/home/ubuntu/ws/jump-jump-game/.verify/nonogram_01_map.png' });

  // Check tutorial modal
  console.log('2. Testing Tutorial modal...');
  await page.click('#tutorialBtn');
  await page.waitForTimeout(200);
  const isTutorialVisible = await page.evaluate(() => document.getElementById('tutorialModal').classList.contains('active'));
  if (!isTutorialVisible) throw new Error('Tutorial modal did not show');
  await page.screenshot({ path: '/home/ubuntu/ws/jump-jump-game/.verify/nonogram_02_tutorial.png' });
  await page.click('#closeTutorialBtn');
  await page.waitForTimeout(150);

  // Click on Stage 1
  console.log('3. Starting Stage 1...');
  const firstStage = await page.$('.stage-card:not(.locked)');
  if (!firstStage) throw new Error('No unlocked stages found');
  await firstStage.click();
  await page.waitForTimeout(300);
  await page.screenshot({ path: '/home/ubuntu/ws/jump-jump-game/.verify/nonogram_03_gameplay_start.png' });

  // Verify board has 25 cells (5x5)
  const cellCount = await page.$$eval('.grid-cell', (cells) => cells.length);
  console.log('Cell count for 5x5:', cellCount);
  if (cellCount !== 25) throw new Error(`Expected 25 cells for 5x5, got ${cellCount}`);

  // Test theme switch
  console.log('4. Testing theme switches...');
  await page.click('#themeBtn'); // classic
  await page.waitForTimeout(200);
  await page.screenshot({ path: '/home/ubuntu/ws/jump-jump-game/.verify/nonogram_04_classic_theme.png' });

  await page.click('#themeBtn'); // forest
  await page.waitForTimeout(200);
  await page.screenshot({ path: '/home/ubuntu/ws/jump-jump-game/.verify/nonogram_05_forest_theme.png' });

  await page.click('#themeBtn'); // back to pastel
  await page.waitForTimeout(150);

  // Test Smart Hint
  console.log('5. Testing smart hint...');
  await page.click('#hintBtn');
  await page.waitForTimeout(300);
  await page.screenshot({ path: '/home/ubuntu/ws/jump-jump-game/.verify/nonogram_06_hint_used.png' });

  // Solve the rest of Stage 1 to test Victory modal!
  console.log('6. Solving remaining cells in Stage 1...');
  await page.evaluate(() => {
    const game = window.game;
    for (let r = 0; r < game.size; r++) {
      for (let c = 0; c < game.size; c++) {
        if (game.solution[r][c] === 1 && game.board[r][c] !== 1) {
          game.currentStroke = [];
          game.applyCellChange(r, c, 1);
          game.undoStack.push(game.currentStroke);
        }
      }
    }
    game.checkLinesSatisfaction();
    game.checkVictory();
  });

  await page.waitForTimeout(1500);
  const isWinShow = await page.evaluate(() => document.getElementById('victoryModal').classList.contains('active'));
  console.log('Victory modal shown:', isWinShow);
  if (!isWinShow) throw new Error('Victory modal not shown after solving');
  await page.screenshot({ path: '/home/ubuntu/ws/jump-jump-game/.verify/nonogram_07_victory.png' });

  // Click Next Stage
  console.log('7. Testing Next Stage...');
  await page.click('#winNextBtn');
  await page.waitForTimeout(300);
  const stageBadgeText = await page.$eval('#hudStageBadge', el => el.textContent);
  console.log('Current stage after Next:', stageBadgeText);
  if (!stageBadgeText.includes('STAGE 2')) throw new Error('Did not advance to Stage 2');

  // Go to Free Play
  console.log('8. Testing Free Play generator (10x10)...');
  await page.click('#backToMapBtn');
  await page.waitForTimeout(200);
  await page.click('#tabFree');
  await page.waitForTimeout(200);
  await page.click('.opt-btn[data-size="10"]');
  await page.waitForTimeout(100);
  await page.click('#startFreeBtn');
  await page.waitForTimeout(300);

  const free10CellCount = await page.$$eval('.grid-cell', (cells) => cells.length);
  console.log('Free play 10x10 cell count:', free10CellCount);
  if (free10CellCount !== 100) throw new Error(`Expected 100 cells for 10x10 free play, got ${free10CellCount}`);
  await page.screenshot({ path: '/home/ubuntu/ws/jump-jump-game/.verify/nonogram_08_freeplay_10x10.png' });

  // Verify Lobby integration in index.html
  console.log('9. Verifying index.html lobby integration...');
  await page.goto('file:///home/ubuntu/ws/jump-jump-game/index.html');
  await page.waitForTimeout(400);

  // Switch to puzzle tab
  await page.click('.tab-btn[data-cat="puzzle"]');
  await page.waitForTimeout(300);

  const hasNonogram = await page.evaluate(() => {
    const cards = Array.from(document.querySelectorAll('.game-card'));
    return cards.some(c => c.innerHTML.includes('nonogram.html') || c.innerHTML.includes('わくわく数織'));
  });
  console.log('Nonogram present in lobby puzzle category:', hasNonogram);
  if (!hasNonogram) throw new Error('Nonogram not found in lobby puzzle category');

  await page.screenshot({ path: '/home/ubuntu/ws/jump-jump-game/.verify/index_with_nonogram.png' });

  if (errors.length > 0) {
    console.error('Errors encountered:', errors);
    throw new Error('Errors logged during verification');
  }

  console.log('ALL NONOGRAM VERIFICATION TESTS PASSED SUCCESSFULLY!');
  await browser.close();
})();
