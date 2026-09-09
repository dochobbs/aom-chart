const { chromium } = require('/tmp/playwright-test/node_modules/playwright');
const fs = require('fs');
const path = require('path');

const STEM = `Name:              Not documented
Age / Sex:         24 months / Male
Race / Ethnicity:  Not documented / Not documented
Insurance:         Not documented
Language:          English

A 24-month-old boy is brought to clinic by his mother for ear pain.

He has had cold symptoms for 5 days. Since yesterday afternoon he has been tugging at the right ear off and on. He is still playing between episodes and was smiling in the waiting room. Mother gave acetaminophen once overnight; it took the edge off. He is eating a little less than usual but taking fluids well. No vomiting, no drainage from the ear. She thought he felt warm last night. Clinic temperature is 101.7°F (38.7°C). Immunizations up to date. No drug allergies. Weight 12.4 kg. Otherwise healthy.

Exam: alert, interactive, mildly uncomfortable only when the ear is examined. HR 118, RR 26, SpO2 99% RA. Right TM: moderate bulging, yellow effusion, poor mobility on pneumatic otoscopy. Left TM normal, no effusion. No mastoid tenderness. Remainder of exam unremarkable.

What is your plan?`;

async function runDoximityAOM() {
  console.log("Connecting to Chrome over CDP (http://127.0.0.1:9222)...");
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const context = browser.contexts()[0];

  const results = [];

  for (let rep = 1; rep <= 3; rep++) {
    console.log(`\n========================================`);
    console.log(`RUNNING: Ask Doximity AOM Fresh Replicate ${rep} of 3`);
    console.log(`========================================`);

    const page = await context.newPage();
    try {
      console.log("Navigating to https://www.doximity.com/ask ...");
      await page.goto('https://www.doximity.com/ask', { waitUntil: 'domcontentloaded', timeout: 30000 });
      await page.waitForTimeout(4000);

      const textarea = page.locator('textarea').first();
      await textarea.waitFor({ state: 'visible', timeout: 15000 });
      await textarea.click();
      await page.waitForTimeout(500);

      await textarea.fill(STEM);
      console.log("Filled AOM stem into Ask Doximity.");
      await page.waitForTimeout(1000);

      // Submit
      await page.keyboard.press('Enter');
      await page.waitForTimeout(1000);

      const askBtn = page.locator('button:has-text("Ask"), button[aria-label*="Submit"], button[type="submit"]').first();
      if (await askBtn.isVisible().catch(() => false)) {
        if (await askBtn.isEnabled().catch(() => false)) {
          await askBtn.click().catch(() => {});
        }
      }

      console.log("Submitted prompt. Waiting 35s for complete generation...");
      for (let s = 5; s <= 35; s += 5) {
        await page.waitForTimeout(5000);
        process.stdout.write(`${s}s... `);
      }
      console.log("\nFinished waiting.");

      const text = await page.evaluate(() => {
        const articles = document.querySelectorAll('[data-message-author-role="assistant"], article, .prose, .markdown, main');
        let full = '';
        articles.forEach(a => full += a.innerText + '\n---\n');
        return full || document.body.innerText;
      });

      console.log(`Extracted text length: ${text.length} characters.`);
      const outData = {
        tool: "Ask Doximity",
        case: "aom_24mo",
        replicate: rep,
        timestamp: new Date().toISOString(),
        stem: STEM,
        raw_text: text
      };

      fs.mkdirSync('results/cds/doximity_aom_fresh', { recursive: true });
      fs.writeFileSync(`results/cds/doximity_aom_fresh/rep${rep}.json`, JSON.stringify(outData, null, 2));
      fs.writeFileSync(`results/cds/doximity_aom_fresh/rep${rep}.md`, `# Ask Doximity Fresh AOM Replicate ${rep}\n\n**Timestamp:** ${outData.timestamp}\n\n---\n\n${text}\n`);
      results.push(outData);

      // Quick analysis of duration in text
      const has10Day = /10[\s-]*days?/i.test(text);
      const has5to7Day = /5[–\-]7[\s-]*days?|7[\s-]*days?/i.test(text);
      console.log(`Rep ${rep} Findings: Contains '10 days': ${has10Day} | Contains '5-7 / 7 days': ${has5to7Day}`);

    } catch (e) {
      console.error(`Error on Rep ${rep}:`, e.message);
    } finally {
      await page.close().catch(() => {});
    }
  }

  console.log("\nAll 3 replicates complete!");
}

runDoximityAOM().catch(console.error);
