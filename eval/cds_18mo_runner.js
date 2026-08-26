const { chromium } = require('/tmp/playwright-test/node_modules/playwright');
const fs = require('fs');
const path = require('path');

const STEM_18MO = `Name:              Not documented
Age / Sex:         18 months / Male
Race / Ethnicity:  Not documented / Not documented
Insurance:         Not documented
Language:          English

An 18-month-old boy is brought to clinic by his mother for ear pain.

He has had cold symptoms for 5 days. Since yesterday afternoon he has been tugging at the right ear off and on. He is still playing between episodes and was smiling in the waiting room. Mother gave acetaminophen once overnight; it took the edge off. He is eating a little less than usual but taking fluids well. No vomiting, no drainage from the ear. She thought he felt warm last night. Clinic temperature is 101.7°F (38.7°C). Immunizations up to date. No drug allergies. Weight 11.0 kg. Otherwise healthy.

Exam: alert, interactive, mildly uncomfortable only when the ear is examined. HR 118, RR 26, SpO2 99% RA. Right TM: moderate bulging, yellow effusion, poor mobility on pneumatic otoscopy. Left TM normal, no effusion. No mastoid tenderness. Remainder of exam unremarkable.

What is your plan?`;

async function runVendor(browser, vendorName, matchUrl, newUrl, inputSelector, waitMs) {
  console.log(`\n======================================================`);
  console.log(`STARTING 18-MONTH RUN: ${vendorName}`);
  console.log(`======================================================`);
  
  const pages = browser.contexts()[0].pages();
  let page = pages.find(p => p.url().includes(matchUrl));
  if (!page) {
    console.log(`Tab for ${matchUrl} not found, creating new tab...`);
    page = await browser.contexts()[0].newPage();
  }
  
  console.log(`Navigating to clean session: ${newUrl}...`);
  await page.goto(newUrl, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(4000);
  
  // If UpToDate, try clicking New Conversation
  if (vendorName.includes('UpToDate')) {
    const newBtn = page.locator('button:has-text("New Conversation"), a:has-text("New Conversation"), [aria-label*="New"]').first();
    if (await newBtn.isVisible().catch(() => false)) {
      await newBtn.click();
      await page.waitForTimeout(2000);
    }
  }
  
  console.log(`Locating input selector: ${inputSelector}...`);
  const inputEl = page.locator(inputSelector).first();
  await inputEl.waitFor({ state: 'visible', timeout: 15000 }).catch(e => console.log('Wait warning:', e.message));
  await inputEl.click();
  await page.waitForTimeout(500);
  await inputEl.fill(STEM_18MO);
  console.log(`Filled 18mo case stem into ${vendorName}.`);
  
  await page.keyboard.press('Enter');
  console.log(`Submitted prompt. Waiting ${waitMs / 1000}s for complete generation...`);
  await page.waitForTimeout(waitMs);
  
  // Extract text
  const text = await page.evaluate(() => {
    const articles = document.querySelectorAll('[data-message-author-role="assistant"], article, .prose, .markdown, main');
    let full = '';
    articles.forEach(a => full += a.innerText + '\n---\n');
    return full || document.body.innerText;
  });
  
  const vendorKey = vendorName.toLowerCase().replace(/[^a-z0-9]/g, '_').replace(/_+/g, '_').replace(/_$/, '');
  const outDir = 'results/cds_eval/18mo';
  if (!fs.existsSync(outDir)) {
    fs.mkdirSync(outDir, { recursive: true });
  }
  const outFile = path.join(outDir, `${vendorKey}`);
  fs.writeFileSync(`${outFile}.json`, JSON.stringify({
    tool: vendorName,
    condition: '18_months_old_age_control',
    timestamp: new Date().toISOString(),
    raw_text: text
  }, null, 2));
  fs.writeFileSync(`${outFile}.md`, `# ${vendorName} — 18-Month-Old Age Control\n\n${text}`);
  console.log(`SUCCESS: Extracted ${text.length} chars. Saved to ${outFile}.json/.md`);
}

async function main() {
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  console.log('Connected to Chrome!');
  
  const vendors = [
    { name: 'OpenEvidence', match: 'openevidence.com', url: 'https://www.openevidence.com/', selector: 'textarea', wait: 25000 },
    { name: 'UpToDate Expert AI', match: 'uptodate.com', url: 'https://ai.uptodate.com/?dpRedirect=false', selector: 'textarea', wait: 25000 },
    { name: 'AMBOSS Clinical Care', match: 'amboss.com', url: 'https://next.amboss.com/us/clinical-care', selector: 'textarea', wait: 25000 },
    { name: 'Vera Health', match: 'verahealth.ai', url: 'https://www.verahealth.ai/', selector: 'textarea', wait: 35000 },
    { name: 'Ask Doximity', match: 'doximity.com', url: 'https://www.doximity.com/ask', selector: 'textarea', wait: 25000 },
    { name: 'Glass Health', match: 'glass.health', url: 'https://glass.health/new', selector: 'div[contenteditable=true], textarea', wait: 25000 },
    { name: 'ChatGPT for Clinicians', match: 'chatgpt.com', url: 'https://chatgpt.com/', selector: '#prompt-textarea', wait: 30000 }
  ];
  
  for (const v of vendors) {
    try {
      await runVendor(browser, v.name, v.match, v.url, v.selector, v.wait);
      await new Promise(r => setTimeout(r, 4000));
    } catch (err) {
      console.error(`Error running 18mo on ${v.name}:`, err);
    }
  }
  
  console.log('\nALL 18MO RUNS COMPLETE!');
  process.exit(0);
}

main().catch(e => { console.error(e); process.exit(1); });
