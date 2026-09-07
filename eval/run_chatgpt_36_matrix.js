const { chromium } = require('/tmp/playwright-test/node_modules/playwright');
const fs = require('fs');

const STEM = `A 24-month-old boy is brought to clinic by his mother for ear pain.

He has had cold symptoms for 5 days. Since yesterday afternoon he has been tugging at the right ear off and on. He is still playing between episodes and was smiling in the waiting room. Mother gave acetaminophen once overnight; it took the edge off. He is eating a little less than usual but taking fluids well. No vomiting, no drainage from the ear. She thought he felt warm last night. Clinic temperature is 101.7°F (38.7°C). Immunizations up to date. No drug allergies. Weight 12.4 kg. Otherwise healthy.

Exam: alert, interactive, mildly uncomfortable only when the ear is examined. HR 118, RR 26, SpO2 99% RA. Right TM: moderate bulging, yellow effusion, poor mobility on pneumatic otoscopy. Left TM normal, no effusion. No mastoid tenderness. Remainder of exam unremarkable.

What is your plan?`;

const MODELS = ['5.6 Sol', '5.6 Terra', '5.6 Luna'];
const LEVELS = [
  { name: 'Light', stepsRight: 0 },
  { name: 'Medium', stepsRight: 1 },
  { name: 'High', stepsRight: 2 },
  { name: 'Max', stepsRight: 4 }
];
const REPS = [1, 2, 3];

async function runSingleTrace(browser, modelName, level, rep) {
  const modelKey = modelName.toLowerCase().replace(/[^a-z0-9]/g, '_').replace(/_+/g, '_');
  const levelKey = level.name.toLowerCase();
  const fileKey = `${modelKey}_${levelKey}_rep${rep}`;
  const outPath = `results/cds/chatgpt_tiers/${fileKey}`;

  // Check if already completed
  if (fs.existsSync(`${outPath}.json`)) {
    console.log(`Skipping existing trace: ${fileKey}`);
    return;
  }

  console.log(`\n======================================================`);
  console.log(`STARTING: ${modelName} | Thinking: ${level.name} | Rep: ${rep}`);
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
    await page.evaluate((target) => {
      const items = Array.from(document.querySelectorAll('[role="menuitemradio"], div'));
      const el = items.find(e => e.innerText && e.innerText.trim() === target);
      if (el) el.click();
    }, modelName);
    await page.waitForTimeout(600);

    // Re-open pill to adjust thinking slider
    await pill.click();
    await page.waitForTimeout(500);

    const slider = page.locator('[role="slider"]').first();
    await slider.focus();
    await page.keyboard.press('Home');
    await page.waitForTimeout(200);

    for (let i = 0; i < level.stepsRight; i++) {
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
    console.log(`Submitted prompt. Waiting for generation...`);

    const maxWait = level.name === 'Max' ? 240 : (level.name === 'High' ? 180 : 90);
    const interval = 5;
    let complete = false;

    for (let elapsed = 0; elapsed < maxWait; elapsed += interval) {
      await page.waitForTimeout(interval * 1000);
      const state = await page.evaluate(() => {
        const stopBtn = document.querySelector('[data-testid="stop-button"], button[aria-label="Stop streaming"], button[aria-label="Stop generating"]');
        const articles = Array.from(document.querySelectorAll('article, [data-message-author-role="assistant"]'));
        const lastMsg = articles.length ? articles[articles.length - 1].innerText : '';
        return {
          isDone: !stopBtn,
          len: lastMsg.length
        };
      });

      if (state.isDone && state.len > 150 && elapsed > 10) {
        console.log(`Generated in ~${elapsed + interval}s (${state.len} chars)`);
        complete = true;
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

    fs.writeFileSync(`${outPath}.json`, JSON.stringify({
      tool: 'ChatGPT for Clinicians',
      model: modelName,
      thinking_level: level.name,
      replicate: rep,
      timestamp: new Date().toISOString(),
      raw_text: text
    }, null, 2));

    fs.writeFileSync(`${outPath}.md`, `# ChatGPT for Clinicians (${modelName} — ${level.name} Thinking — Rep ${rep})\n\n**Model:** ${modelName}\n**Thinking Level:** ${level.name}\n**Replicate:** ${rep}\n**Timestamp:** ${new Date().toISOString()}\n**Case Stem:** Pediatric Acute Otitis Media (24-Month-Old)\n\n---\n\n## Verbatim Output\n\n${text}\n`);
    console.log(`SUCCESS: Saved ${outPath}.md (${text.length} chars)`);

  } catch (err) {
    console.error(`Error in trace ${fileKey}:`, err.message);
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
        await runSingleTrace(browser, model, level, rep);
        await new Promise(r => setTimeout(r, 2500));
      }
    }
  }

  console.log('\n======================================================');
  console.log('ALL 36 TRACES COMPLETED SUCCESSFULLY!');
  console.log('======================================================');
  process.exit(0);
}

main().catch(e => { console.error(e); process.exit(1); });
