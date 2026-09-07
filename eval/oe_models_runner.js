const { chromium } = require('/tmp/playwright-test/node_modules/playwright');
const fs = require('fs');

const STEM = `A 24-month-old boy is brought to clinic by his mother for ear pain.

He has had cold symptoms for 5 days. Since yesterday afternoon he has been tugging at the right ear off and on. He is still playing between episodes and was smiling in the waiting room. Mother gave acetaminophen once overnight; it took the edge off. He is eating a little less than usual but taking fluids well. No vomiting, no drainage from the ear. She thought he felt warm last night. Clinic temperature is 101.7°F (38.7°C). Immunizations up to date. No drug allergies. Weight 12.4 kg. Otherwise healthy.

Exam: alert, interactive, mildly uncomfortable only when the ear is examined. HR 118, RR 26, SpO2 99% RA. Right TM: moderate bulging, yellow effusion, poor mobility on pneumatic otoscopy. Left TM normal, no effusion. No mastoid tenderness. Remainder of exam unremarkable.

What is your plan?`;

const TIERS = [
  { name: 'Osler', label: 'Direct answers at the point of care', waitSec: 30 },
  { name: 'Sackett', label: 'Comprehensive answers for complex cases', waitSec: 60 },
  { name: 'Snow', label: 'Deep consults, long-form research', waitSec: 330 }
];

async function runTier(browser, tier) {
  console.log(`\n======================================================`);
  console.log(`STARTING OPEN EVIDENCE EVALUATION: ${tier.name.toUpperCase()}`);
  console.log(`======================================================`);

  const context = browser.contexts()[0];
  const page = await context.newPage();
  
  try {
    console.log(`Navigating to https://www.openevidence.com/ ...`);
    await page.goto('https://www.openevidence.com/', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(4000);

    // Open model selector
    console.log(`Selecting model: ${tier.name}...`);
    const modelBtn = page.locator('button:has(span:has-text("Osler")), button:has(span:has-text("Sackett")), button:has(span:has-text("Snow"))').first();
    await modelBtn.waitFor({ state: 'visible', timeout: 15000 });
    await modelBtn.click();
    await page.waitForTimeout(1000);

    // Click the specific tier
    const targetOption = page.locator(`div:has-text("${tier.name}")`).filter({ hasText: tier.label }).first();
    if (await targetOption.isVisible()) {
      await targetOption.click();
      console.log(`Clicked tier option: ${tier.name}`);
    } else {
      console.log(`Trying fallback selector for ${tier.name}...`);
      await page.locator(`text=${tier.name}`).last().click();
    }
    await page.waitForTimeout(1500);

    // Fill in textarea
    console.log(`Locating textarea...`);
    const inputEl = page.locator('textarea').first();
    await inputEl.waitFor({ state: 'visible', timeout: 10000 });
    await inputEl.click();
    await page.waitForTimeout(500);
    await inputEl.fill(STEM);
    console.log(`Filled case stem into textarea.`);

    // Submit
    const submitBtn = page.locator('button[aria-label="Submit question"]').first();
    if (await submitBtn.isVisible()) {
      await submitBtn.click();
      console.log(`Clicked submit button.`);
    } else {
      await page.keyboard.press('Enter');
      console.log(`Pressed Enter to submit.`);
    }

    console.log(`Waiting ${tier.waitSec} seconds for ${tier.name} generation...`);
    const interval = 10;
    for (let elapsed = 0; elapsed < tier.waitSec; elapsed += interval) {
      await page.waitForTimeout(interval * 1000);
      console.log(`... ${tier.name}: elapsed ${elapsed + interval}s / ${tier.waitSec}s`);
    }

    // Extract complete text content including citations and references
    const text = await page.evaluate(() => {
      // Find the main answer container
      const mainContent = document.querySelector('main, article, .prose, [data-message-author-role="assistant"]');
      if (mainContent) {
        return mainContent.innerText;
      }
      return document.body.innerText;
    });

    const outFile = `results/cds/oe_tiers/${tier.name.toLowerCase()}`;
    fs.writeFileSync(`${outFile}.json`, JSON.stringify({
      tool: 'OpenEvidence',
      model_tier: tier.name,
      timestamp: new Date().toISOString(),
      raw_text: text
    }, null, 2));

    fs.writeFileSync(`${outFile}.md`, `# OpenEvidence (${tier.name}) — Clinical Evaluation\n\n**Model Tier:** ${tier.name} (${tier.label})\n**Timestamp:** ${new Date().toISOString()}\n**Case Stem:** Pediatric Acute Otitis Media (24-Month-Old)\n\n---\n\n## Verbatim Output\n\n${text}\n`);
    console.log(`SUCCESS: ${tier.name} generation extracted (${text.length} chars). Saved to ${outFile}.md`);

  } catch (err) {
    console.error(`Error during ${tier.name} evaluation:`, err);
  } finally {
    await page.close();
  }
}

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  console.log('Connected to Chrome over CDP!');

  for (const tier of TIERS) {
    await runTier(browser, tier);
    await new Promise(r => setTimeout(r, 4000));
  }

  console.log('\n======================================================');
  console.log('ALL 3 OPEN EVIDENCE TIERS COMPLETED SUCCESSFULLY!');
  console.log('======================================================');
  process.exit(0);
}

main().catch(e => { console.error(e); process.exit(1); });
