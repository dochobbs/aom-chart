const { chromium } = require('/tmp/playwright-test/node_modules/playwright');

(async () => {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('chatgpt.com'));

  for (const m of ['5.6 Sol', '5.6 Terra', '5.6 Luna']) {
    console.log(`\n========================================`);
    console.log(`Testing controls for: ${m}`);
    
    // Open pill
    const pill = page.locator('button.__composer-pill').first();
    await pill.click();
    await page.waitForTimeout(600);

    // Click model
    await page.evaluate((target) => {
      const items = Array.from(document.querySelectorAll('[role="menuitemradio"], div'));
      const el = items.find(e => e.innerText && e.innerText.trim() === target);
      if (el) el.click();
    }, m);
    await page.waitForTimeout(1000);

    const pillText = (await pill.innerText()).replace(/\n/g, ' - ');
    console.log(`Pill display for ${m}:`, pillText);

    // Re-open pill
    await pill.click();
    await page.waitForTimeout(600);

    const popoverInfo = await page.evaluate(() => {
      const popover = document.querySelector('[data-radix-popper-content-wrapper], [role="menu"]');
      if (!popover) return 'No popover';
      const slider = popover.querySelector('[role="slider"]');
      return {
        hasSlider: !!slider,
        sliderMin: slider ? slider.getAttribute('aria-valuemin') : null,
        sliderMax: slider ? slider.getAttribute('aria-valuemax') : null,
        sliderVal: slider ? slider.getAttribute('aria-valuenow') : null,
        textSnippet: popover.innerText.split('\n').slice(0, 8).join(' | ')
      };
    });

    console.log(`Popover info for ${m}:`, JSON.stringify(popoverInfo, null, 2));
    await page.keyboard.press('Escape');
    await page.waitForTimeout(400);
  }

  process.exit(0);
})();
