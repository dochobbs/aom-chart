const { chromium } = require('/tmp/playwright-test/node_modules/playwright');

(async () => {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('chatgpt.com'));
  
  for (const m of ['5.6 Sol', '5.6 Terra', '5.6 Luna']) {
    console.log('\n========================================');
    console.log('Testing model:', m);
    
    // Open pill button
    const pill = page.locator('button.__composer-pill').first();
    await pill.click();
    await page.waitForTimeout(500);
    
    // Click target model
    const opt = page.locator(`[role="menuitemradio"], div`).filter({ hasText: m }).last();
    await opt.click();
    await page.waitForTimeout(500);
    
    const pillText = (await pill.innerText()).replace(/\n/g, ' - ');
    console.log('Selected pill text:', pillText);
    
    // Inspect thinking modes available
    await pill.click();
    await page.waitForTimeout(500);
    
    const menuContent = await page.evaluate(() => {
      const popover = document.querySelector('[data-radix-popper-content-wrapper], [role="menu"]');
      return popover ? popover.innerText : 'No popover';
    });
    console.log('Popover details for', m, ':\n', menuContent);
    
    await page.keyboard.press('Escape');
    await page.waitForTimeout(400);
  }
  
  process.exit(0);
})();
