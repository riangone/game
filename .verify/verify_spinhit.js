const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 400, height: 800 } }); // 模拟手机窄屏
  const errors = [];
  
  page.on('pageerror', (e) => errors.push('pageerror: ' + e.message));
  page.on('console', (msg) => { 
    if (msg.type() === 'error') {
      errors.push('console.error: ' + msg.text()); 
    }
  });

  const filePath = 'file://' + path.resolve(__dirname, '..', 'spinhit.html');
  await page.goto(filePath);
  await page.waitForTimeout(200);

  // 1. 截图：开始界面
  await page.screenshot({ path: path.resolve(__dirname, 'spinhit_00_start.png') });
  console.log("Start screen captured.");

  // 2. 点击开始
  await page.click('#startBtn');
  await page.waitForTimeout(300);

  // 3. 确认已进入 playing 状态
  let gameState = await page.evaluate(() => window.__spinhitDebug.getState());
  console.log("State after start click:", gameState);

  // 4. 截图：运行中界面
  await page.screenshot({ path: path.resolve(__dirname, 'spinhit_01_playing.png') });

  // 5. 模拟 10 次点击发射，每次发射后等待飞完
  console.log("Simulating shots...");
  for (let i = 0; i < 10; i++) {
    // 检查当前状态，如果是 gameover，则重开
    gameState = await page.evaluate(() => window.__spinhitDebug.getState());
    if (gameState === 'gameover') {
      console.log("Game over detected, clicking restart...");
      await page.click('#restartBtn');
      await page.waitForTimeout(300);
    }

    // 在 Canvas 中心偏下方点击进行发射
    const box = await page.locator('#game').boundingBox();
    const clickX = box.width / 2;
    const clickY = box.height * 0.7; // 点击下部
    await page.mouse.click(clickX, clickY);

    // 等待飞针飞完 (飞行速度 900, 距离约 350px，大约需要 400ms)
    await page.waitForTimeout(500);

    const stats = await page.evaluate(() => {
      return {
        score: window.__spinhitDebug.getScore(),
        stage: window.__spinhitDebug.getStage(),
        pinsLeft: window.__spinhitDebug.getPinsLeft(),
        fever: window.__spinhitDebug.getFever(),
        state: window.__spinhitDebug.getState()
      };
    });
    console.log(`Shot ${i + 1} finished. Stats:`, stats);
  }

  // 6. 手动充能 Fever 并触发以验证 Fever 逻辑
  console.log("Testing Fever activation via debug hooks...");
  await page.evaluate(() => {
    window.__spinhitDebug.setFever(true);
  });
  await page.waitForTimeout(200);

  const feverState = await page.evaluate(() => ({
    fever: window.__spinhitDebug.getFever(),
    state: window.__spinhitDebug.getState()
  }));
  console.log("Fever state:", feverState);

  // 7. 截图：Fever 运行中
  await page.screenshot({ path: path.resolve(__dirname, 'spinhit_02_fever.png') });

  // 8. 验证风力
  await page.evaluate(() => {
    window.__spinhitDebug.setWind(-120);
  });
  await page.waitForTimeout(100);
  await page.screenshot({ path: path.resolve(__dirname, 'spinhit_03_wind.png') });

  // 9. 强制制造一次 gameover 并截图
  console.log("Forcing game over test...");
  // 确保关闭 Fever
  await page.evaluate(() => {
    if (window.__spinhitDebug.getFever()) {
      // 调试钩子把时间缩短为0以结束Fever
      window.__spinhitDebug.setFever(false);
    }
    // 关闭风力
    window.__spinhitDebug.setWind(0);
  });
  await page.waitForTimeout(100);

  // 连续发射，每次间隔 550ms，直到发生 gameover
  let retries = 0;
  while (retries < 15) {
    const currentState = await page.evaluate(() => window.__spinhitDebug.getState());
    if (currentState === 'gameover' || currentState === 'failed') {
      console.log(`Game over successfully triggered at retry ${retries}`);
      break;
    }
    if (currentState === 'playing') {
      await page.mouse.click(200, 500);
    }
    await page.waitForTimeout(550);
    retries++;
  }

  // 等待 gameover 遮罩层淡入
  await page.waitForTimeout(1000);

  const finalState = await page.evaluate(() => window.__spinhitDebug.getState());
  console.log("Final state (expected gameover):", finalState);
  await page.screenshot({ path: path.resolve(__dirname, 'spinhit_04_gameover.png') });

  console.log("Verification finished.");
  console.log("Captured errors:", errors);

  await browser.close();
})();
