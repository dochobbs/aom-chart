const { chromium } = require('/tmp/playwright-test/node_modules/playwright');
const fs = require('fs');

const STEM = `A 24-month-old boy is brought to clinic by his mother for ear pain.

He has had cold symptoms for 5 days. Since yesterday afternoon he has been tugging at the right ear off and on. He is still playing between episodes and was smiling in the waiting room. Mother gave acetaminophen once overnight; it took the edge off. He is eating a little less than usual but taking fluids well. No vomiting, no drainage from the ear. She thought he felt warm last night. Clinic temperature is 101.7°F (38.7°C). Immunizations up to date. No drug allergies. Weight 12.4 kg. Otherwise healthy.

Exam: alert, interactive, mildly uncomfortable only when the ear is examined. HR 118, RR 26, SpO2 99% RA. Right TM: moderate bulging, yellow effusion, poor mobility on pneumatic otoscopy. Left TM normal, no effusion. No mastoid tenderness. Remainder of exam unremarkable.

What is your plan?`;

async function testTrace(modelName, levelName, stepsRight) {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const context = browser.contexts()[0];
  const page = await context.newPage();

  try {
    console.log(`Navigating to https://chatgpt.com/ ...`);
    await page.goto('https://chatgpt.com/', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2500);

    // Open popover
    const pill = page.locator('button.__composer-pill').first();
    await pill.waitFor({ state: 'visible', timeout: 10000 });
    await pill.click();
    await page.waitForTimeout(600);

    // Select model
    await page.evaluate((target) => {
      const items = Array.from(document.querySelectorAll('[role="menuitemradio"], div'));
      const el = items.find(e => e.innerText && e.innerText.trim() === target);
      if (el) el.click();
    }, modelName);
    await page.waitForTimeout(600);

    // Open popover again to set slider
    await pill.click();
    await page.waitForTimeout(600);

    // Adjust slider
    const slider = page.locator('[role="slider"]').first();
    await slider.focus();
    await page.keyboard.press('Home');
    await page.waitForTimeout(200);

    for (let i = 0; i < stepsRight; i++) {
      await page.keyboard.press('ArrowRight');
      await page.waitForTimeout(200);
    }
    await page.keyboard.press('Escape');
    await page.waitForTimeout(400);

    // Focus prompt composer
    const textarea = page.locator('#prompt-textarea').first();
    await textarea.click();
    await page.waitForTimeout(300);
    await page.keyboard.insertText(STEM);
    await page.waitForTimeout(400);

    // Submit
    await page.keyboard.press('Enter');
    console.log(`Submitted prompt for ${modelName} (${levelName}). Waiting for generation...`);

    const maxWaitSec = levelName === 'Max' ? 240 : (levelName === 'High' ? 180 : 90);
    for (let elapsed = 0; elapsed < maxWaitSec; elapsed += 5) {
      await page.waitForTimeout(5000);
      const isDone = await page.evaluate(() => {
        const stopBtn = document.querySelector('[data-testid="stop-button"], button[aria-label="Stop streaming"], button[aria-label="Stop generating"]');
        return !stopBtn;
      });
      if (isDone && elapsed > 10) {
        console.log(`Generation completed after ~${elapsed + 5}s`);
        break;
      }
    }

    const text = await page.evaluate(() => {
      const articles = Array.from(document.querySelectorAll('article, [data-message-author-role="assistant"]'));
      if (articles.length > 0) {
        return articles.map(a => a.innerText).join('\n\n---\n\n');
      }
      const main = document.querySelector('main');
      return main ? main.innerText : document.body.innerText;
    });

    console.log(`Generated text length: ${text.length}`);
    console.log(`Preview:\n${text.slice(0, 300)}...`);

  } finally {
    await page.close();
  }
}

testTrace('5.6 Sol', 'Light', 0).then(() => process.exit(0)).catch(e => { console.error(e); process.exit(1); });
