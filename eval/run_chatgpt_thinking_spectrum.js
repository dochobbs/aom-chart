const { chromium } = require('/tmp/playwright-test/node_modules/playwright');
const fs = require('fs');

const STEM = `A 24-month-old boy is brought to clinic by his mother for ear pain.

He has had cold symptoms for 5 days. Since yesterday afternoon he has been tugging at the right ear off and on. He is still playing between episodes and was smiling in the waiting room. Mother gave acetaminophen once overnight; it took the edge off. He is eating a little less than usual but taking fluids well. No vomiting, no drainage from the ear. She thought he felt warm last night. Clinic temperature is 101.7°F (38.7°C). Immunizations up to date. No drug allergies. Weight 12.4 kg. Otherwise healthy.

Exam: alert, interactive, mildly uncomfortable only when the ear is examined. HR 118, RR 26, SpO2 99% RA. Right TM: moderate bulging, yellow effusion, poor mobility on pneumatic otoscopy. Left TM normal, no effusion. No mastoid tenderness. Remainder of exam unremarkable.

What is your plan?`;

const RUNS = [
  { model: '5.6 Sol', thinking: 'Light', key: '5.6_sol_light', sliderPos: 0 },
  { model: '5.6 Terra', thinking: 'Light', key: '5.6_terra_light', sliderPos: 0 },
  { model: '5.6 Terra', thinking: 'Max', key: '5.6_terra_max', sliderPos: 5 },
  { model: '5.6 Luna', thinking: 'Light', key: '5.6_luna_light', sliderPos: 0 }
];

async function runConfig(browser, cfg) {
  console.log(`\n======================================================`);
  console.log(`STARTING: ${cfg.model} (${cfg.thinking} Thinking)`);
  console.log(`======================================================`);

  const context = browser.contexts()[0];
  const page = await context.newPage();

  try {
    await page.goto('https://chatgpt.com/', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(3000);

    // Open pill
    const pill = page.locator('button.__composer-pill').first();
    await pill.waitFor({ state: 'visible', timeout: 15000 });
    await pill.click();
    await page.waitForTimeout(600);

    // Select model
    await page.evaluate((mName) => {
      const items = Array.from(document.querySelectorAll('[role="menuitemradio"], div'));
      const target = items.find(el => el.innerText && el.innerText.trim() === mName);
      if (target) target.click();
    }, cfg.model);
    await page.waitForTimeout(800);

    // Adjust slider if needed
    await pill.click();
    await page.waitForTimeout(600);
    
    // Focus slider and set level
    if (cfg.sliderPos === 0) {
      await page.keyboard.press('Home');
    } else {
      await page.keyboard.press('End');
    }
    await page.waitForTimeout(400);
    await page.keyboard.press('Escape');
    await page.waitForTimeout(500);

    // Fill composer
    const textarea = page.locator('#prompt-textarea').first();
    await textarea.click();
    await page.waitForTimeout(300);
    await page.keyboard.insertText(STEM);
    await page.waitForTimeout(500);

    // Send
    await page.keyboard.press('Enter');
    console.log(`Submitted prompt. Waiting for generation...`);

    for (let i = 0; i < 45; i++) {
      await page.waitForTimeout(3000);
      const isDone = await page.evaluate(() => {
        const stopBtn = document.querySelector('[data-testid="stop-button"], button[aria-label="Stop streaming"], button[aria-label="Stop generating"]');
        return !stopBtn;
      });
      if (isDone && i > 3) {
        console.log(`Generation completed after ~${(i+1)*3}s`);
        break;
      }
    }

    const text = await page.evaluate(() => {
      const main = document.querySelector('main');
      return main ? main.innerText : document.body.innerText;
    });

    const outFile = `results/cds/chatgpt_tiers/${cfg.key}`;
    fs.writeFileSync(`${outFile}.json`, JSON.stringify({
      tool: 'ChatGPT for Clinicians',
      model: cfg.model,
      thinking: cfg.thinking,
      timestamp: new Date().toISOString(),
      raw_text: text
    }, null, 2));

    fs.writeFileSync(`${outFile}.md`, `# ChatGPT for Clinicians (${cfg.model} - ${cfg.thinking} Thinking)\n\n**Model:** ${cfg.model}\n**Thinking Level:** ${cfg.thinking}\n**Timestamp:** ${new Date().toISOString()}\n**Case Stem:** Pediatric Acute Otitis Media (24-Month-Old)\n\n---\n\n## Verbatim Output\n\n${text}\n`);
    console.log(`SAVED: ${outFile}.md (${text.length} chars)`);

  } catch (err) {
    console.error(`Error during ${cfg.key}:`, err);
  } finally {
    await page.close();
  }
}

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  console.log('Connected to Chrome CDP!');

  for (const cfg of RUNS) {
    await runConfig(browser, cfg);
    await new Promise(r => setTimeout(r, 3000));
  }

  console.log('\nALL THINKING SPECTRUM RUNS COMPLETE!');
  process.exit(0);
}

main().catch(e => { console.error(e); process.exit(1); });
