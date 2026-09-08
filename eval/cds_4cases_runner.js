const { chromium } = require('/tmp/playwright-test/node_modules/playwright');
const fs = require('fs');
const path = require('path');

const CASES = {
  head_24mo: {
    id: 'head_24mo',
    name: 'Minor Head Injury (24 Months)',
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

const VENDORS = [
  { name: 'OpenEvidence', match: 'openevidence.com', url: 'https://www.openevidence.com/', selector: 'textarea', waitSec: 30 },
  { name: 'UpToDate Expert AI', match: 'uptodate.com', url: 'https://ai.uptodate.com/?dpRedirect=false', selector: 'textarea', waitSec: 30 },
  { name: 'AMBOSS Clinical Care', match: 'amboss.com', url: 'https://next.amboss.com/us/clinical-care', selector: 'textarea', waitSec: 30 },
  { name: 'Vera Health', match: 'verahealth.ai', url: 'https://www.verahealth.ai/', selector: 'textarea', waitSec: 35 },
  { name: 'Ask Doximity', match: 'doximity.com', url: 'https://www.doximity.com/ask', selector: 'textarea', waitSec: 30 },
  { name: 'ChatGPT for Clinicians', match: 'chatgpt.com', url: 'https://chatgpt.com/', selector: '#prompt-textarea', waitSec: 35 }
];

async function runVendorForCase(browser, vendor, caseData, repNum) {
  console.log(`\n======================================================`);
  console.log(`RUNNING: ${vendor.name} on ${caseData.name} (Rep ${repNum})`);
  console.log(`======================================================`);

  const context = browser.contexts()[0];
  const page = await context.newPage();

  try {
    console.log(`Navigating to: ${vendor.url}...`);
    await page.goto(vendor.url, { waitUntil: 'domcontentloaded', timeout: 20000 });
    await page.waitForTimeout(4000);

    // If UpToDate, try clicking New Conversation
    if (vendor.name.includes('UpToDate')) {
      const newBtn = page.locator('button:has-text("New Conversation"), a:has-text("New Conversation"), [aria-label*="New"]').first();
      if (await newBtn.isVisible().catch(() => false)) {
        await newBtn.click();
        await page.waitForTimeout(2000);
      }
    }

    console.log(`Locating input selector: ${vendor.selector}...`);
    const inputEl = page.locator(vendor.selector).first();
    await inputEl.waitFor({ state: 'visible', timeout: 15000 });
    await inputEl.click();
    await page.waitForTimeout(400);

    if (vendor.match.includes('chatgpt.com')) {
      await page.keyboard.insertText(caseData.stem);
    } else {
      await inputEl.fill(caseData.stem);
    }
    console.log(`Filled case stem into ${vendor.name}.`);
    await page.waitForTimeout(600);

    // Submit
    await page.keyboard.press('Enter');
    
    await page.waitForTimeout(1500);
    const sendBtn = page.locator('button[aria-label*="Send"], button[aria-label*="Submit"], button[data-testid="send-button"], button:has-text("Submit"), button:has-text("Ask")').first();
    if (await sendBtn.isVisible().catch(() => false)) {
      const isEnabled = await sendBtn.isEnabled().catch(() => false);
      if (isEnabled) {
        await sendBtn.click().catch(() => {});
      }
    }

    console.log(`Submitted prompt. Waiting ${vendor.waitSec}s for complete generation...`);
    for (let elapsed = 0; elapsed < vendor.waitSec; elapsed += 5) {
      await page.waitForTimeout(5000);
      process.stdout.write(`... ${elapsed + 5}s / ${vendor.waitSec}s `);
    }
    console.log('\nGeneration wait complete.');

    // Extract text
    const text = await page.evaluate(() => {
      const articles = document.querySelectorAll('[data-message-author-role="assistant"], article, .prose, .markdown, main');
      let full = '';
      articles.forEach(a => full += a.innerText + '\n---\n');
      return full || document.body.innerText;
    });

    const vendorKey = vendor.name.toLowerCase().replace(/[^a-z0-9]/g, '_').replace(/_+/g, '_').replace(/_$/, '');
    const outDir = path.join('results/cds', caseData.id);
    if (!fs.existsSync(outDir)) {
      fs.mkdirSync(outDir, { recursive: true });
    }

    const outFileRep = path.join(outDir, `${vendorKey}_rep${repNum}`);
    fs.writeFileSync(`${outFileRep}.json`, JSON.stringify({
      case_id: caseData.id,
      case_name: caseData.name,
      tool: vendor.name,
      replicate: repNum,
      timestamp: new Date().toISOString(),
      stem: caseData.stem,
      raw_text: text
    }, null, 2));

    fs.writeFileSync(`${outFileRep}.md`, `# ${vendor.name} — ${caseData.name} (Replicate ${repNum})\n\n**Timestamp:** ${new Date().toISOString()}\n**Case:** ${caseData.name}\n**Replicate:** ${repNum}\n\n---\n\n${text}\n`);
    console.log(`SUCCESS: Extracted ${text.length} chars. Saved to ${outFileRep}.json/.md`);
    return { success: true, text, timestamp: new Date().toISOString() };

  } catch (err) {
    console.error(`ERROR running ${vendor.name} rep ${repNum} on ${caseData.id}:`, err.message);
    return { success: false, error: err.message };
  } finally {
    await page.close().catch(() => {});
  }
}

async function compileVendorReports(caseData, vendor) {
  const vendorKey = vendor.name.toLowerCase().replace(/[^a-z0-9]/g, '_').replace(/_+/g, '_').replace(/_$/, '');
  const outDir = path.join('results/cds', caseData.id);
  const repOutputs = [];

  for (let rep = 1; rep <= 3; rep++) {
    const jsonPath = path.join(outDir, `${vendorKey}_rep${rep}.json`);
    if (fs.existsSync(jsonPath)) {
      const d = JSON.parse(fs.readFileSync(jsonPath, 'utf-8'));
      repOutputs.push({ rep, timestamp: d.timestamp, text: d.raw_text });
    }
  }

  if (repOutputs.length > 0) {
    let compositeMd = `# ${vendor.name} — ${caseData.name} (${repOutputs.length} Replicates)\n\n`;
    compositeMd += `**Tool / Platform:** ${vendor.name}\n`;
    compositeMd += `**Case:** ${caseData.name}\n`;
    compositeMd += `**Total Replicates:** ${repOutputs.length}\n\n`;
    compositeMd += `---\n\n## Exact Input Case Stem\n\n\`\`\`text\n${caseData.stem}\n\`\`\`\n\n---\n\n`;

    for (const o of repOutputs) {
      compositeMd += `## Replicate ${o.rep} Trace (Timestamp: ${o.timestamp})\n\n\`\`\`text\n${o.text}\n\`\`\`\n\n---\n\n`;
    }

    const compositeFile = path.join(outDir, `${vendorKey}.md`);
    fs.writeFileSync(compositeFile, compositeMd);
    console.log(`COMPILED: Triplet report (${repOutputs.length} reps) saved to ${compositeFile}`);
  }
}

async function main() {
  const args = process.argv.slice(2);
  let targetCaseIds = Object.keys(CASES);
  
  const caseArgIdx = args.indexOf('--case');
  if (caseArgIdx !== -1 && args[caseArgIdx + 1]) {
    const requested = args[caseArgIdx + 1];
    if (CASES[requested]) {
      targetCaseIds = [requested];
    } else {
      console.error(`Unknown case: ${requested}. Valid cases: ${Object.keys(CASES).join(', ')}`);
      process.exit(1);
    }
  }

  const startRepIdx = args.indexOf('--start-rep');
  const startRep = (startRepIdx !== -1 && args[startRepIdx + 1]) ? parseInt(args[startRepIdx + 1], 10) : 2;

  const endRepIdx = args.indexOf('--end-rep');
  const endRep = (endRepIdx !== -1 && args[endRepIdx + 1]) ? parseInt(args[endRepIdx + 1], 10) : 3;

  console.log(`Connecting to Chrome over CDP (http://127.0.0.1:9222)...`);
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  console.log(`Connected successfully! Target cases: ${targetCaseIds.join(', ')} | Running Replicates: ${startRep} to ${endRep}`);

  for (const caseId of targetCaseIds) {
    const caseData = CASES[caseId];
    console.log(`\n######################################################`);
    console.log(`               PROCESSING CASE: ${caseData.name.toUpperCase()}`);
    console.log(`######################################################`);

    for (const vendor of VENDORS) {
      for (let rep = startRep; rep <= endRep; rep++) {
        await runVendorForCase(browser, vendor, caseData, rep);
        await new Promise(r => setTimeout(r, 4000));
      }
      // Recompile the triplet report (combining rep 1, 2, 3)
      await compileVendorReports(caseData, vendor);
    }
  }

  console.log(`\n======================================================`);
  console.log(`ALL REQUESTED TRIPLETS COMPLETED AND COMPILED!`);
  console.log(`======================================================`);
  process.exit(0);
}

main().catch(e => { console.error(e); process.exit(1); });
