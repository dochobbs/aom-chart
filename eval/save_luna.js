const { chromium } = require('/tmp/playwright-test/node_modules/playwright');
const fs = require('fs');

(async () => {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const pages = browser.contexts()[0].pages();
  const page = pages[pages.length - 1];
  
  const text = await page.evaluate(() => {
    const mainEl = document.querySelector('main');
    return mainEl ? mainEl.innerText : document.body.innerText;
  });
  
  const outFile = 'results/cds/chatgpt_tiers/5.6_luna';
  fs.writeFileSync(outFile + '.json', JSON.stringify({
    tool: 'ChatGPT for Clinicians',
    model: '5.6 Luna (Max Reasoning)',
    timestamp: new Date().toISOString(),
    raw_text: text
  }, null, 2));

  fs.writeFileSync(outFile + '.md', '# ChatGPT for Clinicians (5.6 Luna - Max Reasoning)\n\n**Model:** 5.6 Luna\n**Timestamp:** ' + new Date().toISOString() + '\n**Case Stem:** Pediatric Acute Otitis Media (24-Month-Old)\n\n---\n\n## Verbatim Output\n\n' + text + '\n');
  console.log('Saved 5.6 Luna successfully! File size:', fs.statSync(outFile + '.md').size);
  process.exit(0);
})();
