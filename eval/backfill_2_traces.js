const { chromium } = require('/tmp/playwright-test/node_modules/playwright');
const fs = require('fs');

const STEM = `A 24-month-old boy is brought to clinic by his mother for ear pain.

He has had cold symptoms for 5 days. Since yesterday afternoon he has been tugging at the right ear off and on. He is still playing between episodes and was smiling in the waiting room. Mother gave acetaminophen once overnight; it took the edge off. He is eating a little less than usual but taking fluids well. No vomiting, no drainage from the ear. She thought he felt warm last night. Clinic temperature is 101.7°F (38.7°C). Immunizations up to date. No drug allergies. Weight 12.4 kg. Otherwise healthy.

Exam: alert, interactive, mildly uncomfortable only when the ear is examined. HR 118, RR 26, SpO2 99% RA. Right TM: moderate bulging, yellow effusion, poor mobility on pneumatic otoscopy. Left TM normal, no effusion. No mastoid tenderness. Remainder of exam unremarkable.

What is your plan?`;

const RUNS = [
  { model: '5.6 Terra', steps: 1, name: 'Medium', rep: 1, key: '5_6_terra_medium_rep1' },
  { model: '5.6 Luna', steps: 1, name: 'Medium', rep: 1, key: '5_6_luna_medium_rep1' }
];

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const context = browser.contexts()[0];

  for (const r of RUNS) {
    const outPath = `results/cds/chatgpt_tiers/${r.key}`;
    if (fs.existsSync(`${outPath}.json`)) {
      console.log(`Already exists: ${r.key}`);
      continue;
    }

    console.log(`Running backfill for: ${r.key}`);
    const page = await context.newPage();
    try {
      await page.goto('https://chatgpt.com/', { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(3000);

      const pill = page.locator('form button.__composer-pill').first();
      await pill.waitFor({ state: 'visible', timeout: 15000 });
      await pill.click();
      await page.waitForSelector('[data-radix-popper-content-wrapper], [role="menu"]', { state: 'visible', timeout: 5000 });

      await page.evaluate((target) => {
        const items = Array.from(document.querySelectorAll('[role="menuitemradio"]'));
        const el = items.find(e => e.innerText.includes(target));
        if (el) el.click();
      }, r.model);
      await page.waitForTimeout(600);

      await pill.click();
      await page.waitForSelector('[data-radix-popper-content-wrapper], [role="menu"]', { state: 'visible', timeout: 5000 });
      const slider = page.locator('[role="slider"]').first();
      await slider.focus();
      await page.keyboard.press('Home');
      await page.waitForTimeout(100);
      for (let i = 0; i < r.steps; i++) {
        await page.keyboard.press('ArrowRight');
        await page.waitForTimeout(100);
      }
      await page.keyboard.press('Escape');
      await page.waitForTimeout(400);

      const textarea = page.locator('#prompt-textarea').first();
      await textarea.click();
      await page.waitForTimeout(300);
      await page.keyboard.insertText(STEM);
      await page.waitForTimeout(400);
      await page.keyboard.press('Enter');

      for (let elapsed = 0; elapsed < 120; elapsed += 5) {
        await page.waitForTimeout(5000);
        const state = await page.evaluate(() => {
          const stopBtn = document.querySelector('[data-testid="stop-button"], button[aria-label="Stop streaming"], button[aria-label="Stop generating"]');
          const articles = Array.from(document.querySelectorAll('article, [data-message-author-role="assistant"]'));
          const lastMsg = articles.length ? articles[articles.length - 1].innerText : '';
          return { isDone: !stopBtn, len: lastMsg.length };
        });
        if (state.isDone && state.len > 150 && elapsed > 8) {
          break;
        }
      }

      const text = await page.evaluate(() => {
        const articles = Array.from(document.querySelectorAll('article, [data-message-author-role="assistant"]'));
        if (articles.length > 0) return articles.map(a => a.innerText).join('\n\n---\n\n');
        const main = document.querySelector('main');
        return main ? main.innerText : document.body.innerText;
      });

      fs.writeFileSync(`${outPath}.json`, JSON.stringify({
        tool: 'ChatGPT for Clinicians',
        model: r.model,
        thinking_level: r.name,
        replicate: r.rep,
        timestamp: new Date().toISOString(),
        raw_text: text
      }, null, 2));

      fs.writeFileSync(`${outPath}.md`, `# ChatGPT for Clinicians (${r.model} — ${r.name} Thinking — Rep ${r.rep})\n\n**Model:** ${r.model}\n**Thinking Level:** ${r.name}\n**Replicate:** ${r.rep}\n**Timestamp:** ${new Date().toISOString()}\n**Case Stem:** Pediatric Acute Otitis Media (24-Month-Old)\n\n---\n\n## Verbatim Output\n\n${text}\n`);
      console.log(`Saved ${outPath}.md`);

    } finally {
      await page.close();
    }
  }

  console.log('Backfill complete!');
  process.exit(0);
}

main().catch(e => { console.error(e); process.exit(1); });
