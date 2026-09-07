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
    console.log('Navigating to fresh ChatGPT tab...');
    await page.goto('https://chatgpt.com/', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(3000);

    // Click pill
    const pill = page.locator('button.__composer-pill').first();
    await pill.click();
    await page.waitForTimeout(600);

    // Select 5.6 Luna
    console.log('Selecting 5.6 Luna...');
    await page.evaluate(() => {
      const items = Array.from(document.querySelectorAll('[role="menuitemradio"], div'));
      const luna = items.find(el => el.innerText && el.innerText.trim() === '5.6 Luna');
      if (luna) luna.click();
    });
    await page.waitForTimeout(1000);

    // Verify pill text
    const pillText = (await pill.innerText()).replace(/\n/g, ' ');
    console.log('Active pill text:', pillText);

    // Type prompt
    const textarea = page.locator('#prompt-textarea').first();
    await textarea.click();
    await page.waitForTimeout(300);
    await page.keyboard.insertText(STEM);
    await page.waitForTimeout(500);

    // Send
    await page.keyboard.press('Enter');
    console.log('Submitted prompt for 5.6 Luna. Waiting for generation...');

    for (let i = 0; i < 40; i++) {
      await page.waitForTimeout(4000);
      const isDone = await page.evaluate(() => {
        const stopBtn = document.querySelector('[data-testid="stop-button"], button[aria-label="Stop streaming"], button[aria-label="Stop generating"]');
        return !stopBtn;
      });
      console.log(`... [${(i+1)*4}s] Done status: ${isDone}`);
      if (isDone && i > 3) {
        break;
      }
    }

    const text = await page.evaluate(() => {
      const main = document.querySelector('main');
      return main ? main.innerText : document.body.innerText;
    });

    fs.writeFileSync('results/cds/chatgpt_tiers/5.6_luna.json', JSON.stringify({
      tool: 'ChatGPT for Clinicians',
      model: '5.6 Luna',
      timestamp: new Date().toISOString(),
      raw_text: text
    }, null, 2));

    fs.writeFileSync('results/cds/chatgpt_tiers/5.6_luna.md', `# ChatGPT for Clinicians (5.6 Luna)\n\n**Model:** 5.6 Luna\n**Timestamp:** ${new Date().toISOString()}\n**Case Stem:** Pediatric Acute Otitis Media (24-Month-Old)\n\n---\n\n## Verbatim Output\n\n${text}\n`);
    console.log('Successfully saved results/cds/chatgpt_tiers/5.6_luna.md');

  } finally {
    await page.close();
  }
  process.exit(0);
}

main().catch(e => { console.error(e); process.exit(1); });
