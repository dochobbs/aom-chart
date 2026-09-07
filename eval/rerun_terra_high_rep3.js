const { chromium } = require('/tmp/playwright-test/node_modules/playwright');
const fs = require('fs');

const STEM = `A 24-month-old boy is brought to clinic by his mother for ear pain.

He has had cold symptoms for 5 days. Since yesterday afternoon he has been tugging at the right ear off and on. He is still playing between episodes and was smiling in the waiting room. Mother gave acetaminophen once overnight; it took the edge off. He is eating a little less than usual but taking fluids well. No vomiting, no drainage from the ear. She thought he felt warm last night. Clinic temperature is 101.7°F (38.7°C). Immunizations up to date. No drug allergies. Weight 12.4 kg. Otherwise healthy.

Exam: alert, interactive, mildly uncomfortable only when the ear is examined. HR 118, RR 26, SpO2 99% RA. Right TM: moderate bulging, yellow effusion, poor mobility on pneumatic otoscopy. Left TM normal, no effusion. No mastoid tenderness. Remainder of exam unremarkable.

What is your plan?`;

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const context = browser.contexts()[0];
  const page = await context.newPage();

  try {
    console.log('Navigating to https://chatgpt.com/ ...');
    await page.goto('https://chatgpt.com/', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(3000);

    const pill = page.locator('form button.__composer-pill').first();
    await pill.waitFor({ state: 'visible', timeout: 15000 });
    await pill.click();
    await page.waitForSelector('[data-radix-popper-content-wrapper], [role="menu"]', { state: 'visible', timeout: 5000 });

    await page.evaluate(() => {
      const items = Array.from(document.querySelectorAll('[role="menuitemradio"]'));
      const el = items.find(e => e.innerText.includes('5.6 Terra'));
      if (el) el.click();
    });
    await page.waitForTimeout(600);

    await pill.click();
    await page.waitForSelector('[data-radix-popper-content-wrapper], [role="menu"]', { state: 'visible', timeout: 5000 });
    const slider = page.locator('[role="slider"]').first();
    await slider.focus();
    await page.keyboard.press('Home');
    await page.waitForTimeout(100);
    // Level 2: High
    await page.keyboard.press('ArrowRight');
    await page.waitForTimeout(100);
    await page.keyboard.press('ArrowRight');
    await page.waitForTimeout(100);
    await page.keyboard.press('Escape');
    await page.waitForTimeout(400);

    const activePill = (await pill.innerText()).replace(/\n/g, ' ');
    console.log(`Configured setting: "${activePill}"`);

    const textarea = page.locator('#prompt-textarea').first();
    await textarea.click();
    await page.waitForTimeout(300);
    await page.keyboard.insertText(STEM);
    await page.waitForTimeout(400);
    await page.keyboard.press('Enter');
    console.log('Submitted prompt for 5_6_terra_high_rep3. Streaming response...');

    for (let elapsed = 0; elapsed < 140; elapsed += 5) {
      await page.waitForTimeout(5000);
      const state = await page.evaluate(() => {
        const stopBtn = document.querySelector('[data-testid="stop-button"], button[aria-label="Stop streaming"], button[aria-label="Stop generating"]');
        const articles = Array.from(document.querySelectorAll('article, [data-message-author-role="assistant"]'));
        const lastMsg = articles.length ? articles[articles.length - 1].innerText : '';
        return { isDone: !stopBtn, len: lastMsg.length };
      });
      if (state.isDone && state.len > 150 && elapsed > 8) {
        console.log(`Generation completed in ~${elapsed + 5}s (${state.len} chars)`);
        break;
      }
    }

    const text = await page.evaluate(() => {
      const articles = Array.from(document.querySelectorAll('article, [data-message-author-role="assistant"]'));
      if (articles.length > 0) return articles.map(a => a.innerText).join('\n\n---\n\n');
      const main = document.querySelector('main');
      return main ? main.innerText : document.body.innerText;
    });

    const outPath = 'results/cds/chatgpt_tiers/5_6_terra_high_rep3';
    fs.writeFileSync(`${outPath}.json`, JSON.stringify({
      tool: 'ChatGPT for Clinicians',
      model: '5.6 Terra',
      thinking_level: 'High',
      replicate: 3,
      configured_pill: activePill,
      timestamp: new Date().toISOString(),
      raw_text: text
    }, null, 2));

    fs.writeFileSync(`${outPath}.md`, `# ChatGPT for Clinicians (5.6 Terra — High Thinking — Rep 3)\n\n**Model:** 5.6 Terra\n**Thinking Level:** High\n**Replicate:** 3\n**Timestamp:** ${new Date().toISOString()}\n**Case Stem:** Pediatric Acute Otitis Media (24-Month-Old)\n\n---\n\n## Verbatim Output\n\n${text}\n`);
    console.log(`RE-RUN COMPLETE: Saved clean ${outPath}.md (${text.length} chars)`);

  } finally {
    await page.close();
  }
  process.exit(0);
}

main().catch(e => { console.error(e); process.exit(1); });
