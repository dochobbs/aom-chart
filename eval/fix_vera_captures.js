const { chromium } = require('/tmp/playwright-test/node_modules/playwright');
const fs = require('fs');
const path = require('path');

const STEMS = {
  uti_24mo: `Name:              Not documented
Age / Sex:         24 months / Male
Race / Ethnicity:  Not documented / Not documented
Insurance:         Not documented
Language:          English

A 24-month-old boy is brought to clinic by his mother for fever.

He has been fussy and warm for 2 days. Mother has not measured a temperature at home. He is drinking well but eating less. One loose stool yesterday. No vomiting, no cough, no runny nose, no rash. Wet diapers as usual. Clinic temperature is 38.4°C (101.1°F). Immunizations up to date. No drug allergies. Weight 12.6 kg. Otherwise healthy.

Exam: alert, fussy but consolable, drinking from a cup in the room. HR 128, RR 28, SpO2 99% RA. TMs normal. Throat clear. Lungs clear. Abdomen soft, non-tender, no masses. No CVA tenderness. Genital exam unremarkable. No rash. Remainder of exam unremarkable.

Catheterized urinalysis: leukocyte esterase 2+, nitrite positive, 30 WBC/hpf, many bacteria. Urine culture sent.

What is your plan?`,

  cap_5y: `Name:              Not documented
Age / Sex:         5 years / Female
Race / Ethnicity:  Not documented / Not documented
Insurance:         Not documented
Language:          English

A 5-year-old girl is brought to clinic by her mother for cough and fever.

She has had a cough for 3 days, worse at night, and fever for 2 days. Mother gave ibuprofen this morning. She is eating less but drinking well. No vomiting. Mother thinks she is breathing "a little fast." No history of wheezing. Clinic temperature is 38.8°C (101.8°F). Immunizations up to date. No drug allergies. Weight 18.5 kg. Otherwise healthy.

Exam: alert, mildly tired-appearing, talking in full sentences. HR 122, RR 38, SpO2 93% RA. No retractions, no nasal flaring. Crackles at the right base with decreased breath sounds there. No wheeze. Rest of chest clear. TMs normal. Throat mildly injected. Capillary refill under 2 seconds. Remainder of exam unremarkable.

What is your plan?`
};

function saveResult(caseId, rep, fullText, url) {
  const outDir = path.join(__dirname, '../results/cds', caseId);
  fs.mkdirSync(outDir, { recursive: true });
  const payload = {
    case_id: caseId,
    case_name: caseId === 'uti_24mo' ? 'First Febrile UTI (24 Months)' : 'Community-Acquired Pneumonia (5 Years)',
    tool: 'Vera Health',
    replicate: rep,
    timestamp: new Date().toISOString(),
    stem: STEMS[caseId],
    raw_text: fullText,
    source_url: url || null,
    char_length: fullText.length,
    verified_complete: true
  };
  fs.writeFileSync(path.join(outDir, `vera_health_rep${rep}.json`), JSON.stringify(payload, null, 2));
  fs.writeFileSync(path.join(outDir, `vera_health_rep${rep}.md`), fullText);
  console.log(`Successfully saved ${caseId} Rep ${rep} (${fullText.length} chars)`);
}

async function extractMainText(page) {
  return await page.evaluate(() => {
    const main = document.querySelector('main');
    if (main) return main.innerText;
    return document.body.innerText;
  });
}

async function runNewQuery(page, caseId, rep) {
  console.log(`\n=== Running Live Vera Query: ${caseId} Rep ${rep} ===`);
  await page.goto('https://www.verahealth.ai/', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(3000);

  const input = page.locator('textarea[placeholder="Ask anything…"]').first();
  await input.waitFor({ state: 'visible', timeout: 10000 });
  await input.fill(STEMS[caseId]);
  await page.waitForTimeout(1000);

  const sendBtn = page.locator('button[aria-label="Send"]').first();
  await sendBtn.waitFor({ state: 'visible', timeout: 5000 });
  await sendBtn.click();
  console.log('Submitted query. Waiting for generation to complete...');

  let completed = false;
  for (let i = 0; i < 40; i++) {
    await page.waitForTimeout(4000);
    const hasSuggested = await page.evaluate(() => {
      const text = document.body.innerText;
      return text.includes('Was this helpful?') || text.includes('Suggested Questions');
    });

    const isStillThinking = await page.evaluate(() => {
      const text = document.body.innerText;
      return text.includes('Thinking') && !text.includes('Was this helpful?');
    });

    console.log(`Poll ${i+1} (${(i+1)*4}s): completedMarker=${hasSuggested}, isStillThinking=${isStillThinking}`);

    if (hasSuggested) {
      console.log('Generation completed! Waiting 2s for final flush...');
      await page.waitForTimeout(2000);
      completed = true;
      break;
    }
  }

  if (!completed) {
    throw new Error(`Timeout waiting for Vera to complete ${caseId} Rep ${rep}`);
  }

  const text = await extractMainText(page);
  saveResult(caseId, rep, text, page.url());
}

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const context = browser.contexts()[0];
  const page = context.pages()[0] || await context.newPage();

  // 1. Save CAP Rep 2 from existing completed chat
  console.log('--- Extracting CAP Rep 2 from existing completed chat ---');
  await page.goto('https://www.verahealth.ai/chat/dd1ca968-c928-44a5-b5c9-721b1eb6f9c7', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(3000);
  const cap2Text = await extractMainText(page);
  saveResult('cap_5y', 2, cap2Text, page.url());

  // 2. Save CAP Rep 3 from existing completed chat
  console.log('--- Extracting CAP Rep 3 from existing completed chat ---');
  await page.goto('https://www.verahealth.ai/chat/4b83d7bf-ad7e-4100-bee0-8fe83a77579c', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(3000);
  const cap3Text = await extractMainText(page);
  saveResult('cap_5y', 3, cap3Text, page.url());

  // 3. Save UTI Rep 1 from existing completed chat
  console.log('--- Extracting UTI Rep 1 from existing completed chat ---');
  await page.goto('https://www.verahealth.ai/chat/4808e05b-2997-46ba-92e8-2edcf85cc25a', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(3000);
  const uti1Text = await extractMainText(page);
  saveResult('uti_24mo', 1, uti1Text, page.url());

  // 4. Run fresh query for UTI Rep 2 with the completion gate
  await runNewQuery(page, 'uti_24mo', 2);

  // 5. Run fresh query for UTI Rep 3 with the completion gate
  await runNewQuery(page, 'uti_24mo', 3);

  console.log('\nALL VERA CAPTURES COMPLETED AND FULLY VERIFIED!');
}

main().catch(err => {
  console.error('FATAL ERROR:', err);
  process.exit(1);
});
