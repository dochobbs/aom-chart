const { chromium } = require("/tmp/playwright-test/node_modules/playwright");
const fs = require("fs");
const path = require("path");

async function renderGraphic() {
  const browser = await chromium.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: true
  });
  const page = await browser.newPage({
    viewport: { width: 1500, height: 960 },
    deviceScaleFactor: 2
  });

  const html = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: #06090e;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 24px;
    }
    #card-container {
      background: #0d121d;
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 16px;
      padding: 32px 36px;
      width: 1440px;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.85);
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 24px;
      padding-bottom: 18px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    .title-group h1 {
      color: #ffffff;
      font-size: 24px;
      font-weight: 800;
      letter-spacing: -0.4px;
      margin-bottom: 4px;
    }
    .title-group p {
      color: #94a3b8;
      font-size: 13.5px;
      font-weight: 400;
    }
    .audit-badge {
      background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%);
      border: 1px solid #3b82f6;
      color: #bfdbfe;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      padding: 5px 12px;
      border-radius: 9999px;
    }
    
    .grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
    }
    .pattern-card {
      background: rgba(18, 24, 38, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 12px;
      padding: 20px 22px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .card-top {
      margin-bottom: 12px;
    }
    .pattern-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }
    .pattern-num {
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      padding: 2px 8px;
      border-radius: 4px;
    }
    .num-red { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }
    .num-amber { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
    .num-blue { background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }
    .num-green { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }

    .case-tag {
      font-size: 11px;
      color: #64748b;
      font-weight: 600;
    }
    .pattern-title {
      font-size: 16px;
      font-weight: 700;
      color: #ffffff;
      margin-bottom: 6px;
    }
    .pattern-desc {
      font-size: 12.5px;
      color: #94a3b8;
      line-height: 1.45;
      margin-bottom: 12px;
    }
    
    .verbatim-box {
      background: #090d15;
      border-left: 3px solid;
      border-radius: 0 6px 6px 0;
      padding: 10px 14px;
      font-family: "SF Mono", Consolas, "Liberation Mono", Menlo, monospace;
      font-size: 11.5px;
      line-height: 1.5;
      color: #cbd5e1;
      margin-bottom: 12px;
    }
    .verbatim-red { border-color: #ef4444; }
    .verbatim-amber { border-color: #f59e0b; }
    .verbatim-blue { border-color: #3b82f6; }
    .verbatim-green { border-color: #10b981; }
    
    .highlight-red { color: #f87171; font-weight: 700; }
    .highlight-amber { color: #fbbf24; font-weight: 700; }
    .highlight-blue { color: #60a5fa; font-weight: 700; }
    .highlight-green { color: #34d399; font-weight: 700; }

    .takeaway {
      font-size: 12px;
      font-weight: 600;
      color: #e2e8f0;
      padding-top: 10px;
      border-top: 1px solid rgba(255, 255, 255, 0.06);
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .takeaway-label {
      font-size: 10.5px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      font-weight: 800;
      color: #64748b;
    }

    .footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 20px;
      padding-top: 14px;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      color: #64748b;
      font-size: 11.5px;
    }
  </style>
</head>
<body>
  <div id="card-container">
    <div class="header">
      <div class="title-group">
        <h1>Clinical AI in Acute Pediatrics: 4 Verbatim Cognitive & Architecture Patterns</h1>
        <p>Forensic findings from 84 live audited encounters across 7 commercial CDS tools (N=3 replicates per case).</p>
      </div>
      <div class="audit-badge">Audited Dataset (N=84)</div>
    </div>

    <div class="grid">
      <!-- CARD 1 -->
      <div class="pattern-card">
        <div class="card-top">
          <div class="pattern-header">
            <span class="pattern-num num-red">Pattern 1</span>
            <span class="case-tag">5yo Pneumonia (18.5 kg)</span>
          </div>
          <div class="pattern-title">Retrieval Accuracy ≠ Arithmetic Execution</div>
          <div class="pattern-desc">The model correctly retrieves the 90 mg/kg/day IDSA standard, but halving math drops the dose to low-dose 45 mg/kg/day while simultaneously warning against underdosing.</div>
          
          <div class="verbatim-box verbatim-red">
            "Start high-dose amoxicillin 90 mg/kg/day... For this 18.5 kg child: <span class="highlight-red">415 mg PO every 12 hours</span>"<br>
            <span style="color:#64748b;">Bottom of same trace:</span> "Common Pitfalls: Underdosing amoxicillin (<span class="highlight-red">45 mg/kg/day</span>) may be insufficient..."
          </div>
        </div>
        <div class="takeaway">
          <span class="takeaway-label">Clinical Rule:</span> Pediatric dosing must be handed off to deterministic calculators, not token prediction.
        </div>
      </div>

      <!-- CARD 2 -->
      <div class="pattern-card">
        <div class="card-top">
          <div class="pattern-header">
            <span class="pattern-num num-amber">Pattern 2</span>
            <span class="case-tag">6mo First Seizure (7.6 kg)</span>
          </div>
          <div class="pattern-title">Emergency Escalation vs. Diagnostic Criteria</div>
          <div class="pattern-desc">The model conflates the active 5-minute resuscitation trigger (when to give lorazepam) with the diagnostic definition of complex febrile seizure (≥15 minutes).</div>
          
          <div class="verbatim-box verbatim-amber">
            "This is a <span class="highlight-amber">complex febrile seizure because it lasted approximately 9 minutes</span>... warrants immediate ED evaluation by EMS... A seizure lasting <span class="highlight-amber">≥5 minutes</span> should be treated as prolonged/status epilepticus..."
          </div>
        </div>
        <div class="takeaway">
          <span class="takeaway-label">Clinical Rule:</span> Acute status epilepticus protocols override baseline diagnostic definitions during unconstrained generation.
        </div>
      </div>

      <!-- CARD 3 -->
      <div class="pattern-card">
        <div class="card-top">
          <div class="pattern-header">
            <span class="pattern-num num-blue">Pattern 3</span>
            <span class="case-tag">24mo Couch Fall</span>
          </div>
          <div class="pattern-title">The "Closed-World" Chart Completion Habit</div>
          <div class="pattern-desc">When presented with unstated LOC and unwitnessed fall, the model manufactures negative facts to eliminate ambiguity and force a decisive PECARN branch.</div>
          
          <div class="verbatim-box verbatim-blue">
            "He has isolated vomiting (one episode) and <span class="highlight-blue">no LOC</span>... The history (<span class="highlight-blue">witnessed short fall</span>, single injury site, consistent mechanism) is reassuring..."
          </div>
        </div>
        <div class="takeaway">
          <span class="takeaway-label">Clinical Rule:</span> Clinical equipoise creates hallucination pressure: models invent missing facts to avoid ambiguity.
        </div>
      </div>

      <!-- CARD 4 -->
      <div class="pattern-card">
        <div class="card-top">
          <div class="pattern-header">
            <span class="pattern-num num-green">Pattern 4</span>
            <span class="case-tag">24mo Febrile UTI</span>
          </div>
          <div class="pattern-title">Active Probing vs. Passive Autocomplete</div>
          <div class="pattern-desc">Instead of guessing unstated clinical variables in prose, resilient architectures declare working assumptions and render interactive chips to solicit clinician confirmation.</div>
          
          <div class="verbatim-box verbatim-green">
            "I am assuming he can tolerate oral medication and has reliable follow-up...<br>
            <span class="highlight-green">Is there anything to add or change?</span><br>
            • vomiting or cannot tolerate oral meds • follow-up unreliable • E. coli resistance ≥15%"
          </div>
        </div>
        <div class="takeaway">
          <span class="takeaway-label">Design Rule:</span> UI friction is a safety feature: declaring assumptions explicitly prevents silent misrouting.
        </div>
      </div>
    </div>

    <div class="footer">
      <div>Source: 84 audited CDS encounters (AMBOSS, ChatGPT, Vera, OpenEvidence, Glass, UpToDate, Doximity)</div>
      <div>Repository: <code>github.com/dochobbs/aom-chart</code></div>
    </div>
  </div>
</body>
</html>
  `;

  const outDir = path.join(__dirname, "../posts");
  fs.mkdirSync(outDir, { recursive: true });
  const outPath = path.join(outDir, "clinical_ai_4patterns_infographic.png");

  await page.setContent(html, { waitUntil: "networkidle" });
  await page.waitForTimeout(600);

  const container = await page.$("#card-container");
  if (container) {
    await container.screenshot({ path: outPath });
  } else {
    await page.screenshot({ path: outPath, fullPage: true });
  }

  // Copy to Desktop
  const desktopPath = "/Users/dochobbs/Desktop/clinical_ai_4patterns_infographic.png";
  fs.copyFileSync(outPath, desktopPath);

  // Copy to artifact directory
  const artifactDir = "/Users/dochobbs/.gemini/antigravity-cli/brain/848e8396-385e-4483-b378-b981fc22610e";
  fs.mkdirSync(artifactDir, { recursive: true });
  const artifactPath = path.join(artifactDir, "clinical_ai_4patterns_infographic.png");
  fs.copyFileSync(outPath, artifactPath);

  // Copy to results
  const resultsPath = path.join(__dirname, "../results/cds/clinical_ai_4patterns_infographic.png");
  fs.copyFileSync(outPath, resultsPath);

  await browser.close();
  console.log(`Saved infographic to:\n- ${outPath}\n- ${desktopPath}\n- ${artifactPath}\n- ${resultsPath}`);
}

renderGraphic().catch(err => {
  console.error("Error rendering graphic:", err);
  process.exit(1);
});
