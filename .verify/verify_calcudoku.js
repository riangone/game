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

  const filePath = 'file://' + path.resolve(__dirname, '..', 'calcudoku.html');
  console.log('Navigating to:', filePath);
  await page.goto(filePath);
  await page.waitForTimeout(400);

  console.log('1. Checking Adventure Map render...');
  await page.screenshot({ path: path.resolve(__dirname, 'calcudoku_01_map.png') });

  // Check tutorial modal
  console.log('2. Testing Tutorial modal...');
  await page.click('#tutorialBtn');
  await page.waitForTimeout(200);
  const isTutorialVisible = await page.evaluate(() => document.getElementById('tutorialModal').classList.contains('show'));
  if (!isTutorialVisible) throw new Error('Tutorial modal did not show');
  await page.screenshot({ path: path.resolve(__dirname, 'calcudoku_02_tutorial.png') });
  await page.click('#closeTutorialBtn');
  await page.waitForTimeout(150);

  // Click on Stage 1
  console.log('3. Starting Stage 1...');
  const firstStage = await page.$('.stage-card:not(.locked)');
  if (!firstStage) throw new Error('No unlocked stages found');
  await firstStage.click();
  await page.waitForTimeout(300);

  await page.screenshot({ path: path.resolve(__dirname, 'calcudoku_03_gameplay_start.png') });

  // Verify board is 3x3
  const cellCount = await page.$$eval('.cell', (cells) => cells.length);
  console.log('Cell count for 3x3:', cellCount);
  if (cellCount !== 9) throw new Error(`Expected 9 cells for 3x3, got ${cellCount}`);

  // Test theme switch to Animals
  console.log('4. Switching theme to animals...');
  await page.click('button[data-theme="animals"]');
  await page.waitForTimeout(200);
  await page.screenshot({ path: path.resolve(__dirname, 'calcudoku_04_animals_theme.png') });

  // Test theme switch back to Numbers
  await page.click('button[data-theme="numbers"]');
  await page.waitForTimeout(150);

  // Select cell (0, 0)
  console.log('5. Selecting cell and entering number...');
  await page.click('.cell[data-row="0"][data-col="0"]');
  await page.waitForTimeout(150);

  // Toggle memo mode
  console.log('6. Testing note mode...');
  await page.click('#noteModeBtn');
  await page.waitForTimeout(100);
  // Input note 2
  await page.click('.num-btn[data-val="2"]');
  await page.waitForTimeout(100);
  await page.click('#noteModeBtn'); // Toggle off
  await page.waitForTimeout(100);

  // Test Smart Hint
  console.log('7. Testing smart hint...');
  await page.click('#hintBtn');
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.resolve(__dirname, 'calcudoku_05_hint_used.png') });

  // Solve the rest of Stage 1 to test Victory modal!
  console.log('8. Solving remaining cells in Stage 1...');
  await page.evaluate(() => {
    const game = window.calcudokuApp;
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
  const isWinShow = await page.evaluate(() => document.getElementById('victoryModal').classList.contains('show'));
  console.log('Victory modal shown:', isWinShow);
  if (!isWinShow) throw new Error('Victory modal not shown after solving');
  await page.screenshot({ path: path.resolve(__dirname, 'calcudoku_06_victory.png') });

  // Return to Map
  console.log('9. Returning to Map...');
  await page.click('#winMapBtn');
  await page.waitForTimeout(300);

  // Test Free Play View
  console.log('10. Testing Free Play View...');
  await page.click('button[data-view="freePlayView"]');
  await page.waitForTimeout(200);
  // Pick 4x4
  await page.click('#freeSizeOptions .opt-btn[data-size="4"]');
  await page.waitForTimeout(100);
  await page.click('#startFreeBtn');
  await page.waitForTimeout(400);

  const freeCellCount = await page.$$eval('.cell', (cells) => cells.length);
  console.log('Cell count for Free Play 4x4:', freeCellCount);
  if (freeCellCount !== 16) throw new Error(`Expected 16 cells for 4x4, got ${freeCellCount}`);
  await page.screenshot({ path: path.resolve(__dirname, 'calcudoku_07_freeplay_4x4.png') });

  console.log('All verification checks passed!');
  if (errors.length > 0) {
    console.error('Page errors encountered:', errors);
    process.exit(1);
  }

  await browser.close();
  console.log('SUCCESS!');
})();
