const { chromium } = require('/tmp/playwright-test/node_modules/playwright');
const fs = require('fs');

const STEM = `A 24-month-old boy is brought to clinic by his mother for ear pain.

He has had cold symptoms for 5 days. Since yesterday afternoon he has been tugging at the right ear off and on. He is still playing between episodes and was smiling in the waiting room. Mother gave acetaminophen once overnight; it took the edge off. He is eating a little less than usual but taking fluids well. No vomiting, no drainage from the ear. She thought he felt warm last night. Clinic temperature is 101.7°F (38.7°C). Immunizations up to date. No drug allergies. Weight 12.4 kg. Otherwise healthy.

Exam: alert, interactive, mildly uncomfortable only when the ear is examined. HR 118, RR 26, SpO2 99% RA. Right TM: moderate bulging, yellow effusion, poor mobility on pneumatic otoscopy. Left TM normal, no effusion. No mastoid tenderness. Remainder of exam unremarkable.

What is your plan?`;

async function main() {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222');
  const page = browser.contexts()[0].pages().find(p => p.url().includes('chatgpt.com'));
  
  console.log('Navigating to https://chatgpt.com/ ...');
  await page.goto('https://chatgpt.com/', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(3000);

  // Switch model to 5.6 Sol
  console.log('Opening model menu...');
  const pill = page.locator('button.__composer-pill').first();
  await pill.click();
  await page.waitForTimeout(600);

  console.log('Selecting 5.6 Sol...');
  await page.evaluate(() => {
    const items = Array.from(document.querySelectorAll('[role="menuitemradio"]'));
    const sol = items.find(el => el.innerText.includes('5.6 Sol'));
    if (sol) sol.click();
  });
  await page.waitForTimeout(1000);

  // Fill prompt via keyboard insert
  console.log('Focusing composer...');
  const textarea = page.locator('#prompt-textarea').first();
  await textarea.click();
  await page.waitForTimeout(400);
  
  console.log('Inserting text...');
  await page.keyboard.insertText(STEM);
  await page.waitForTimeout(600);
  
  console.log('Submitting prompt via Enter...');
  await page.keyboard.press('Enter');
  await page.waitForTimeout(3000);

  console.log('Waiting for generation...');
  for (let i = 0; i < 40; i++) {
    await page.waitForTimeout(3000);
    const state = await page.evaluate(() => {
      const stopBtn = document.querySelector('[data-testid="stop-button"], button[aria-label="Stop streaming"], button[aria-label="Stop generating"]');
      const sendBtn = document.querySelector('[data-testid="send-button"]');
      const articles = document.querySelectorAll('[data-message-author-role="assistant"]');
      return {
        isStreaming: !!stopBtn,
        hasSend: !!sendBtn,
        assistantCount: articles.length,
        lastLen: articles.length ? articles[articles.length - 1].innerText.length : 0
      };
    });
    
    console.log(`[${(i+1)*3}s] Streaming: ${state.isStreaming} | Assistant count: ${state.assistantCount} | Text len: ${state.lastLen}`);
    
    if (!state.isStreaming && state.assistantCount > 0 && state.lastLen > 100 && i > 3) {
      console.log('Generation completed!');
      break;
    }
  }

  // Extract assistant text
  const responseText = await page.evaluate(() => {
    const assistantMessages = Array.from(document.querySelectorAll('[data-message-author-role="assistant"]'));
    return assistantMessages.map(m => m.innerText).join('\n\n---\n\n');
  });

  console.log('Extracted response length:', responseText.length);
  fs.writeFileSync('results/cds/chatgpt_tiers/5.6_sol.md', `# ChatGPT for Clinicians (5.6 Sol)\n\n**Timestamp:** ${new Date().toISOString()}\n\n---\n\n${responseText}`);
  console.log('Saved to results/cds/chatgpt_tiers/5.6_sol.md');
  process.exit(0);
}

main().catch(e => { console.error(e); process.exit(1); });
