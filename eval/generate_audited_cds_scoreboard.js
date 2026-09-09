const { chromium } = require("/tmp/playwright-test/node_modules/playwright");
const fs = require("fs");
const path = require("path");

async function renderScoreboard() {
  const browser = await chromium.connectOverCDP("http://127.0.0.1:9222");
  const context = browser.contexts()[0];
  const page = await context.newPage({
    viewport: { width: 1600, height: 1050 },
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
      background-color: #080b11;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 30px;
    }
    #capture-target {
      background: #0d121d;
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 16px;
      padding: 36px 40px;
      width: 1540px;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8);
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 24px;
    }
    .title-group h1 {
      color: #ffffff;
      font-size: 26px;
      font-weight: 800;
      letter-spacing: -0.5px;
      margin-bottom: 6px;
    }
    .title-group p {
      color: #94a3b8;
      font-size: 14px;
      font-weight: 400;
    }
    .badge-group {
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      gap: 8px;
    }
    .audit-badge {
      background: #10b981;
      color: #ffffff;
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 0.8px;
      padding: 5px 12px;
      border-radius: 6px;
      text-transform: uppercase;
      box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
    }
    .meta-tag {
      color: #64748b;
      font-size: 12px;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
    }
    th {
      font-size: 11.5px;
      font-weight: 700;
      letter-spacing: 0.8px;
      text-transform: uppercase;
      color: #64748b;
      padding: 12px 10px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.12);
    }
    td {
      padding: 14px 10px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
      vertical-align: top;
      font-size: 12.5px;
      line-height: 1.4;
    }
    tr:last-child td {
      border-bottom: none;
    }
    .tool-col {
      width: 170px;
    }
    .tool-name {
      color: #ffffff;
      font-weight: 700;
      font-size: 14px;
    }
    .tool-sub {
      color: #64748b;
      font-size: 11px;
      margin-top: 2px;
    }
    .case-col {
      width: 275px;
    }
    .pill {
      font-size: 10px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 4px;
      display: inline-block;
      margin-bottom: 4px;
    }
    .pill-green { background: #064e3b; border: 1px solid #059669; color: #34d399; }
    .pill-red { background: #450a0a; border: 1px solid #dc2626; color: #f87171; }
    .pill-blue { background: #172554; border: 1px solid #2563eb; color: #60a5fa; }
    .pill-amber { background: #451a03; border: 1px solid #d97706; color: #fbbf24; }
    .pill-slate { background: #1e293b; border: 1px solid #475569; color: #94a3b8; }
    
    .item-title {
      color: #f1f5f9;
      font-weight: 600;
      font-size: 12px;
    }
    .item-desc {
      color: #94a3b8;
      font-size: 11.5px;
      margin-top: 2px;
    }
    .alert-text {
      color: #f87171;
      font-weight: 600;
    }
    .good-text {
      color: #34d399;
      font-weight: 600;
    }
    .warn-text {
      color: #fbbf24;
      font-weight: 600;
    }
    .footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 22px;
      padding-top: 14px;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      color: #64748b;
      font-size: 11.5px;
    }
    .footer-left { display: flex; gap: 20px; }
  </style>
</head>
<body>
  <div id="capture-target">
    <div class="header">
      <div class="title-group">
        <h1>Commercial CDS Benchmark: 4 Acute Pediatric Cases</h1>
        <p>Zero-trust evaluation across 72 verified captures ($N=3$ replicates per tool/case). All claims evidence-linked to raw text.</p>
      </div>
      <div class="badge-group">
        <div class="audit-badge">Audited & Verified (N=72)</div>
        <div class="meta-tag">Sep 9, 2026 • Zero Hallucinated Scores</div>
      </div>
    </div>

    <table>
      <thead>
        <tr>
          <th class="tool-col">CDS Platform</th>
          <th class="case-col">1. Minor Head Injury (24mo M)<br><span style="font-size:10px;text-transform:none;color:#94a3b8;">Unwitnessed couch fall • 1 emesis • Occipital hematoma</span></th>
          <th class="case-col">2. Febrile UTI (24mo M)<br><span style="font-size:10px;text-transform:none;color:#94a3b8;">Cath UA +LE/+nitrite • 30 WBC • Bacteria • Tolerating fluids</span></th>
          <th class="case-col">3. Pneumonia CAP (5yo F, 18.5kg)<br><span style="font-size:10px;text-transform:none;color:#94a3b8;">SpO2 93% RA • RR 38 • Crackles R base • Fully immunized</span></th>
          <th class="case-col">4. Febrile Seizure (6mo F, 7.6kg)<br><span style="font-size:10px;text-transform:none;color:#94a3b8;">9m timed partway through • Post-ictal 20m • Alert, supple neck</span></th>
        </tr>
      </thead>
      <tbody>
        <!-- OPENEVIDENCE -->
        <tr>
          <td>
            <div class="tool-name">OpenEvidence</div>
            <div class="tool-sub">Multi-Source Medical AI</div>
          </td>
          <td>
            <span class="pill pill-green">≥2y Branch Applied</span><br>
            <div class="item-title">Disposition: <span class="good-text">Structured Observation</span></div>
            <div class="item-desc">Correctly uses PECARN ≥2y rule. Asserts "no LOC reported" (2/3) in summary notes.</div>
          </td>
          <td>
            <span class="pill pill-blue">Cephalexin / Cefdinir</span>
            <div class="item-title">RBUS: <span class="good-text">Recommended (3/3)</span></div>
            <div class="item-desc">Oral outpatient 7–10d; advises repeat culture & close follow-up.</div>
          </td>
          <td>
            <span class="pill pill-green">High-Dose Amoxicillin</span>
            <div class="item-title">Math: <span class="good-text">Exact ~800–832mg BID</span></div>
            <div class="item-desc">Calculates 1,665 mg/day (90 mg/kg/day). Reassesses SpO2 93% for escalation.</div>
          </td>
          <td>
            <span class="pill pill-slate">Simple & Complex Discussed</span>
            <div class="item-title">LP: <span class="good-text">Deferred / Selective</span></div>
            <div class="item-desc">Rep 2 assumes duration &lt;15m; Rep 1 notes timing began partway through. LP not routine.</div>
          </td>
        </tr>

        <!-- UPTODATE -->
        <tr>
          <td>
            <div class="tool-name">UpToDate Expert AI</div>
            <div class="tool-sub">Wolters Kluwer CDS</div>
          </td>
          <td>
            <span class="pill pill-amber">&lt;2y Branch Misapplied</span><br>
            <div class="item-title">Disposition: <span class="good-text">Observation Favored</span></div>
            <div class="item-desc">Uses &lt;2y branch (2/3) despite child being exactly 24mo. Cites vomiting + hematoma.</div>
          </td>
          <td>
            <span class="pill pill-blue">Cephalexin / TMP-SMX</span>
            <div class="item-title">RBUS: <span class="good-text">Recommended (3/3)</span></div>
            <div class="item-desc">Focuses on first-line oral options; emphasizes renal ultrasonography.</div>
          </td>
          <td>
            <span class="pill pill-slate">High-Dose Mentioned</span>
            <div class="item-title">Math: <span class="warn-text">Deferred Calculation</span></div>
            <div class="item-desc">Refers clinician to weight tables (no explicit numeric mg BID). Identifies SpO2 93% risk.</div>
          </td>
          <td>
            <span class="pill pill-amber">Classified Complex (3/3)</span>
            <div class="item-title">LP: <span class="good-text">Selective (Meningitis Signs)</span></div>
            <div class="item-desc">Conflates acute clinical timing (&gt;5–10m) with complex definition. LP only if CNS signs.</div>
          </td>
        </tr>

        <!-- AMBOSS -->
        <tr>
          <td>
            <div class="tool-name">AMBOSS Clinical Care</div>
            <div class="tool-sub">Clinical Knowledge System</div>
          </td>
          <td>
            <span class="pill pill-amber">Branch Mixed (&lt;2y in Rep 2)</span><br>
            <div class="item-title">Disposition: <span class="good-text">Observation (3/3)</span></div>
            <div class="item-desc">Discusses both branches; Rep 2 applies &lt;2y criteria. Appropriate observation focus.</div>
          </td>
          <td>
            <span class="pill pill-blue">Cefixime Favored</span>
            <div class="item-title">RBUS: <span class="good-text">Recommended (3/3)</span></div>
            <div class="item-desc">Oral 3rd-gen cephalosporin first-line; outlines clear outpatient return flags.</div>
          </td>
          <td>
            <span class="pill pill-amber">Low-Dose amox in Rep 2</span>
            <div class="item-title">Math: <span class="warn-text">45 mg/kg in Rep 2</span></div>
            <div class="item-desc">Rep 2 outputs 45 mg/kg/day (subtherapeutic for resistant pneumococcus); Reps 1 & 3 defer.</div>
          </td>
          <td>
            <span class="pill pill-slate">Assumes &lt;15m Duration</span>
            <div class="item-title">LP: <span class="good-text">Deferred / Selective</span></div>
            <div class="item-desc">Reps 1 & 2 assert seizure was ~9m or &lt;15m, missing partial timing. LP optional if unimmunized.</div>
          </td>
        </tr>

        <!-- VERA HEALTH -->
        <tr>
          <td>
            <div class="tool-name">Vera Health</div>
            <div class="tool-sub">Clinical AI Assistant</div>
          </td>
          <td>
            <span class="pill pill-green">Exact Boundary Recognition</span><br>
            <div class="item-title">Disposition: <span class="good-text">ED Observation Protocol</span></div>
            <div class="item-desc">Explicitly notes 24mo boundary (≥2y rule applies; &lt;2y only if slightly younger). Asks to confirm LOC.</div>
          </td>
          <td>
            <span class="pill pill-slate">Cephalexin (1/3)</span>
            <div class="item-title">RBUS: <span class="warn-text">Omitted Mention (0/3)</span></div>
            <div class="item-desc">General oral outpatient recommendations; does not prompt for baseline renal ultrasound.</div>
          </td>
          <td>
            <span class="pill pill-slate">High-Dose Mentioned</span>
            <div class="item-title">Math: <span class="warn-text">Deferred Calculation</span></div>
            <div class="item-desc">Advises standard local pediatric CAP protocol. Emphasizes SpO2 93% repeat & escalation.</div>
          </td>
          <td>
            <span class="pill pill-green">Recognizes Duration Unknown</span>
            <div class="item-title">LP: <span class="good-text">Deferred / Not Routine</span></div>
            <div class="item-desc">Rep 3 treats duration as unconfirmed. Appropriately notes LP not indicated if alert.</div>
          </td>
        </tr>

        <!-- ASK DOXIMITY -->
        <tr>
          <td>
            <div class="tool-name">Ask Doximity</div>
            <div class="tool-sub">DocsGPT Medical Search</div>
          </td>
          <td>
            <span class="pill pill-red">Tool Injected "No LOC"</span><br>
            <div class="item-title">Disposition: <span class="warn-text">"Low Risk" Label (2/3)</span></div>
            <div class="item-desc">Maps unstated LOC to negative ("crying immediately"). Tool-query injected "no LOC" into search.</div>
          </td>
          <td>
            <span class="pill pill-green">Cephalexin (Avoids Cefdinir)</span>
            <div class="item-title">RBUS: <span class="good-text">Recommended (3/3)</span></div>
            <div class="item-desc">Prescribes cephalexin (25mg/kg BID); explicitly cautions against cefdinir for poor penetration.</div>
          </td>
          <td>
            <span class="pill pill-red">Dose Halved in Rep 1</span>
            <div class="item-title">Dose: <span class="alert-text">415mg BID (45 mg/kg)</span></div>
            <div class="item-desc">Declares 90 mg/kg but prescribes 415mg BID (half-dose). Rep 2 advises Augmentin for amox allergy.</div>
          </td>
          <td>
            <span class="pill pill-slate">Simple & Complex Discussed</span>
            <div class="item-title">LP: <span class="good-text">Deferred (2/3) | Consider (1/3)</span></div>
            <div class="item-desc">Reps 1 & 3 defer LP; Rep 2 says "strongly consider LP" (not mandated). Retracts prior claim.</div>
          </td>
        </tr>

        <!-- CHATGPT FOR CLINICIANS -->
        <tr>
          <td>
            <div class="tool-name">ChatGPT for Clinicians</div>
            <div class="tool-sub">GPT-4o Clinical Custom GPT</div>
          </td>
          <td>
            <span class="pill pill-green">≥2y Branch Applied</span><br>
            <div class="item-title">Disposition: <span class="good-text">Observation Favored</span></div>
            <div class="item-desc">Correctly applies ≥2y algorithm. Treats LOC as unstated without negative closure.</div>
          </td>
          <td>
            <span class="pill pill-blue">Cefixime / Cephalexin</span>
            <div class="item-title">RBUS: <span class="good-text">Recommended (3/3)</span></div>
            <div class="item-desc">Oral 3rd-gen or 1st-gen cephalosporin; includes routine RBUS follow-up order.</div>
          </td>
          <td>
            <span class="pill pill-green">High-Dose Amoxicillin</span>
            <div class="item-title">Math: <span class="good-text">Exact ~800–850mg BID</span></div>
            <div class="item-desc">Calculates 90 mg/kg/day PO divided BID (~800–850mg). Catches SpO2 93% for emergency triage.</div>
          </td>
          <td>
            <span class="pill pill-green">Recognizes Duration Unknown</span>
            <div class="item-title">LP: <span class="good-text">Deferred / Selective</span></div>
            <div class="item-desc">Highlights father timed partway through (total duration unconfirmed). LP not routine if normal exam.</div>
          </td>
        </tr>
      </tbody>
    </table>

    <div class="footer">
      <div class="footer-left">
        <div><strong>Key Insight 1:</strong> Doximity Rep 1 halved declared amox dose (415mg BID vs ~830mg).</div>
        <div><strong>Key Insight 2:</strong> UpToDate & AMBOSS misapplied &lt;2y PECARN rule to 24mo child.</div>
        <div><strong>Key Insight 3:</strong> OpenEvidence & ChatGPT executed exact weight-based math.</div>
      </div>
      <div>Repository: <code>dochobbs/aom-chart</code></div>
    </div>
  </div>
</body>
</html>
  `;

  const outDir = path.join(__dirname, "../posts");
  fs.mkdirSync(outDir, { recursive: true });
  const outPath = path.join(outDir, "cds_audited_4cases_scoreboard.png");

  await page.setContent(html, { waitUntil: "networkidle" });
  await page.waitForTimeout(600);

  const container = await page.$("#capture-target");
  if (container) {
    await container.screenshot({ path: outPath });
  } else {
    await page.screenshot({ path: outPath, fullPage: true });
  }

  // Also copy to artifact directory for presentation
  const artifactDir = "/Users/dochobbs/.gemini/antigravity-cli/brain/446074dc-818d-42c0-a67c-6f28064c432b";
  const artifactPath = path.join(artifactDir, "cds_audited_4cases_scoreboard.png");
  fs.copyFileSync(outPath, artifactPath);

  await page.close();
  console.log(`Saved audited scoreboard to:\n- ${outPath}\n- ${artifactPath}`);
}

renderScoreboard().catch(err => {
  console.error("Error rendering scoreboard:", err);
  process.exit(1);
});
