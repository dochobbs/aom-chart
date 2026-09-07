const { chromium } = require('/tmp/playwright-test/node_modules/playwright');
const fs = require('fs');

const STEM = `A 24-month-old boy is brought to clinic by his mother for ear pain.

He has had cold symptoms for 5 days. Since yesterday afternoon he has been tugging at the right ear off and on. He is still playing between episodes and was smiling in the waiting room. Mother gave acetaminophen once overnight; it took the edge off. He is eating a little less than usual but taking fluids well. No vomiting, no drainage from the ear. She thought he felt warm last night. Clinic temperature is 101.7°F (38.7°C). Immunizations up to date. No drug allergies. Weight 12.4 kg. Otherwise healthy.

Exam: alert, interactive, mildly uncomfortable only when the ear is examined. HR 118, RR 26, SpO2 99% RA. Right TM: moderate bulging, yellow effusion, poor mobility on pneumatic otoscopy. Left TM normal, no effusion. No mastoid tenderness. Remainder of exam unremarkable.

What is your plan?`;

const MODELS = [
  { name: '5.6 Terra', key: '5.6_terra', waitMaxSec: 180 },
  { name: '5.6 Luna', key: '5.6_luna', waitMaxSec: 180 }
];

async function runModel(browser, m) {
  console.log(`\n======================================================`);
  console.log(`STARTING CHATGPT FOR CLINICIANS: ${m.name.toUpperCase()}`);
  console.log(`======================================================`);

  const context = browser.contexts()[0];
  const page = await context.newPage();

  try {
    console.log(`Navigating to https://chatgpt.com/ ...`);
    await page.goto('https://chatgpt.com/', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(3500);

    // Open model selector pill
    console.log(`Selecting model: ${m.name}...`);
    const pill = page.locator('button.__composer-pill').first();
    await pill.waitFor({ state: 'visible', timeout: 15000 });
    await pill.click();
    await page.waitForTimeout(800);

    // Click model option
    const clicked = await page.evaluate((targetName) => {
      const items = Array.from(document.querySelectorAll('[role="menuitemradio"], [data-radix-collection-item], div'));
      const target = items.find(el => el.innerText && el.innerText.trim() === targetName);
      if (target) {
        target.click();
        return true;
      }
      return false;
    }, m.name);

    console.log(`Model selection clicked: ${clicked}`);
    await page.waitForTimeout(1200);

    // Focus prompt textarea
    console.log(`Focusing prompt composer...`);
    const textarea = page.locator('#prompt-textarea').first();
    await textarea.click();
    await page.waitForTimeout(400);

    console.log(`Inserting case stem...`);
    await page.keyboard.insertText(STEM);
    await page.waitForTimeout(600);

    console.log(`Submitting prompt via Enter...`);
    await page.keyboard.press('Enter');
    await page.waitForTimeout(4000);

    console.log(`Waiting for ${m.name} to complete generation (up to ${m.waitMaxSec}s)...`);
    const interval = 5;
    let complete = false;

    for (let elapsed = 0; elapsed < m.waitMaxSec; elapsed += interval) {
      await page.waitForTimeout(interval * 1000);
      
      const state = await page.evaluate(() => {
        const stopBtn = document.querySelector('[data-testid="stop-button"], button[aria-label="Stop streaming"], button[aria-label="Stop generating"]');
        const articles = Array.from(document.querySelectorAll('article, [data-message-author-role="assistant"]'));
        const lastMsg = articles.length ? articles[articles.length - 1].innerText : '';
        return {
          isStreaming: !!stopBtn,
          count: articles.length,
          len: lastMsg.length
        };
      });

      console.log(`... [${elapsed + interval}s] Streaming: ${state.isStreaming} | Assistant msg len: ${state.len}`);

      if (!state.isStreaming && state.len > 100 && elapsed > 10) {
        console.log(`SUCCESS: ${m.name} completed generation after ${elapsed + interval}s!`);
        complete = true;
        break;
      }
    }

    // Extract full text
    const text = await page.evaluate(() => {
      const articles = Array.from(document.querySelectorAll('article, [data-message-author-role="assistant"]'));
      if (articles.length > 0) {
        return articles.map(a => a.innerText).join('\n\n---\n\n');
      }
      const main = document.querySelector('main');
      return main ? main.innerText : document.body.innerText;
    });

    const outFile = `results/cds/chatgpt_tiers/${m.key}`;
    fs.writeFileSync(`${outFile}.json`, JSON.stringify({
      tool: 'ChatGPT for Clinicians',
      model: m.name,
      timestamp: new Date().toISOString(),
      raw_text: text
    }, null, 2));

    fs.writeFileSync(`${outFile}.md`, `# ChatGPT for Clinicians (${m.name})\n\n**Model:** ${m.name}\n**Timestamp:** ${new Date().toISOString()}\n**Case Stem:** Pediatric Acute Otitis Media (24-Month-Old)\n\n---\n\n## Verbatim Output\n\n${text}\n`);
    console.log(`SAVED: ${m.name} (${text.length} chars) to ${outFile}.md`);

  } catch (err) {
    console.error(`Error during ${m.name} evaluation:`, err);
  } finally {
    await page.close();
  }
}

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  console.log('Connected to Chrome over CDP!');

  for (const m of MODELS) {
    await runModel(browser, m);
    await new Promise(r => setTimeout(r, 4000));
  }

  console.log('\n======================================================');
  console.log('ALL CHATGPT FOR CLINICIANS MODELS COMPLETED!');
  console.log('======================================================');
  process.exit(0);
}

main().catch(e => { console.error(e); process.exit(1); });
