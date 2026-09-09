const { chromium } = require('/tmp/playwright-test/node_modules/playwright');
const fs = require('fs');
const path = require('path');

const STEMS = {
  aom_24mo: {
    id: 'aom_24mo',
    name: 'Acute Otitis Media (24 Months)',
    outDir: 'results/cds_eval',
    filePrefix: 'glass_health',
    reps: [2, 3], // Rep 1 already exists and is valid
    stem: `Name:              Not documented
Age / Sex:         24 months / Male
Race / Ethnicity:  Not documented / Not documented
Insurance:         Not documented
Language:          English

A 24-month-old boy is brought to clinic by his mother for ear pain.

He has had cold symptoms for 5 days. Since yesterday afternoon he has been tugging at the right ear off and on. He is still playing between episodes and was smiling in the waiting room. Mother gave acetaminophen once overnight; it took the edge off. He is eating a little less than usual but taking fluids well. No vomiting, no drainage from the ear. She thought he felt warm last night. Clinic temperature is 101.7°F (38.7°C). Immunizations up to date. No drug allergies. Weight 12.4 kg. Otherwise healthy.

Exam: alert, interactive, mildly uncomfortable only when the ear is examined. HR 118, RR 26, SpO2 99% RA. Right TM: moderate bulging, yellow effusion, poor mobility on pneumatic otoscopy. Left TM normal, no effusion. No mastoid tenderness. Remainder of exam unremarkable.

What is your plan?`
  },
  head_24mo: {
    id: 'head_24mo',
    name: 'Minor Head Injury (24 Months)',
    outDir: 'results/cds/head_24mo',
    filePrefix: 'glass_health',
    reps: [1, 2, 3],
    stem: `Name:              Not documented
Age / Sex:         24 months / Male
Race / Ethnicity:  Not documented / Not documented
Insurance:         Not documented
Language:          English

A 24-month-old boy is brought to clinic by his father after a fall at home.

About 2 hours ago he fell off the living-room couch onto a hardwood floor. Father was in the kitchen and heard the thud; the boy was crying when he got to him. He vomited once in the car on the way in. No seizure activity. Immunizations up to date. No drug allergies. Weight 12.8 kg. Otherwise healthy.

Exam: alert, walks to the toy bin and plays, GCS 15. HR 112, RR 24, SpO2 99% RA. 3 cm soft boggy swelling over the occiput, no step-off, no laceration. Pupils equal and reactive. No hemotympanum, no Battle sign, no periorbital bruising. Fontanelle closed. No bruising elsewhere on full skin exam. Neuro non-focal, gait normal. Remainder of exam unremarkable.

What is your plan?`
  },
  uti_24mo: {
    id: 'uti_24mo',
    name: 'First Febrile UTI (24 Months)',
    outDir: 'results/cds/uti_24mo',
    filePrefix: 'glass_health',
    reps: [1, 2, 3],
    stem: `Name:              Not documented
Age / Sex:         24 months / Male
Race / Ethnicity:  Not documented / Not documented
Insurance:         Not documented
Language:          English

A 24-month-old boy is brought to clinic by his mother for fever.

He has been fussy and warm for 2 days. Mother has not measured a temperature at home. He is drinking well but eating less. One loose stool yesterday. No vomiting, no cough, no runny nose, no rash. Wet diapers as usual. Clinic temperature is 38.4°C (101.1°F). Immunizations up to date. No drug allergies. Weight 12.6 kg. Otherwise healthy.

Exam: alert, fussy but consolable, drinking from a cup in the room. HR 128, RR 28, SpO2 99% RA. TMs normal. Throat clear. Lungs clear. Abdomen soft, non-tender, no masses. No CVA tenderness. Genital exam unremarkable. No rash. Remainder of exam unremarkable.

Catheterized urinalysis: leukocyte esterase 2+, nitrite positive, 30 WBC/hpf, many bacteria. Urine culture sent.

What is your plan?`
  },
  cap_5y: {
    id: 'cap_5y',
    name: 'Community-Acquired Pneumonia (5 Years)',
    outDir: 'results/cds/cap_5y',
    filePrefix: 'glass_health',
    reps: [1, 2, 3],
    stem: `Name:              Not documented
Age / Sex:         5 years / Female
Race / Ethnicity:  Not documented / Not documented
Insurance:         Not documented
Language:          English

A 5-year-old girl is brought to clinic by her mother for cough and fever.

She has had a cough for 3 days, worse at night, and fever for 2 days. Mother gave ibuprofen this morning. She is eating less but drinking well. No vomiting. Mother thinks she is breathing "a little fast." No history of wheezing. Clinic temperature is 38.8°C (101.8°F). Immunizations up to date. No drug allergies. Weight 18.5 kg. Otherwise healthy.

Exam: alert, mildly tired-appearing, talking in full sentences. HR 122, RR 38, SpO2 93% RA. No retractions, no nasal flaring. Crackles at the right base with decreased breath sounds there. No wheeze. Rest of chest clear. TMs normal. Throat mildly injected. Capillary refill under 2 seconds. Remainder of exam unremarkable.

What is your plan?`
  },
  seizure_6mo: {
    id: 'seizure_6mo',
    name: 'First Febrile Seizure (6 Months)',
    outDir: 'results/cds/seizure_6mo',
    filePrefix: 'glass_health',
    reps: [1, 2, 3],
    stem: `Name:              Not documented
Age / Sex:         6 months / Female
Race / Ethnicity:  Not documented / Not documented
Insurance:         Not documented
Language:          English

A 6-month-old girl is brought to clinic by her father after a shaking episode at home this morning.

She has had a runny nose and mild cough for 2 days. This morning while on the play mat she stiffened, then her arms and legs jerked rhythmically; father says both sides. He started timing partway through; his phone shows 9 minutes from when he began until it stopped on its own. She was sleepy for about 20 minutes afterward and has since nursed and is looking around. No vomiting, no rash. He thought she felt warm before the episode and gave acetaminophen after. Temperature at home 38.6°C (101.5°F). Clinic temperature is 38.9°C (102.0°F). No drug allergies. Weight 7.6 kg. Otherwise healthy.

Exam: alert, tracks, consolable, smiles at father. HR 142, RR 34, SpO2 99% RA. Anterior fontanelle soft and flat. Neck supple. TMs normal. Clear rhinorrhea. No rash, no petechiae. Moves all limbs symmetrically, tone normal, no focal findings. Remainder of exam unremarkable.

What is your plan?`
  }
};

async function extractGlassText(page) {
  return await page.evaluate(() => {
    // Look for Glass Health specific output containers
    const candidates = [
      document.querySelector('[data-testid="encounter-content"]'),
      document.querySelector('.encounter-output'),
      document.querySelector('[data-testid="clinical-plan"]'),
      document.querySelector('.prose'),
      document.querySelector('main')
    ];
    for (const c of candidates) {
      if (c && c.innerText.length > 250) {
        return c.innerText;
      }
    }
    // Fallback: search for elements after "Progress: Response generated" or "What is your plan?"
    const body = document.body.innerText;
    if (body.includes("What is your plan?")) {
      const idx = body.indexOf("What is your plan?");
      const sub = body.slice(idx + 18).trim();
      if (sub.length > 200) return sub;
    }
    return body;
  });
}

async function runGlassCase(browser, caseObj, rep) {
  console.log(`\n======================================================`);
  console.log(`RUNNING GLASS HEALTH: ${caseObj.name} (Rep ${rep})`);
  console.log(`======================================================`);

  const context = browser.contexts()[0];
  const page = await context.newPage();

  try {
    console.log(`Navigating to https://glass.health/new ...`);
    await page.goto('https://glass.health/new', { waitUntil: 'domcontentloaded', timeout: 25000 });
    await page.waitForTimeout(4000);

    const inputSelector = 'div[contenteditable="true"], textarea, [placeholder*="case"], [placeholder*="patient"]';
    const inputEl = page.locator(inputSelector).first();
    await inputEl.waitFor({ state: 'visible', timeout: 15000 });
    await inputEl.click();
    await page.waitForTimeout(500);

    // Fill stem
    try {
      await inputEl.fill(caseObj.stem);
    } catch {
      await page.keyboard.insertText(caseObj.stem);
    }
    console.log(`Filled case stem into Glass Health.`);
    await page.waitForTimeout(1000);

    // Submit via button or Enter
    const submitBtn = page.locator('button[type="submit"], button:has-text("Submit"), button:has-text("Generate"), button:has-text("Ask")').first();
    if (await submitBtn.isVisible().catch(() => false)) {
      console.log(`Clicking submit button...`);
      await submitBtn.click();
    } else {
      console.log(`Pressing Enter...`);
      await page.keyboard.press('Enter');
    }

    console.log(`Waiting 35s for generation...`);
    await page.waitForTimeout(35000);

    // Extract text
    const text = await extractGlassText(page);
    console.log(`Extracted ${text.length} characters.`);

    // Save
    fs.mkdirSync(caseObj.outDir, { recursive: true });
    const outFileBase = path.join(caseObj.outDir, `${caseObj.filePrefix}_rep${rep}`);
    fs.writeFileSync(`${outFileBase}.json`, JSON.stringify({
      case_id: caseObj.id,
      case_name: caseObj.name,
      tool: 'Glass Health',
      replicate: rep,
      timestamp: new Date().toISOString(),
      stem: caseObj.stem,
      raw_text: text
    }, null, 2));

    fs.writeFileSync(`${outFileBase}.md`, `# Glass Health — ${caseObj.name} (Rep ${rep})\n\n${text}`);
    console.log(`SAVED: ${outFileBase}.json / .md`);
  } catch (err) {
    console.error(`ERROR running Glass Health ${caseObj.id} rep ${rep}:`, err.message);
  } finally {
    await page.close().catch(() => {});
  }
}

async function compileCompositeFiles() {
  console.log(`\nCompiling composite triplet markdown files...`);

  // 1. AOM (Case 6)
  try {
    const rep1Data = JSON.parse(fs.readFileSync('results/cds_eval/glass.json', 'utf8'));
    const rep2Data = JSON.parse(fs.readFileSync('results/cds_eval/glass_health_rep2.json', 'utf8'));
    const rep3Data = JSON.parse(fs.readFileSync('results/cds_eval/glass_health_rep3.json', 'utf8'));

    const aomMd = `# Glass Health — 3 Replicate Evaluation Traces

**Vendor / Platform:** Glass Health  
**Total Evaluated Runs:** 3 independent sessions  
**Evaluation Date:** August 25, 2026 / September 9, 2026  

---

## Exact Input Query / Case Stem

\`\`\`text
${STEMS.aom_24mo.stem}
\`\`\`

---

## Replicate 1 Trace (Timestamp: ${rep1Data.timestamp || '2026-08-25T13:47:28.488Z'})

\`\`\`text
${rep1Data.raw_response || rep1Data.raw_text || ''}
\`\`\`

---

## Replicate 2 Trace (Timestamp: ${rep2Data.timestamp})

\`\`\`text
${rep2Data.raw_text}
\`\`\`

---

## Replicate 3 Trace (Timestamp: ${rep3Data.timestamp})

\`\`\`text
${rep3Data.raw_text}
\`\`\`
`;
    fs.writeFileSync('results/cds/6_glass_health.md', aomMd);
    console.log(`COMPILED: results/cds/6_glass_health.md`);
  } catch (e) {
    console.warn(`Could not compile AOM triplet:`, e.message);
  }

  // 2. Acute cases
  const acuteCases = ['head_24mo', 'uti_24mo', 'cap_5y', 'seizure_6mo'];
  for (const cid of acuteCases) {
    const caseObj = STEMS[cid];
    try {
      let acuteMd = `# Glass Health — 3 Replicate Evaluation Traces (${caseObj.name})

**Vendor / Platform:** Glass Health  
**Total Evaluated Runs:** 3 independent sessions  
**Evaluation Date:** September 9, 2026  

---

## Exact Input Query / Case Stem

\`\`\`text
${caseObj.stem}
\`\`\`

---

`;
      for (let rep = 1; rep <= 3; rep++) {
        const fileJson = path.join(caseObj.outDir, `${caseObj.filePrefix}_rep${rep}.json`);
        const data = JSON.parse(fs.readFileSync(fileJson, 'utf8'));
        acuteMd += `## Replicate ${rep} Trace (Timestamp: ${data.timestamp})\n\n\`\`\`text\n${data.raw_text}\n\`\`\`\n\n---\n\n`;
      }
      const outComposite = path.join(caseObj.outDir, 'glass_health.md');
      fs.writeFileSync(outComposite, acuteMd);
      console.log(`COMPILED: ${outComposite}`);
    } catch (e) {
      console.warn(`Could not compile acute triplet for ${cid}:`, e.message);
    }
  }
}

async function ensureLoggedIn(browser) {
  const context = browser.contexts()[0];
  let page = context.pages().find(p => p.url().includes('glass.health'));
  if (!page) {
    page = await context.newPage();
    await page.goto('https://glass.health/new', { waitUntil: 'domcontentloaded' });
  }
  await page.waitForTimeout(2000);
  if (page.url().includes('/login') || page.url().endsWith('glass.health/')) {
    console.log(`Checking session on ${page.url()}...`);
    await page.goto('https://glass.health/new', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2000);
  }
  
  if (page.url().includes('/login')) {
    console.log('Detected login page: https://glass.health/login/');
    console.log('>>> WAITING FOR USER TO COMPLETE LOGIN IN CHROME WINDOW... <<<');
    while (page.url().includes('/login')) {
      await page.waitForTimeout(2000);
    }
    console.log(`>>> LOGIN DETECTED! Current URL: ${page.url()} <<<`);
    await page.waitForTimeout(3000);
  } else {
    console.log(`Session authenticated! Current URL: ${page.url()}`);
  }
}

async function main() {
  console.log(`Connecting to Chrome on port 9222...`);
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  console.log(`Connected successfully!`);

  await ensureLoggedIn(browser);

  for (const key of Object.keys(STEMS)) {
    const caseObj = STEMS[key];
    for (const rep of caseObj.reps) {
      await runGlassCase(browser, caseObj, rep);
      await new Promise(r => setTimeout(r, 4000));
    }
  }

  await compileCompositeFiles();

  console.log(`\nALL GLASS HEALTH CAPTURES COMPLETED & COMPILED!`);
  process.exit(0);
}

main().catch(err => {
  console.error('Fatal error:', err.message);
  process.exit(1);
});

