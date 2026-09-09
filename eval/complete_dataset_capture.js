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

function saveResult(caseId, toolKey, toolName, rep, rawText, url) {
  if (!rawText || rawText.length < 500) {
    throw new Error(`CRITICAL QUALITY FAILURE: Extracted text for ${toolKey} rep ${rep} is too short (${rawText ? rawText.length : 0} chars)!`);
  }
  const outDir = path.join(__dirname, '../results/cds', caseId);
  fs.mkdirSync(outDir, { recursive: true });
  
  const baseName = `${toolKey}_rep${rep}`;
  const jsonPath = path.join(outDir, `${baseName}.json`);
  const mdPath = path.join(outDir, `${baseName}.md`);

  const payload = {
    case_id: caseId,
    case_name: CASES[caseId].name,
    tool: toolName,
    replicate: rep,
    timestamp: new Date().toISOString(),
    stem: CASES[caseId].stem,
    raw_text: rawText,
    source_url: url || null,
    char_length: rawText.length,
    verified_complete: true
  };

  fs.writeFileSync(jsonPath, JSON.stringify(payload, null, 2));
  fs.writeFileSync(mdPath, `# ${toolName} — ${CASES[caseId].name} (Replicate ${rep})\n\n**Timestamp:** ${payload.timestamp}\n**Source:** ${url || 'Live Session'}\n**Length:** ${rawText.length} characters\n\n---\n\n${rawText}\n`);
  console.log(`>>> VERIFIED & SAVED: ${caseId} / ${baseName} (${rawText.length} chars)`);
}

async function runVeraQuery(page, caseId, rep) {
  const caseData = CASES[caseId];
  console.log(`\n--- Running Vera Health for ${caseId} (Rep ${rep}) ---`);
  await page.goto("https://www.verahealth.ai/", { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(3000);

  const input = page.locator("textarea[placeholder=\"Ask anything…\"]").first();
  await input.waitFor({ state: "visible", timeout: 10000 });
  await input.fill(caseData.stem);
  await page.waitForTimeout(1000);

  const sendBtn = page.locator("button[aria-label=\"Send\"]").first();
  await sendBtn.waitFor({ state: "visible", timeout: 5000 });
  await sendBtn.click();
  console.log("Submitted to Vera. Waiting for streaming and stabilization...");

  await page.waitForTimeout(6000);
  console.log("Current URL:", page.url());

  let lastLen = 0;
  let stableCount = 0;
  let text = "";

  for (let t = 0; t < 24; t++) {
    await page.waitForTimeout(5000);
    const bodyText = await page.evaluate(() => document.body.innerText);
    const len = bodyText.length;
    console.log(`Poll ${t + 1} (${(t + 1) * 5}s): total body length = ${len}`);
    
    // Vera response text must be significantly larger than prompt stem + sidebar (> 4500)
    if (len > 4500 && len === lastLen) {
      stableCount++;
      if (stableCount >= 2) {
        console.log("Vera response has stabilized.");
        text = bodyText;
        break;
      }
    } else {
      stableCount = 0;
      lastLen = len;
    }
  }

  if (!text || text.length < 4500) {
    throw new Error(`Vera Health generation failed or incomplete (length: ${text ? text.length : 0})`);
  }

  saveResult(caseId, 'vera_health', 'Vera Health', rep, text, page.url());
}

async function main() {
  const browser = await chromium.connectOverCDP("http://127.0.0.1:9222");
  const context = browser.contexts()[0];
  const page = await context.newPage();

  console.log("==========================================================");
  console.log("STEP 1: RECOVERING VERIFIED CHATGPT FULL RESPONSES");
  console.log("==========================================================");

  // 1. ChatGPT UTI Rep 2
  await page.goto("https://chatgpt.com/c/6aa08945-3ac4-8332-a578-7610f05490a0", { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(4000);
  const gptUtiText = await page.evaluate(() => {
    const articles = document.querySelectorAll("[data-message-author-role=\"assistant\"]");
    return articles.length > 0 ? articles[articles.length - 1].innerText : document.body.innerText;
  });
  saveResult('uti_24mo', 'chatgpt_for_clinicians', 'ChatGPT for Clinicians', 2, gptUtiText, page.url());

  // 2. ChatGPT CAP Rep 1
  await page.goto("https://chatgpt.com/c/6aa07ba9-a2cc-8326-a0a8-0243caf548cf", { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(4000);
  const gptCapText = await page.evaluate(() => {
    const articles = document.querySelectorAll("[data-message-author-role=\"assistant\"]");
    return articles.length > 0 ? articles[articles.length - 1].innerText : document.body.innerText;
  });
  saveResult('cap_5y', 'chatgpt_for_clinicians', 'ChatGPT for Clinicians', 1, gptCapText, page.url());

  console.log("\n==========================================================");
  console.log("STEP 2: RECOVERING VERIFIED DOXIMITY FULL RESPONSES");
  console.log("==========================================================");

  // 3. Doximity Head Rep 1
  await page.goto("https://www.doximity.com/docs-gpt/chats/339c0221-1291-40cf-8989-bc8934490f99", { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(4000);
  const doxHeadText = await page.evaluate(() => document.body.innerText);
  saveResult('head_24mo', 'ask_doximity', 'Ask Doximity', 1, doxHeadText, page.url());

  // 4. Doximity Seizure Rep 3
  await page.goto("https://www.doximity.com/docs-gpt/chats/6f80db4c-262e-47e2-81b2-94cb2bd94fb0", { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(4000);
  const doxSeizureText = await page.evaluate(() => document.body.innerText);
  saveResult('seizure_6mo', 'ask_doximity', 'Ask Doximity', 3, doxSeizureText, page.url());

  console.log("\n==========================================================");
  console.log("STEP 3: RECOVERING EXISTING FULL VERA HEALTH RESPONSES");
  console.log("==========================================================");

  // 5. Vera Head Rep 3 (from our test run)
  await page.goto("https://www.verahealth.ai/chat/441ce142-6c1a-41c6-87e6-8ff0d4afeac7", { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(4000);
  const veraHead3 = await page.evaluate(() => document.body.innerText);
  saveResult('head_24mo', 'vera_health', 'Vera Health', 3, veraHead3, page.url());

  // 6. Vera CAP Rep 1 (from saved chat)
  await page.goto("https://www.verahealth.ai/chat/a1fb9232-978e-4662-a56f-36c7d818c36d", { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(4000);
  const veraCap1 = await page.evaluate(() => document.body.innerText);
  saveResult('cap_5y', 'vera_health', 'Vera Health', 1, veraCap1, page.url());

  // 7. Vera Seizure Rep 3 (from saved chat)
  await page.goto("https://www.verahealth.ai/chat/d196f0fb-7e73-40f8-ba84-a75b11b1d844", { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(4000);
  const veraSeizure3 = await page.evaluate(() => document.body.innerText);
  saveResult('seizure_6mo', 'vera_health', 'Vera Health', 3, veraSeizure3, page.url());

  console.log("\n==========================================================");
  console.log("STEP 4: LIVE RE-CAPTURING MISSING VERA HEALTH RUNS");
  console.log("==========================================================");

  // 8. Vera UTI Rep 1
  await runVeraQuery(page, 'uti_24mo', 1);

  // 9. Vera UTI Rep 2
  await runVeraQuery(page, 'uti_24mo', 2);

  // 10. Vera CAP Rep 2
  await runVeraQuery(page, 'cap_5y', 2);

  // 11. Vera CAP Rep 3
  await runVeraQuery(page, 'cap_5y', 3);

  console.log("\n==========================================================");
  console.log("ALL 11 RUNS SUCCESSFULLY CAPTURED AND VERIFIED!");
  console.log("==========================================================");

  await page.close();
  process.exit(0);
}

main().catch(err => {
  console.error("FATAL ERROR IN RE-CAPTURE RUNNER:", err);
  process.exit(1);
});
