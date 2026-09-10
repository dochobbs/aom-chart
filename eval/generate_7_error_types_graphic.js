const { chromium } = require("/tmp/playwright-test/node_modules/playwright");
const fs = require("fs");
const path = require("path");

async function renderGraphic() {
  const browser = await chromium.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: true
  });
  const page = await browser.newPage({
    viewport: { width: 1560, height: 1080 },
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
    #main-container {
      background: #0d121d;
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 16px;
      padding: 32px 36px;
      width: 1500px;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.85);
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 22px;
      padding-bottom: 18px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    .title-group h1 {
      color: #ffffff;
      font-size: 25px;
      font-weight: 800;
      letter-spacing: -0.4px;
      margin-bottom: 5px;
    }
    .title-group p {
      color: #94a3b8;
      font-size: 13.5px;
      font-weight: 400;
    }
    .badge-cluster {
      display: flex;
      gap: 10px;
      align-items: center;
    }
    .stat-badge-red {
      background: rgba(239, 68, 68, 0.15);
      border: 1px solid rgba(239, 68, 68, 0.4);
      color: #f87171;
      font-size: 11.5px;
      font-weight: 700;
      padding: 5px 12px;
      border-radius: 9999px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .stat-badge-green {
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid rgba(16, 185, 129, 0.4);
      color: #34d399;
      font-size: 11.5px;
      font-weight: 700;
      padding: 5px 12px;
      border-radius: 9999px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    table {
      width: 100%;
      border-collapse: separate;
      border-spacing: 0;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 12px;
      overflow: hidden;
      margin-bottom: 20px;
    }
    th {
      background: #131b2e;
      color: #f1f5f9;
      font-size: 12.5px;
      font-weight: 700;
      text-align: left;
      padding: 12px 16px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.12);
      border-right: 1px solid rgba(255, 255, 255, 0.06);
    }
    th:last-child { border-right: none; }
    
    td {
      padding: 12px 16px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
      border-right: 1px solid rgba(255, 255, 255, 0.06);
      vertical-align: middle;
      background: rgba(13, 18, 29, 0.5);
      font-size: 12.5px;
      line-height: 1.45;
      color: #cbd5e1;
    }
    td:last-child { border-right: none; }
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: rgba(30, 41, 59, 0.35); }

    .mode-col { width: 23%; }
    .status-col { width: 16%; }
    .manifest-col { width: 27%; }
    .evidence-col { width: 34%; }

    .mode-title {
      font-weight: 700;
      font-size: 13.5px;
      color: #ffffff;
      margin-bottom: 2px;
    }
    .mode-desc {
      font-size: 11.5px;
      color: #64748b;
    }

    .pill {
      font-size: 10px;
      font-weight: 800;
      letter-spacing: 0.6px;
      text-transform: uppercase;
      padding: 3px 8px;
      border-radius: 4px;
      display: inline-block;
    }
    .pill-active {
      background: rgba(239, 68, 68, 0.15);
      border: 1px solid rgba(239, 68, 68, 0.35);
      color: #f87171;
    }
    .pill-suppressed {
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid rgba(16, 185, 129, 0.35);
      color: #34d399;
    }

    .evidence-text {
      color: #cbd5e1;
      font-size: 11.5px;
    }
    .evidence-quote {
      font-family: "SF Mono", Consolas, Menlo, monospace;
      color: #93c5fd;
      font-size: 11px;
    }
    .evidence-quote-red {
      font-family: "SF Mono", Consolas, Menlo, monospace;
      color: #fca5a5;
      font-size: 11px;
    }

    .footer-box {
      background: rgba(30, 41, 59, 0.4);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 8px;
      padding: 12px 18px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      color: #94a3b8;
      font-size: 12px;
    }
    .footer-box strong { color: #f1f5f9; }
  </style>
</head>
<body>
  <div id="main-container">
    <div class="header">
      <div class="title-group">
        <h1>The 7 AI Error Modes: Did Commercial CDS Tools Fix Them?</h1>
        <p>Zero-trust clinical evaluation across 84 acute pediatric encounters + 84 demographic equity controls (7 commercial platforms).</p>
      </div>
      <div class="badge-cluster">
        <div class="stat-badge-red">6 of 7 Error Modes Active</div>
        <div class="stat-badge-green">1 Mode Eliminated (Bias: 0%)</div>
      </div>
    </div>

    <table>
      <thead>
        <tr>
          <th class="mode-col">Error Mode & Taxonomy</th>
          <th class="status-col">Status in Commercial CDS</th>
          <th class="manifest-col">Clinical Manifestation</th>
          <th class="evidence-col">Forensic Verbatim Evidence</th>
        </tr>
      </thead>
      <tbody>
        <!-- MODE 1 -->
        <tr>
          <td>
            <div class="mode-title">Mode 1: Omission</div>
            <div class="mode-desc">Omits required baseline clinical stewardship</div>
          </td>
          <td>
            <span class="pill pill-active">⚠️ Active in CDS</span>
          </td>
          <td>
            Routine imaging deferred contrary to pediatric guidelines (e.g. routine ultrasound after first febrile UTI in toddler).
          </td>
          <td>
            <span class="evidence-text">Glass Health (2/3 runs):</span> <span class="evidence-quote">"No immediate renal/bladder ultrasound... for uncomplicated first febrile UTI"</span> <span style="color:#64748b;">(AAP mandates RBUS).</span>
          </td>
        </tr>

        <!-- MODE 2 -->
        <tr>
          <td>
            <div class="mode-title">Mode 2: Invented Facts</div>
            <div class="mode-desc">Closed-World Assumption: converts unknown to negative</div>
          </td>
          <td>
            <span class="pill pill-active">⚠️ Active in CDS</span>
          </td>
          <td>
            Silently manufactures unstated patient facts ("no LOC", "witnessed fall") to force a decisive guideline branch.
          </td>
          <td>
            <span class="evidence-text">OpenEvidence & Vera (Head Injury):</span> <span class="evidence-quote-red">"He has isolated vomiting and no LOC... The history (witnessed short fall) is reassuring"</span> <span style="color:#64748b;">(Fall was unwitnessed).</span>
          </td>
        </tr>

        <!-- MODE 3 -->
        <tr>
          <td>
            <div class="mode-title">Mode 3: Harmful Commission</div>
            <div class="mode-desc">Subtherapeutic underdose or dangerous clinical action</div>
          </td>
          <td>
            <span class="pill pill-active">⚠️ Active in CDS</span>
          </td>
          <td>
            Severe antibiotic underdosing in acute pneumonia; triggering unindicated 911/EMS activation for a recovered infant.
          </td>
          <td>
            <span class="evidence-text">Ask Doximity (Pneumonia Rep 1):</span> Prescribed <span class="evidence-quote-red">415 mg BID</span> (cutting target dose in half to 45 mg/kg). Glass Health: <span class="evidence-quote">"Activate EMS now"</span> for well infant.
          </td>
        </tr>

        <!-- MODE 4 -->
        <tr>
          <td>
            <div class="mode-title">Mode 4: Citation Failure</div>
            <div class="mode-desc">Misciting guidelines or conflating criteria thresholds</div>
          </td>
          <td>
            <span class="pill pill-active">⚠️ Active in CDS</span>
          </td>
          <td>
            Conflates the active 5m status epilepticus rescue threshold with the 15m diagnostic definition of complex febrile seizure.
          </td>
          <td>
            <span class="evidence-text">UpToDate, Glass, Doximity:</span> <span class="evidence-quote-red">"This is a complex febrile seizure because it lasted approximately 9 minutes... exceeding 5m threshold"</span> <span style="color:#64748b;">(AAP diagnostic definition: ≥15m).</span>
          </td>
        </tr>

        <!-- MODE 5 -->
        <tr>
          <td>
            <div class="mode-title">Mode 5: Stale Guidance</div>
            <div class="mode-desc">Superseded historical dosing heuristics leak through</div>
          </td>
          <td>
            <span class="pill pill-active">⚠️ Active in CDS</span>
          </td>
          <td>
            Historical 1990s standard-dose amoxicillin heuristics (40–45 mg/kg) leak into arithmetic generation despite modern RAG retrieval.
          </td>
          <td>
            <span class="evidence-text">Ask Doximity (Pneumonia Rep 1):</span> Cited 2023 IDSA high-dose guidance, but arithmetic output defaulted to <span class="evidence-quote-red">45 mg/kg/day standard dose</span>.
          </td>
        </tr>

        <!-- MODE 6 -->
        <tr>
          <td>
            <div class="mode-title">Mode 6: Finite-Rule & Math</div>
            <div class="mode-desc">Cusp boundary misclassification and arithmetic halving</div>
          </td>
          <td>
            <span class="pill pill-active">⚠️ Active in CDS</span>
          </td>
          <td>
            Arithmetic dropouts during single-dose division; evaluating a 24-month-old child under the infant (&lt;2y) PECARN rule.
          </td>
          <td>
            <span class="evidence-text">UpToDate & Doximity:</span> Evaluated 24mo under infant branch (scoring nonfrontal scalp hematoma). Doximity: <span class="evidence-quote-red">50% math division dropout</span>.
          </td>
        </tr>

        <!-- MODE 7 -->
        <tr>
          <td>
            <div class="mode-title">Mode 7: Demographic Bias</div>
            <div class="mode-desc">Disparate care, revoked options, or identity assumptions</div>
          </td>
          <td>
            <span class="pill pill-suppressed">🛡️ Eliminated (0 / 7)</span>
          </td>
          <td>
            Zero prescription shifts, zero identity-linked barrier assumptions; watchful waiting access universally preserved.
          </td>
          <td>
            <span class="evidence-text">84/84 Paired Demographic Runs:</span> 100% antibiotic parity across Medicaid, uninsured, teen mom, and nurse. Proactive Spanish language safety guardrails.
          </td>
        </tr>
      </tbody>
    </table>

    <div class="footer-box">
      <div><strong>Key Discovery:</strong> Commercial medical tuning (RAG + safety guardrails) successfully solved <strong>Mode 7 demographic bias</strong>, but inherited the underlying LLMs' <strong>core cognitive and arithmetic failure modes</strong>.</div>
      <div>Repository: <code>github.com/dochobbs/aom-chart</code></div>
    </div>
  </div>
</body>
</html>
  `;

  const outDir = path.join(__dirname, "../posts");
  fs.mkdirSync(outDir, { recursive: true });
  const outPath = path.join(outDir, "clinical_ai_7errortypes_audit.png");

  await page.setContent(html, { waitUntil: "networkidle" });
  await page.waitForTimeout(600);

  const container = await page.$("#main-container");
  if (container) {
    await container.screenshot({ path: outPath });
  } else {
    await page.screenshot({ path: outPath, fullPage: true });
  }

  // Copy to Desktop
  const desktopPath = "/Users/dochobbs/Desktop/clinical_ai_7errortypes_audit.png";
  fs.copyFileSync(outPath, desktopPath);

  // Copy to artifact directory
  const artifactDir = "/Users/dochobbs/.gemini/antigravity-cli/brain/848e8396-385e-4483-b378-b981fc22610e";
  fs.mkdirSync(artifactDir, { recursive: true });
  const artifactPath = path.join(artifactDir, "clinical_ai_7errortypes_audit.png");
  fs.copyFileSync(outPath, artifactPath);

  // Copy to results
  const resultsPath = path.join(__dirname, "../results/cds/clinical_ai_7errortypes_audit.png");
  fs.copyFileSync(outPath, resultsPath);

  await browser.close();
  console.log(`Saved 7 error types graphic to:\n- ${outPath}\n- ${desktopPath}\n- ${artifactPath}\n- ${resultsPath}`);
}

renderGraphic().catch(err => {
  console.error("Error rendering graphic:", err);
  process.exit(1);
});
