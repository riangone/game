const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 420, height: 840 } });
  const errors = [];

  page.on('pageerror', (e) => errors.push('pageerror: ' + e.message));
  page.on('console', (msg) => {
    if (msg.type() === 'error') errors.push('console.error: ' + msg.text());
  });

  const filePath = 'file://' + path.resolve(__dirname, '..', 'sudoku.html');
  await page.goto(filePath);
  await page.waitForTimeout(300);

  console.log('Checking adventure map render...');
  await page.screenshot({ path: path.resolve(__dirname, 'sudoku_01_map.png') });

  // Check tutorial modal
  console.log('Testing Tutorial modal...');
  await page.click('#tutorialBtn');
  await page.waitForTimeout(200);
  const isTutorialVisible = await page.evaluate(() => document.getElementById('tutorialModal').classList.contains('show'));
  if (!isTutorialVisible) throw new Error('Tutorial modal did not show');
  await page.screenshot({ path: path.resolve(__dirname, 'sudoku_02_tutorial.png') });
  await page.click('#closeTutorialBtn');
  await page.waitForTimeout(150);

  // Click on Stage 1
  console.log('Starting Stage 1...');
  const firstStage = await page.$('.stage-card:not(.locked)');
  if (!firstStage) throw new Error('No unlocked stages found');
  await firstStage.click();
  await page.waitForTimeout(300);

  await page.screenshot({ path: path.resolve(__dirname, 'sudoku_03_gameplay_start.png') });

  // Verify board is 4x4
  const cellCount = await page.$$eval('.cell', (cells) => cells.length);
  console.log('Cell count for 4x4:', cellCount);
  if (cellCount !== 16) throw new Error(`Expected 16 cells for 4x4, got ${cellCount}`);

  // Test theme switch to Animals
  console.log('Switching theme to animals...');
  await page.click('button[data-style="animals"]');
  await page.waitForTimeout(200);
  await page.screenshot({ path: path.resolve(__dirname, 'sudoku_04_animals_theme.png') });

  // Test theme switch back to Numbers
  await page.click('button[data-style="numbers"]');
  await page.waitForTimeout(150);

  // Select an empty cell
  const emptyCell = await page.$('.cell:not(.clue)');
  if (!emptyCell) throw new Error('No empty cell found');
  await emptyCell.click();
  await page.waitForTimeout(150);

  // Toggle memo mode
  console.log('Testing note mode...');
  await page.click('#pencilBtn');
  await page.waitForTimeout(100);
  // Input note 2
  await page.click('.num-btn:nth-child(2)');
  await page.waitForTimeout(100);
  await page.click('#pencilBtn'); // Toggle off
  await page.waitForTimeout(100);

  // Test Smart Hint
  console.log('Testing smart hint...');
  await page.click('#hintBtn');
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.resolve(__dirname, 'sudoku_05_hint_used.png') });

  // Solve the rest of Stage 1 to test Victory modal!
  console.log('Solving remaining cells in Stage 1...');
  await page.evaluate(() => {
    const game = window.__sudokuGame;
    for (let r = 0; r < game.size; r++) {
      for (let c = 0; c < game.size; c++) {
        if (game.currentGrid[r][c] === 0) {
          game.selectedCell = { r, c };
          game.handleNumberInput(game.solutionGrid[r][c]);
        }
      }
    }
  });

  await page.waitForTimeout(800);
  const isWinShow = await page.evaluate(() => document.getElementById('victoryModal').classList.contains('show'));
  console.log('Victory modal shown:', isWinShow);
  if (!isWinShow) throw new Error('Victory modal not shown after solving');
  await page.screenshot({ path: path.resolve(__dirname, 'sudoku_06_victory.png') });

  // Return to Map
  await page.click('#winMapBtn');
  await page.waitForTimeout(300);

  // Verify Stage 2 is unlocked
  const unlockedCount = await page.$$eval('.stage-card:not(.locked)', (cards) => cards.length);
  console.log('Unlocked stages count in tier 1:', unlockedCount);
  if (unlockedCount < 2) throw new Error('Stage 2 should be unlocked after clearing Stage 1');

  // Switch to Free Play View
  console.log('Testing Free Play mode...');
  await page.click('button[data-view="freePlayView"]');
  await page.waitForTimeout(200);

  // Select 6x6
  await page.click('#freeSizeOptions .opt-btn[data-size="6"]');
  await page.waitForTimeout(100);
  await page.click('#startFreeBtn');
  await page.waitForTimeout(300);

  const cellCount6 = await page.$$eval('.cell', (cells) => cells.length);
  console.log('Cell count for 6x6 free play:', cellCount6);
  if (cellCount6 !== 36) throw new Error(`Expected 36 cells for 6x6, got ${cellCount6}`);
  await page.screenshot({ path: path.resolve(__dirname, 'sudoku_07_freeplay_6x6.png') });

  if (errors.length > 0) {
    console.error('Errors found:', errors);
    throw new Error('Console or page errors detected');
  }

  console.log('All tests passed successfully!');
  await browser.close();
})();

// Also test 9x9 freeplay render
(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 420, height: 840 } });
  const filePath = 'file://' + path.resolve(__dirname, '..', 'sudoku.html');
  await page.goto(filePath);
  await page.waitForTimeout(200);
  await page.click('button[data-view="freePlayView"]');
  await page.waitForTimeout(100);
  await page.click('#freeSizeOptions .opt-btn[data-size="9"]');
  await page.waitForTimeout(100);
  await page.click('#startFreeBtn');
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.resolve(__dirname, 'sudoku_08_freeplay_9x9.png') });
  console.log('9x9 screenshot captured');
  await browser.close();
})();
