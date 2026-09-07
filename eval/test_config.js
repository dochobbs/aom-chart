const { chromium } = require('/tmp/playwright-test/node_modules/playwright');

(async () => {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('chatgpt.com'));
  
  async function setModelAndEffort(modelName, stepsRight) {
    const pill = page.locator('form button.__composer-pill').first();
    
    // Step 1: Select Model
    await pill.click();
    await page.waitForTimeout(600);
    await page.evaluate((target) => {
      const items = Array.from(document.querySelectorAll('[role="menuitemradio"]'));
      const el = items.find(e => e.innerText.includes(target));
      if (el) el.click();
    }, modelName);
    await page.waitForTimeout(600);

    // Step 2: Set Effort
    await pill.click();
    await page.waitForTimeout(600);
    const slider = page.locator('[role="slider"]').first();
    await slider.focus();
    await page.keyboard.press('Home');
    await page.waitForTimeout(150);
    for (let i = 0; i < stepsRight; i++) {
      await page.keyboard.press('ArrowRight');
      await page.waitForTimeout(150);
    }
    await page.keyboard.press('Escape');
    await page.waitForTimeout(400);

    const resultingPill = (await pill.innerText()).replace(/\n/g, ' ');
    console.log(`Configured [${modelName}, steps: ${stepsRight}] -> Resulting pill: "${resultingPill}"`);
  }

  await setModelAndEffort('5.6 Sol', 0); // Light
  await setModelAndEffort('5.6 Terra', 2); // High
  await setModelAndEffort('5.6 Luna', 4); // Max

  process.exit(0);
})();
