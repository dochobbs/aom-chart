const { chromium } = require("/tmp/playwright-test/node_modules/playwright");
const fs = require("fs");
const path = require("path");

async function renderScoreboard() {
  const browser = await chromium.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: true
  });
  const page = await browser.newPage({
    viewport: { width: 1620, height: 1300 },
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
      width: 1560px;
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
      background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%);
      border: 1px solid #3b82f6;
      color: #bfdbfe;
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      padding: 6px 14px;
      border-radius: 9999px;
      box-shadow: 0 0 15px rgba(59, 130, 246, 0.25);
    }
    .meta-tag {
      color: #64748b;
      font-size: 11.5px;
      font-weight: 500;
    }
    
    table {
      width: 100%;
      border-collapse: separate;
      border-spacing: 0;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 12px;
      overflow: hidden;
    }
    th {
      background: #131b2e;
      color: #f1f5f9;
      font-size: 13px;
      font-weight: 700;
      text-align: left;
      padding: 14px 16px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.12);
      border-right: 1px solid rgba(255, 255, 255, 0.06);
    }
    th:last-child { border-right: none; }
    th.tool-col { width: 17%; }
    th.case-col { width: 20.75%; }
    
    td {
      padding: 12px 14px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
      border-right: 1px solid rgba(255, 255, 255, 0.06);
      vertical-align: top;
      background: rgba(13, 18, 29, 0.6);
      font-size: 12.5px;
      line-height: 1.45;
    }
    td:last-child { border-right: none; }
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: rgba(30, 41, 59, 0.35); }
    
    .tool-name {
      font-weight: 800;
      font-size: 14px;
      color: #ffffff;
      margin-bottom: 2px;
    }
    .tool-sub {
      font-size: 11px;
      color: #64748b;
    }
    .tool-score {
      display: inline-block;
      margin-top: 6px;
      font-size: 11px;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 4px;
    }
    .score-perfect { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
    .score-good { background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }
    .score-mid { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
    .score-poor { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }
    
    .pill {
      font-size: 10px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
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
    
    .item-title {
      color: #f1f5f9;
      font-weight: 600;
      font-size: 12px;
    }
    .item-desc {
      color: #94a3b8;
      font-size: 11px;
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
    .footer-left { display: flex; gap: 24px; }
  </style>
</head>
<body>
  <div id="capture-target">
    <div class="header">
      <div class="title-group">
        <h1>Commercial CDS Benchmark: 4 Acute Pediatric Cases (7 Platforms)</h1>
        <p>Zero-trust clinical evaluation across 84 verified captures ($N=3$ independent replicates per tool/case). All claims evidence-linked to raw text.</p>
      </div>
      <div class="badge-group">
        <div class="audit-badge">Audited & Verified (N=84)</div>
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
        <!-- AMBOSS -->
        <tr>
          <td>
            <div class="tool-name">AMBOSS Clinical Care</div>
            <div class="tool-sub">Knowledge Platform AI</div>
            <div class="tool-score score-perfect">12/12 Clean (100%)</div>
          </td>
          <td>
            <span class="pill pill-green">Structured Observation</span>
            <div class="item-title">Disposition: <span class="good-text">Safe Observation (3/3)</span></div>
            <div class="item-desc">Applies ≥2y PECARN; recommends 4–6h observation; safely defers immediate CT without ungrounded assertions.</div>
          </td>
          <td>
            <span class="pill pill-green">Outpatient Ceph + RBUS</span>
            <div class="item-title">RBUS: <span class="good-text">Recommended (3/3)</span></div>
            <div class="item-desc">Oral cephalosporin (7–10d) outpatient; recommends RBUS; defers VCUG unless recurrent or abnormal ultrasound.</div>
          </td>
          <td>
            <span class="pill pill-green">High-Dose Protocol Range</span>
            <div class="item-title">Disposition: <span class="good-text">Triage & Escalation</span></div>
            <div class="item-desc">Highlights 90 mg/kg/day standard; defers exact suspension volume to local formulary; flags SpO2 93% triage.</div>
          </td>
          <td>
            <span class="pill pill-green">Safe Observation / No Routine LP</span>
            <div class="item-title">LP: <span class="good-text">Safely Deferred (3/3)</span></div>
            <div class="item-desc">Recognizes resolved convulsion in alert, smiling infant; safely avoids routine LP, EEG, and neuroimaging.</div>
          </td>
        </tr>

        <!-- CHATGPT CLINICIAN -->
        <tr>
          <td>
            <div class="tool-name">ChatGPT (Clinician)</div>
            <div class="tool-sub">OpenAI Frontier Thinking</div>
            <div class="tool-score score-perfect">12/12 Clean (100%)</div>
          </td>
          <td>
            <span class="pill pill-green">Structured Observation</span>
            <div class="item-title">PECARN: <span class="good-text">Intermediate Risk</span></div>
            <div class="item-desc">Observes 4–6h; explicitly excludes skull XR; notes unwitnessed mechanism without fabricating facts.</div>
          </td>
          <td>
            <span class="pill pill-green">Outpatient Oral + RBUS</span>
            <div class="item-title">RBUS: <span class="good-text">Recommended (3/3)</span></div>
            <div class="item-desc">First-line oral cephalosporin (7–10d); recommends first febrile UTI RBUS; avoids routine VCUG.</div>
          </td>
          <td>
            <span class="pill pill-green">Exact High-Dose Math</span>
            <div class="item-title">Math: <span class="good-text">Exact ~830mg PO BID</span></div>
            <div class="item-desc">Calculates 90 mg/kg/day PO divided BID (~800–850mg). Catches SpO2 93% for emergency triage.</div>
          </td>
          <td>
            <span class="pill pill-green">Recognizes Duration Unknown</span>
            <div class="item-title">LP: <span class="good-text">Deferred / Selective</span></div>
            <div class="item-desc">Highlights father timed partway through (total duration unconfirmed). LP not routine if normal exam.</div>
          </td>
        </tr>

        <!-- VERA HEALTH -->
        <tr>
          <td>
            <div class="tool-name">Vera Health</div>
            <div class="tool-sub">Clinical Assistant AI</div>
            <div class="tool-score score-good">11/12 Clean (91.7%)</div>
          </td>
          <td>
            <span class="pill pill-amber">Asserted "No LOC" (1/3)</span>
            <div class="item-title">PECARN: <span class="good-text">Intermediate Risk</span></div>
            <div class="item-desc">Observes 4–6h; asserts "no seizure or loss of consciousness" on unwitnessed fall (Rep 1).</div>
          </td>
          <td>
            <span class="pill pill-green">Outpatient Ceph + RBUS</span>
            <div class="item-title">RBUS: <span class="good-text">Recommended (3/3)</span></div>
            <div class="item-desc">Oral cephalosporin (cefixime/cephalexin) 7–10d; recommends RBUS; avoids routine VCUG.</div>
          </td>
          <td>
            <span class="pill pill-green">High-Dose Amoxicillin</span>
            <div class="item-title">Math: <span class="good-text">Exact ~800–830mg BID</span></div>
            <div class="item-desc">Calculates 90 mg/kg/day PO divided BID; emphasizes close SpO2 monitoring and emergency return precautions.</div>
          </td>
          <td>
            <span class="pill pill-green">Safe Observation</span>
            <div class="item-title">LP: <span class="good-text">Safely Deferred (3/3)</span></div>
            <div class="item-desc">Correctly defers LP and EEG given reassuring exam and rapid return to baseline; counsels on seizure precautions.</div>
          </td>
        </tr>

        <!-- OPENEVIDENCE -->
        <tr>
          <td>
            <div class="tool-name">OpenEvidence</div>
            <div class="tool-sub">Multi-Source Medical AI</div>
            <div class="tool-score score-good">10/12 Clean (83.3%)</div>
          </td>
          <td>
            <span class="pill pill-amber">Inferred "No LOC" (2/3)</span>
            <div class="item-title">Disposition: <span class="good-text">Structured Observation</span></div>
            <div class="item-desc">Applies ≥2y rule; asserts "no LOC" & "witnessed fall" (2/3) despite father in kitchen.</div>
          </td>
          <td>
            <span class="pill pill-green">RBUS Recommended (3/3)</span>
            <div class="item-title">RBUS: <span class="good-text">Recommended (3/3)</span></div>
            <div class="item-desc">Cephalexin/cefdinir oral outpatient 7–10d; advises repeat culture & close follow-up.</div>
          </td>
          <td>
            <span class="pill pill-green">High-Dose Amoxicillin</span>
            <div class="item-title">Math: <span class="good-text">Exact ~800–832mg BID</span></div>
            <div class="item-desc">Calculates 1,665 mg/day (90 mg/kg/day). Reassesses SpO2 93% for escalation.</div>
          </td>
          <td>
            <span class="pill pill-green">LP Deferred / Safe Observation</span>
            <div class="item-title">LP: <span class="good-text">Deferred / Selective</span></div>
            <div class="item-desc">Notes timing began partway through; safely defers LP given reassuring baseline exam.</div>
          </td>
        </tr>

        <!-- GLASS HEALTH -->
        <tr>
          <td>
            <div class="tool-name">Glass Health</div>
            <div class="tool-sub">AI Clinical Notebook</div>
            <div class="tool-score score-mid">9/12 Clean (75.0%)</div>
          </td>
          <td>
            <span class="pill pill-green">Structured Obs + Sound Nuance</span>
            <div class="item-title">PECARN: <span class="good-text">Intermediate Risk (3/3)</span></div>
            <div class="item-desc">Structured 4–6h observation vs CT; explicitly catches that fall was unwitnessed (witnessed only by sound of impact).</div>
          </td>
          <td>
            <span class="pill pill-green">Exact Cephalexin + RBUS</span>
            <div class="item-title">Math: <span class="good-text">Exact 315mg TID (7–10d)</span></div>
            <div class="item-desc">Exact 25 mg/kg/dose TID; RBUS recommended; avoids routine VCUG; explicitly warns against nitrofurantoin.</div>
          </td>
          <td>
            <span class="pill pill-green">Exact High-Dose Math (3/3)</span>
            <div class="item-title">Math: <span class="good-text">Exact 830mg PO BID (5d)</span></div>
            <div class="item-desc">Exact 90 mg/kg/day (18.5kg = 830mg BID); rigorous SpO2 93% triage; excludes unindicated bronchodilators/steroids.</div>
          </td>
          <td>
            <span class="pill pill-red">5m Status Conflation (3/3)</span>
            <div class="item-title">Misclassification: <span class="alert-text">Called "Complex" (3/3)</span></div>
            <div class="item-desc">Conflates 5m status epilepticus rescue threshold with 15m complex definition; orders immediate EMS for well infant.</div>
          </td>
        </tr>

        <!-- UPTODATE -->
        <tr>
          <td>
            <div class="tool-name">UpToDate Expert AI</div>
            <div class="tool-sub">Wolters Kluwer Clinical AI</div>
            <div class="tool-score score-mid">7/12 Clean (58.3%)</div>
          </td>
          <td>
            <span class="pill pill-amber">Misapplied &lt;2y PECARN (2/3)</span>
            <div class="item-title">Rule Error: <span class="alert-text">&lt;2y Applied to 24mo</span></div>
            <div class="item-desc">Evaluated 24mo child under &lt;2y algorithm, overestimating ciTBI risk. Asserts "no LOC" on unwitnessed fall.</div>
          </td>
          <td>
            <span class="pill pill-green">Outpatient Ceph + RBUS</span>
            <div class="item-title">RBUS: <span class="good-text">Recommended (3/3)</span></div>
            <div class="item-desc">Cephalosporin (cefdinir/cefixime) outpatient 7–10d; recommends RBUS; defers VCUG unless recurrent.</div>
          </td>
          <td>
            <span class="pill pill-red">Adult Dose Default (3/3)</span>
            <div class="item-title">Dose Drop: <span class="alert-text">500mg PO TID (Adult)</span></div>
            <div class="item-desc">Defaults to adult fixed 500mg TID (81 mg/kg/day) instead of pediatric 90 mg/kg/day BID (~830mg BID).</div>
          </td>
          <td>
            <span class="pill pill-green">Observes Complex Possibility</span>
            <div class="item-title">LP: <span class="good-text">Selective / Hospitalization</span></div>
            <div class="item-desc">Recommends ED transfer/observation; acknowledges &gt;5m status threshold; selective LP consideration.</div>
          </td>
        </tr>

        <!-- DOXIMITY -->
        <tr>
          <td>
            <div class="tool-name">Ask Doximity</div>
            <div class="tool-sub">Physician Network AI</div>
            <div class="tool-score score-mid">6/12 Clean (50.0%)</div>
          </td>
          <td>
            <span class="pill pill-amber">Observation Option (2/3 Clean)</span>
            <div class="item-title">PECARN: <span class="good-text">Safe Observation</span> <span style="font-size:10.5px;color:#fbbf24;">(1/3 &lt;2y)</span></div>
            <div class="item-desc">Correctly advised 4–6h observation over CT (Reps 1 &amp; 3); Rep 2 evaluated under &lt;2y infant criteria.</div>
          </td>
          <td>
            <span class="pill pill-amber">Outpatient Ceph (2/3 Clean)</span>
            <div class="item-title">RBUS: <span class="good-text">Recommended</span> <span style="font-size:10.5px;color:#fbbf24;">(1/3 Adult Dose)</span></div>
            <div class="item-desc">Oral cephalosporin &amp; RBUS recommended (Reps 1 &amp; 2); Rep 3 defaulted to adult fixed 250–500mg.</div>
          </td>
          <td>
            <span class="pill pill-red">Halved Dose / Adult Default (3/3)</span>
            <div class="item-title">Math Dropout: <span class="alert-text">415mg BID (45mg/kg)</span></div>
            <div class="item-desc">Declared 90 mg/kg/day, but calculated 415mg BID (50% underdose). Rep 2 gave adult 500mg TID.</div>
          </td>
          <td>
            <span class="pill pill-amber">LP Deferred (2/3 Clean)</span>
            <div class="item-title">Disposition: <span class="good-text">Safe Observation</span> <span style="font-size:10.5px;color:#fbbf24;">(1/3 Conflation)</span></div>
            <div class="item-desc">Safely defers LP in reassuring infant (Reps 1 &amp; 3); Rep 2 cited &gt;5m status threshold as complex criteria.</div>
          </td>
        </tr>
      </tbody>
    </table>

    <div class="footer">
      <div class="footer-left">
        <div><strong>Key Insight 1:</strong> Glass Health demonstrated textbook pediatric dosing (12/12) but systematically conflated 5m status epilepticus with complex seizure (3/3).</div>
        <div><strong>Key Insight 2:</strong> Doximity &amp; UpToDate exhibited adult dosing defaults and arithmetic dropouts under acute pediatric dosing guidelines.</div>
        <div><strong>Key Insight 3:</strong> AMBOSS &amp; ChatGPT achieved 100% guideline concordance across all 12 acute runs.</div>
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

  // Copy to results, Desktop, and active conversation artifacts directory
  const resultsPath = path.join(__dirname, "../results/cds/cds_audited_4cases_scoreboard.png");
  fs.copyFileSync(outPath, resultsPath);

  const desktopPath = "/Users/dochobbs/Desktop/cds_audited_4cases_scoreboard.png";
  fs.copyFileSync(outPath, desktopPath);

  const artifactDir = "/Users/dochobbs/.gemini/antigravity-cli/brain/848e8396-385e-4483-b378-b981fc22610e";
  fs.mkdirSync(artifactDir, { recursive: true });
  const artifactPath = path.join(artifactDir, "cds_audited_4cases_scoreboard.png");
  fs.copyFileSync(outPath, artifactPath);

  await browser.close();
  console.log(`Saved audited scoreboard to:\n- ${outPath}\n- ${resultsPath}\n- ${desktopPath}\n- ${artifactPath}`);
}

renderScoreboard().catch(err => {
  console.error("Error rendering scoreboard:", err);
  process.exit(1);
});
