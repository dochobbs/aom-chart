const { chromium } = require('/tmp/playwright-test/node_modules/playwright');
const fs = require('fs');

const STEM = `A 24-month-old boy is brought to clinic by his mother for ear pain.

He has had cold symptoms for 5 days. Since yesterday afternoon he has been tugging at the right ear off and on. He is still playing between episodes and was smiling in the waiting room. Mother gave acetaminophen once overnight; it took the edge off. He is eating a little less than usual but taking fluids well. No vomiting, no drainage from the ear. She thought he felt warm last night. Clinic temperature is 101.7°F (38.7°C). Immunizations up to date. No drug allergies. Weight 12.4 kg. Otherwise healthy.

Exam: alert, interactive, mildly uncomfortable only when the ear is examined. HR 118, RR 26, SpO2 99% RA. Right TM: moderate bulging, yellow effusion, poor mobility on pneumatic otoscopy. Left TM normal, no effusion. No mastoid tenderness. Remainder of exam unremarkable.

What is your plan?`;

const MODELS = ['5.6 Sol', '5.6 Terra', '5.6 Luna'];
const LEVELS = [
  { name: 'Light', steps: 0, waitSec: 75 },
  { name: 'Medium', steps: 1, waitSec: 100 },
  { name: 'High', steps: 2, waitSec: 140 },
  { name: 'Max', steps: 4, waitSec: 240 }
];
const REPS = [1, 2, 3];

async function executeSingleRun(browser, modelName, level, rep) {
  const modelSlug = modelName.toLowerCase().replace(/[^a-z0-9]/g, '_').replace(/_+/g, '_');
  const levelSlug = level.name.toLowerCase();
  const fileKey = `${modelSlug}_${levelSlug}_rep${rep}`;
  const outPath = `results/cds/chatgpt_tiers/${fileKey}`;

  if (fs.existsSync(`${outPath}.json`) && fs.statSync(`${outPath}.json`).size > 200) {
    console.log(`[SKIP] Already exists: ${fileKey}`);
    return;
  }

  console.log(`\n======================================================`);
  console.log(`[RUNNING] ${modelName} | Level: ${level.name} | Replicate: ${rep}`);
  console.log(`======================================================`);

  const context = browser.contexts()[0];
  const page = await context.newPage();

  try {
    await page.goto('https://chatgpt.com/', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2500);

    const pill = page.locator('form button.__composer-pill').first();
    await pill.waitFor({ state: 'visible', timeout: 12000 });

    // Step 1: Select Model
    await pill.click();
    await page.waitForSelector('[data-radix-popper-content-wrapper], [role="menu"]', { state: 'visible', timeout: 5000 });
    await page.evaluate((target) => {
      const items = Array.from(document.querySelectorAll('[role="menuitemradio"]'));
      const el = items.find(e => e.innerText.includes(target));
      if (el) el.click();
    }, modelName);
    await page.waitForTimeout(600);

    // Step 2: Set Effort Slider
    await pill.click();
    await page.waitForSelector('[data-radix-popper-content-wrapper], [role="menu"]', { state: 'visible', timeout: 5000 });
    const slider = page.locator('[role="slider"]').first();
    await slider.focus();
    await page.keyboard.press('Home');
    await page.waitForTimeout(100);
    for (let i = 0; i < level.steps; i++) {
      await page.keyboard.press('ArrowRight');
      await page.waitForTimeout(100);
    }
    await page.keyboard.press('Escape');
    await page.waitForTimeout(400);

    const activePillText = (await pill.innerText()).replace(/\n/g, ' ');
    console.log(`Configured active setting: "${activePillText}"`);

    // Step 3: Insert Prompt & Send
    const textarea = page.locator('#prompt-textarea').first();
    await textarea.click();
    await page.waitForTimeout(300);
    await page.keyboard.insertText(STEM);
    await page.waitForTimeout(400);
    await page.keyboard.press('Enter');
    console.log(`Prompt submitted. Streaming response...`);

    // Step 4: Wait for completion
    let complete = false;
    for (let elapsed = 0; elapsed < level.waitSec; elapsed += 5) {
      await page.waitForTimeout(5000);
      const state = await page.evaluate(() => {
        const stopBtn = document.querySelector('[data-testid="stop-button"], button[aria-label="Stop streaming"], button[aria-label="Stop generating"]');
        const articles = Array.from(document.querySelectorAll('article, [data-message-author-role="assistant"]'));
        const lastMsg = articles.length ? articles[articles.length - 1].innerText : '';
        return {
          isDone: !stopBtn,
          len: lastMsg.length
        };
      });

      if (state.isDone && state.len > 150 && elapsed > 8) {
        console.log(`[DONE] Finished in ~${elapsed + 5}s (${state.len} chars)`);
        complete = true;
        break;
      }
    }

    // Step 5: Extract full text & save
    const text = await page.evaluate(() => {
      const articles = Array.from(document.querySelectorAll('article, [data-message-author-role="assistant"]'));
      if (articles.length > 0) {
        return articles.map(a => a.innerText).join('\n\n---\n\n');
      }
      const main = document.querySelector('main');
      return main ? main.innerText : document.body.innerText;
    });

    fs.writeFileSync(`${outPath}.json`, JSON.stringify({
      tool: 'ChatGPT for Clinicians',
      model: modelName,
      thinking_level: level.name,
      replicate: rep,
      configured_pill: activePillText,
      timestamp: new Date().toISOString(),
      raw_text: text
    }, null, 2));

    fs.writeFileSync(`${outPath}.md`, `# ChatGPT for Clinicians (${modelName} — ${level.name} Thinking — Rep ${rep})\n\n**Model:** ${modelName}\n**Thinking Level:** ${level.name}\n**Replicate:** ${rep}\n**Timestamp:** ${new Date().toISOString()}\n**Case Stem:** Pediatric Acute Otitis Media (24-Month-Old)\n\n---\n\n## Verbatim Output\n\n${text}\n`);
    console.log(`[SAVED] ${outPath}.md (${text.length} chars)`);

  } catch (err) {
    console.error(`[ERROR] in ${fileKey}:`, err.message);
  } finally {
    await page.close();
  }
}

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  console.log('Connected to Chrome CDP!');

  for (const model of MODELS) {
    for (const level of LEVELS) {
      for (const rep of REPS) {
        await executeSingleRun(browser, model, level, rep);
        await new Promise(r => setTimeout(r, 2000));
      }
    }
  }

  console.log('\n======================================================');
  console.log('ALL 36 CHATGPT FOR CLINICIANS RUNS COMPLETE!');
  console.log('======================================================');
  process.exit(0);
}

main().catch(e => { console.error(e); process.exit(1); });
