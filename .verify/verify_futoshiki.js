const { chromium } = require('/home/ubuntu/ws/jump-jump-game/.verify/node_modules/playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: '/home/ubuntu/.cache/ms-playwright/chromium-1234/chrome-linux/chrome' });
  const page = await browser.newPage({ viewport: { width: 420, height: 840 } });
  const errors = [];

  page.on('pageerror', (e) => errors.push('pageerror: ' + e.message));
  page.on('console', (msg) => {
    if (msg.type() === 'error') errors.push('console.error: ' + msg.text());
  });

  const filePath = 'file:///home/ubuntu/ws/jump-jump-game/futoshiki.html';
  console.log('Navigating to:', filePath);
  await page.goto(filePath);
  await page.waitForTimeout(400);

  console.log('1. Checking Adventure Map render...');
  await page.screenshot({ path: '/home/ubuntu/ws/jump-jump-game/.verify/futoshiki_01_map.png' });

  // Check tutorial modal
  console.log('2. Testing Tutorial modal...');
  await page.click('#tutorialBtn');
  await page.waitForTimeout(200);
  const isTutorialVisible = await page.evaluate(() => document.getElementById('tutorialModal').classList.contains('active'));
  if (!isTutorialVisible) throw new Error('Tutorial modal did not show');
  await page.screenshot({ path: '/home/ubuntu/ws/jump-jump-game/.verify/futoshiki_02_tutorial.png' });
  await page.click('#closeTutorialBtn');
  await page.waitForTimeout(150);

  // Click on Stage 1
  console.log('3. Starting Stage 1...');
  const firstStage = await page.$('.stage-card:not(.locked)');
  if (!firstStage) throw new Error('No unlocked stages found');
  await firstStage.click();
  await page.waitForTimeout(300);

  await page.screenshot({ path: '/home/ubuntu/ws/jump-jump-game/.verify/futoshiki_03_gameplay_start.png' });

  // Verify board has 16 cells (4x4)
  const cellCount = await page.$$eval('.cell', (cells) => cells.length);
  console.log('Cell count for 4x4:', cellCount);
  if (cellCount !== 16) throw new Error(`Expected 16 cells for 4x4, got ${cellCount}`);

  // Test theme switch to Animals
  console.log('4. Switching theme to animals...');
  await page.click('button[data-theme="animals"]');
  await page.waitForTimeout(200);
  await page.screenshot({ path: '/home/ubuntu/ws/jump-jump-game/.verify/futoshiki_04_animals_theme.png' });

  // Test theme switch to Fruits
  console.log('5. Switching theme to fruits...');
  await page.click('button[data-theme="fruits"]');
  await page.waitForTimeout(200);
  await page.screenshot({ path: '/home/ubuntu/ws/jump-jump-game/.verify/futoshiki_05_fruits_theme.png' });

  // Test theme switch back to Numbers
  await page.click('button[data-theme="numbers"]');
  await page.waitForTimeout(150);

  // Select cell (0, 0)
  console.log('6. Selecting cell and entering number...');
  await page.click('#cell-0-0');
  await page.waitForTimeout(150);

  // Toggle memo mode
  console.log('7. Testing note mode...');
  await page.click('#noteModeBtn');
  await page.waitForTimeout(100);
  // Input note 2
  await page.click('.num-btn[data-val="2"]');
  await page.waitForTimeout(100);
  await page.click('#noteModeBtn'); // Toggle off
  await page.waitForTimeout(100);

  // Test Smart Hint
  console.log('8. Testing smart hint...');
  await page.click('#hintBtn');
  await page.waitForTimeout(300);
  await page.screenshot({ path: '/home/ubuntu/ws/jump-jump-game/.verify/futoshiki_06_hint_used.png' });

  // Solve the rest of Stage 1 to test Victory modal!
  console.log('9. Solving remaining cells in Stage 1...');
  await page.evaluate(() => {
    const game = window.game;
    for (let r = 0; r < game.gridSize; r++) {
      for (let c = 0; c < game.gridSize; c++) {
        if (game.board[r][c] === 0) {
          game.selectedCell = { r, c };
          game.handleNumberInput(game.solution[r][c]);
        }
      }
    }
  });

  await page.waitForTimeout(800);
  const isWinShow = await page.evaluate(() => document.getElementById('victoryModal').classList.contains('active'));
  console.log('Victory modal shown:', isWinShow);
  if (!isWinShow) throw new Error('Victory modal not shown after solving');
  await page.screenshot({ path: '/home/ubuntu/ws/jump-jump-game/.verify/futoshiki_07_victory.png' });

  // Return to Map
  console.log('10. Returning to Map...');
  await page.click('#winMapBtn');
  await page.waitForTimeout(300);

  // Check if Stage 2 is unlocked
  const unlockedCount = await page.$$eval('.stage-card:not(.locked)', cards => cards.length);
  console.log('Unlocked stages count now:', unlockedCount);
  if (unlockedCount < 2) throw new Error('Stage 2 was not unlocked!');

  // Test Free Play View
  console.log('11. Testing Free Play mode...');
  await page.click('button[data-view="freePlayView"]');
  await page.waitForTimeout(200);

  // Select 5x5
  await page.click('#freeSizeOptions .opt-btn[data-size="5"]');
  await page.waitForTimeout(100);
  await page.click('#startFreeBtn');
  await page.waitForTimeout(500);

  const freeCellCount = await page.$$eval('.cell', (cells) => cells.length);
  console.log('Free play 5x5 cell count:', freeCellCount);
  if (freeCellCount !== 25) throw new Error(`Expected 25 cells for 5x5, got ${freeCellCount}`);
  await page.screenshot({ path: '/home/ubuntu/ws/jump-jump-game/.verify/futoshiki_08_freeplay_5x5.png' });

  // 12. Verify Index Portal has Futoshiki
  console.log('12. Checking index.html portal...');
  const indexUrl = 'file:///home/ubuntu/ws/jump-jump-game/index.html';
  await page.goto(indexUrl);
  await page.waitForTimeout(400);

  // Filter puzzle tab
  await page.click('button[data-cat="puzzle"]');
  await page.waitForTimeout(300);

  const hasFutoshikiCard = await page.evaluate(() => {
    return !!document.querySelector('.game-card[data-id="futoshiki"]');
  });
  console.log('Futoshiki card present in index portal:', hasFutoshikiCard);
  if (!hasFutoshikiCard) throw new Error('Futoshiki card not found in index.html!');

  await page.screenshot({ path: '/home/ubuntu/ws/jump-jump-game/.verify/index_with_futoshiki.png' });

  if (errors.length > 0) {
    console.error('Errors encountered during test:', errors);
    throw new Error('Test had errors');
  }

  console.log('All Futoshiki tests completed successfully!');
  await browser.close();
})();
