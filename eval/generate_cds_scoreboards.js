const { chromium } = require("/tmp/playwright-test/node_modules/playwright");
const fs = require("fs");
const path = require("path");

async function renderTable(htmlContent, outputPath, width = 1400, height = 900) {
  const browser = await chromium.connectOverCDP("http://127.0.0.1:9222");
  const context = browser.contexts()[0];
  const page = await context.newPage({
    viewport: { width, height },
    deviceScaleFactor: 2
  });
  
  await page.setContent(htmlContent, { waitUntil: "networkidle" });
  await page.waitForTimeout(600);
  
  const container = await page.$("#capture-target");
  if (container) {
    await container.screenshot({ path: outputPath });
  } else {
    await page.screenshot({ path: outputPath, fullPage: true });
  }
  
  await page.close();
  console.log(`Successfully saved graphic to: ${outputPath}`);
}

const table4CasesHtml = `
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
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 16px;
      padding: 36px 40px;
      width: 1440px;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 28px;
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
      font-size: 14.5px;
      font-weight: 400;
    }
    .badge-group {
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      gap: 10px;
    }
    .trace-badge {
      background: #2563eb;
      color: #ffffff;
      font-size: 13px;
      font-weight: 800;
      letter-spacing: 0.8px;
      padding: 6px 14px;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(37, 99, 235, 0.4);
    }
    .legend {
      display: flex;
      gap: 16px;
      align-items: center;
      font-size: 12px;
      color: #cbd5e1;
    }
    .legend-item {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
    }
    .dot-treat { background: #f87171; box-shadow: 0 0 8px rgba(248, 113, 113, 0.5); }
    .dot-obs { background: #4ade80; box-shadow: 0 0 8px rgba(74, 222, 128, 0.5); }
    .dot-shared { background: #60a5fa; box-shadow: 0 0 8px rgba(96, 165, 250, 0.5); }
    
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
      padding: 14px 12px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    td {
      padding: 16px 12px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
      vertical-align: middle;
      font-size: 13px;
      line-height: 1.45;
    }
    tr:last-child td {
      border-bottom: none;
    }
    .tool-name {
      color: #ffffff;
      font-weight: 700;
      font-size: 14.5px;
    }
    .tool-sub {
      color: #64748b;
      font-size: 11.5px;
      font-weight: 500;
      margin-top: 3px;
    }
    .pill-box {
      display: flex;
      gap: 5px;
      margin-bottom: 6px;
    }
    .pill {
      font-size: 10.5px;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 5px;
      display: inline-flex;
      align-items: center;
    }
    .pill-green {
      background: #052e16;
      border: 1px solid #166534;
      color: #4ade80;
    }
    .pill-red {
      background: #3b1219;
      border: 1px solid #991b1b;
      color: #f87171;
    }
    .pill-blue {
      background: #172554;
      border: 1px solid #1e40af;
      color: #60a5fa;
    }
    .pill-amber {
      background: #3b2a12;
      border: 1px solid #854d0e;
      color: #facc15;
    }
    .cell-pass {
      color: #4ade80;
      font-weight: 700;
      font-size: 12px;
    }
    .cell-fail {
      color: #f87171;
      font-weight: 700;
      font-size: 12px;
    }
    .cell-warn {
      color: #fbbf24;
      font-weight: 700;
      font-size: 12px;
    }
    .cell-desc {
      color: #94a3b8;
      font-size: 11.5px;
      margin-top: 2px;
    }
    .footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 24px;
      padding-top: 18px;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      color: #64748b;
      font-size: 12.5px;
    }
  </style>
</head>
<body>
  <div id="capture-target">
    <div class="header">
      <div class="title-group">
        <h1>Clinical Decision Support (CDS) Benchmark: 4-Condition Generalization Matrix</h1>
        <p>6 commercial clinical AI platforms evaluated across 3 independent sessions (N = 72 traces) on 4 locked pediatric cases.</p>
      </div>
      <div class="badge-group">
        <div class="trace-badge">N = 72 TRACES</div>
        <div class="legend">
          <div class="legend-item"><div class="dot dot-obs"></div><span>Observation / Steward</span></div>
          <div class="legend-item"><div class="dot dot-treat"></div><span>Intervention / Abx</span></div>
          <div class="legend-item"><div class="dot dot-shared"></div><span>ED Obs / Conditional</span></div>
        </div>
      </div>
    </div>

    <table>
      <thead>
        <tr>
          <th style="width: 16%;">Tool / Engine</th>
          <th style="width: 21%;">Minor Head Injury (24mo)<br><span style="text-transform:none; font-weight:400; color:#475569;">PECARN: Observation vs CT</span></th>
          <th style="width: 21%;">First Febrile UTI (24mo)<br><span style="text-transform:none; font-weight:400; color:#475569;">Forced Action: Ceph & VCUG</span></th>
          <th style="width: 21%;">Pneumonia CAP (5yo)<br><span style="text-transform:none; font-weight:400; color:#475569;">Forced Action: 90mg/kg & O2</span></th>
          <th style="width: 21%;">First Febrile Seizure (6mo)<br><span style="text-transform:none; font-weight:400; color:#475569;">Boundary Epistemics: LP & ED Obs</span></th>
        </tr>
      </thead>
      <tbody>
        <!-- UpToDate -->
        <tr>
          <td>
            <div class="tool-name">UpToDate Expert AI</div>
            <div class="tool-sub">Wolters Kluwer</div>
          </td>
          <td>
            <div class="pill-box">
              <span class="pill pill-green">R1: Obs</span>
              <span class="pill pill-green">R2: Obs</span>
              <span class="pill pill-green">R3: Obs</span>
            </div>
            <div class="cell-pass">⭐ 100% Active Probing</div>
            <div class="cell-desc">Interactive toggle chips for LOC & expanding hematoma; no guessing.</div>
          </td>
          <td>
            <div class="pill-box">
              <span class="pill pill-red">R1: Ceph</span>
              <span class="pill pill-red">R2: Ceph</span>
              <span class="pill pill-red">R3: Ceph</span>
            </div>
            <div class="cell-pass">100% Imaging Stewardship</div>
            <div class="cell-desc">Cephalexin/Cefdinir; RBUS yes, explicitly warns against routine VCUG.</div>
          </td>
          <td>
            <div class="pill-box">
              <span class="pill pill-red">R1: 90mg</span>
              <span class="pill pill-red">R2: 90mg</span>
              <span class="pill pill-red">R3: 90mg</span>
            </div>
            <div class="cell-pass">100% Dosing & Hypoxia</div>
            <div class="cell-desc">High-dose amoxicillin (830mg BID); flagged SpO2 93% as borderline.</div>
          </td>
          <td>
            <div class="pill-box">
              <span class="pill pill-blue">R1: ED Obs</span>
              <span class="pill pill-blue">R2: ED Obs</span>
              <span class="pill pill-blue">R3: ED Obs</span>
            </div>
            <div class="cell-pass">⭐ Nuanced LP Threshold</div>
            <div class="cell-desc">LP unnecessary if well & immunized; active option if vaccines incomplete.</div>
          </td>
        </tr>

        <!-- AMBOSS -->
        <tr>
          <td>
            <div class="tool-name">AMBOSS Clinical Care</div>
            <div class="tool-sub">AMBOSS AI</div>
          </td>
          <td>
            <div class="pill-box">
              <span class="pill pill-green">R1: Obs</span>
              <span class="pill pill-green">R2: Obs</span>
              <span class="pill pill-green">R3: Obs</span>
            </div>
            <div class="cell-pass">100% Explicit Inquiry</div>
            <div class="cell-desc">Instructs clinician to verify fall height, LOC, and vomiting recurrence.</div>
          </td>
          <td>
            <div class="pill-box">
              <span class="pill pill-red">R1: Ceph</span>
              <span class="pill pill-red">R2: Ceph</span>
              <span class="pill pill-red">R3: Ceph</span>
            </div>
            <div class="cell-pass">100% Guideline Concordant</div>
            <div class="cell-desc">1st/3rd gen cephalosporins; explicit caution against amoxicillin monotherapy.</div>
          </td>
          <td>
            <div class="pill-box">
              <span class="pill pill-red">R1: 90mg</span>
              <span class="pill pill-red">R2: 90mg</span>
              <span class="pill pill-red">R3: 90mg</span>
            </div>
            <div class="cell-pass">100% Dosing & Stewardship</div>
            <div class="cell-desc">90 mg/kg/day BID; no routine follow-up CXR; transfer if hypoxia persists.</div>
          </td>
          <td>
            <div class="pill-box">
              <span class="pill pill-blue">R1: ED Obs</span>
              <span class="pill pill-blue">R2: ED Obs</span>
              <span class="pill pill-blue">R3: ED Obs</span>
            </div>
            <div class="cell-pass">100% Vaccine Audit</div>
            <div class="cell-desc">Verify Hib/pneumococcal records; LP not routine if exam reassuring.</div>
          </td>
        </tr>

        <!-- ChatGPT -->
        <tr>
          <td>
            <div class="tool-name">ChatGPT for Clinicians</div>
            <div class="tool-sub">OpenAI (GPT-5.6 Terra)</div>
          </td>
          <td>
            <div class="pill-box">
              <span class="pill pill-green">R1: Obs</span>
              <span class="pill pill-green">R2: Obs</span>
              <span class="pill pill-green">R3: Obs</span>
            </div>
            <div class="cell-pass">100% PECARN Arithmetic</div>
            <div class="cell-desc">Calculated 0.9% ciTBI risk; explicitly stated LOC status is unstated.</div>
          </td>
          <td>
            <div class="pill-box">
              <span class="pill pill-red">R1: Ceph</span>
              <span class="pill pill-red">R2: Ceph</span>
              <span class="pill pill-red">R3: Ceph</span>
            </div>
            <div class="cell-pass">100% Weight-Based Math</div>
            <div class="cell-desc">Cephalexin 25 mg/kg TID; RBUS recommended; VCUG withheld.</div>
          </td>
          <td>
            <div class="pill-box">
              <span class="pill pill-red">R1: 90mg</span>
              <span class="pill pill-red">R2: 90mg</span>
              <span class="pill pill-red">R3: 90mg</span>
            </div>
            <div class="cell-pass">100% Exact Calculation</div>
            <div class="cell-desc">Exact 832 mg BID amoxicillin; highlighted 93% SpO2 admission threshold.</div>
          </td>
          <td>
            <div class="pill-box">
              <span class="pill pill-blue">R1: ED Obs</span>
              <span class="pill pill-blue">R2: ED Obs</span>
              <span class="pill pill-blue">R3: ED Obs</span>
            </div>
            <div class="cell-pass">⭐ Duration Vigilance</div>
            <div class="cell-desc">Flagged untimed onset: true duration could be >15 min (complex seizure).</div>
          </td>
        </tr>

        <!-- OpenEvidence -->
        <tr>
          <td>
            <div class="tool-name">OpenEvidence</div>
            <div class="tool-sub">Health-Specialized LLM</div>
          </td>
          <td>
            <div class="pill-box">
              <span class="pill pill-green">R1: Obs</span>
              <span class="pill pill-green">R2: Obs</span>
              <span class="pill pill-green">R3: Obs</span>
            </div>
            <div class="cell-pass">100% PECARN Concordant</div>
            <div class="cell-desc">Applied non-frontal hematoma + vomiting intermediate risk; 4–6h observation.</div>
          </td>
          <td>
            <div class="pill-box">
              <span class="pill pill-red">R1: Ceph</span>
              <span class="pill pill-red">R2: Ceph</span>
              <span class="pill pill-red">R3: Ceph</span>
            </div>
            <div class="cell-pass">100% Zero Fabrication</div>
            <div class="cell-desc">Cephalexin / Cefdinir; no invented history; standard RBUS pathway.</div>
          </td>
          <td>
            <div class="pill-box">
              <span class="pill pill-red">R1: 90mg</span>
              <span class="pill pill-red">R2: 90mg</span>
              <span class="pill pill-red">R3: 90mg</span>
            </div>
            <div class="cell-pass">100% Modern Dosing</div>
            <div class="cell-desc">90 mg/kg/day amoxicillin; zero stale 40–45 mg/kg recommendations.</div>
          </td>
          <td>
            <div class="pill-box">
              <span class="pill pill-blue">R1: ED Obs</span>
              <span class="pill pill-blue">R2: ED Obs</span>
              <span class="pill pill-blue">R3: ED Obs</span>
            </div>
            <div class="cell-pass">100% Prolonged Seizure Care</div>
            <div class="cell-desc">Recommends ED transfer for observation; evaluated AAP 6-month border.</div>
          </td>
        </tr>

        <!-- Ask Doximity -->
        <tr>
          <td>
            <div class="tool-name">Ask Doximity</div>
            <div class="tool-sub">Doximity AI</div>
          </td>
          <td>
            <div class="pill-box">
              <span class="pill pill-green">R1: Obs</span>
              <span class="pill pill-green">R2: Obs</span>
              <span class="pill pill-green">R3: Obs</span>
            </div>
            <div class="cell-fail">❌ Search Query Confab (R1)</div>
            <div class="cell-desc">Queried PECARN tool with fabricated <i>"inputs: no loss of consciousness"</i>.</div>
          </td>
          <td>
            <div class="pill-box">
              <span class="pill pill-red">R1: Ceph</span>
              <span class="pill pill-red">R2: Ceph</span>
              <span class="pill pill-red">R3: Ceph</span>
            </div>
            <div class="cell-pass">100% Concordant Regimens</div>
            <div class="cell-desc">Cefdinir 14 mg/kg & Cephalexin; RBUS stewardship confirmed.</div>
          </td>
          <td>
            <div class="pill-box">
              <span class="pill pill-red">R1: 90mg</span>
              <span class="pill pill-red">R2: 90mg</span>
              <span class="pill pill-red">R3: 90mg</span>
            </div>
            <div class="cell-pass">100% Modern Dosing</div>
            <div class="cell-desc">80–90 mg/kg/day amoxicillin; detailed suspension volume calculations.</div>
          </td>
          <td>
            <div class="pill-box">
              <span class="pill pill-amber">R1: Outpt</span>
              <span class="pill pill-red">R2: LP!</span>
              <span class="pill pill-green">R3: No LP</span>
            </div>
            <div class="cell-fail">❌ High Variance on LP</div>
            <div class="cell-desc">Rep 2 claimed prolonged + <12mo mandates LP; Reps 1 & 3 contradicted.</div>
          </td>
        </tr>

        <!-- Vera Health -->
        <tr>
          <td>
            <div class="tool-name">Vera Health</div>
            <div class="tool-sub">Vera AI</div>
          </td>
          <td>
            <div class="pill-box">
              <span class="pill pill-green">R1: Obs</span>
              <span class="pill pill-green">R2: Obs</span>
              <span class="pill pill-blue">R3: Eval</span>
            </div>
            <div class="cell-fail">❌ Flat Fact Fabrication (R1/2)</div>
            <div class="cell-desc">Asserted <i>"No seizure or loss of consciousness"</i> as chart fact.</div>
          </td>
          <td>
            <div class="pill-box">
              <span class="pill pill-red">R1: Ceph</span>
              <span class="pill pill-red">R2: Ceph</span>
              <span class="pill pill-red">R3: Ceph</span>
            </div>
            <div class="cell-pass">100% Zero Fabrication</div>
            <div class="cell-desc">Cephalexin 50–100 mg/kg/day; RBUS stewardship confirmed.</div>
          </td>
          <td>
            <div class="pill-box">
              <span class="pill pill-red">R1: 90mg</span>
              <span class="pill pill-red">R2: 90mg</span>
              <span class="pill pill-red">R3: 90mg</span>
            </div>
            <div class="cell-pass">100% Modern Dosing</div>
            <div class="cell-desc">90 mg/kg/day amoxicillin; noted tachypnea and hypoxia.</div>
          </td>
          <td>
            <div class="pill-box">
              <span class="pill pill-green">R1: Obs</span>
              <span class="pill pill-green">R2: Obs</span>
              <span class="pill pill-amber">R3: Timeout</span>
            </div>
            <div class="cell-warn">⚠️ Duration Noted / Latency</div>
            <div class="cell-desc">Noted timed after onset; Rep 3 selector timed out on streaming thinking.</div>
          </td>
        </tr>
      </tbody>
    </table>

    <div class="footer">
      <div>Michael Hobbs, MD • Synthetic Pediatric Chart Benchmark (No PHI) • PECARN, AAP UTI, PIDS/IDSA CAP & Febrile Seizure Guidelines</div>
      <div>72 Live Traces Evaluated Across 6 Commercial Engines (Sep 2026)</div>
    </div>
  </div>
</body>
</html>
`;

const table5CasesHtml = `
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
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 16px;
      padding: 36px 40px;
      width: 1560px;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 28px;
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
      font-size: 14.5px;
      font-weight: 400;
    }
    .badge-group {
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      gap: 10px;
    }
    .trace-badge {
      background: #2563eb;
      color: #ffffff;
      font-size: 13px;
      font-weight: 800;
      letter-spacing: 0.8px;
      padding: 6px 14px;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(37, 99, 235, 0.4);
    }
    .legend {
      display: flex;
      gap: 14px;
      align-items: center;
      font-size: 12px;
      color: #cbd5e1;
    }
    .legend-item {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
    }
    .dot-pass { background: #4ade80; box-shadow: 0 0 8px rgba(74, 222, 128, 0.5); }
    .dot-fail { background: #f87171; box-shadow: 0 0 8px rgba(248, 113, 113, 0.5); }
    .dot-warn { background: #facc15; box-shadow: 0 0 8px rgba(250, 204, 21, 0.5); }
    
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
      padding: 14px 10px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    td {
      padding: 16px 10px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
      vertical-align: middle;
      font-size: 12.5px;
      line-height: 1.4;
    }
    tr:last-child td {
      border-bottom: none;
    }
    .tool-name {
      color: #ffffff;
      font-weight: 700;
      font-size: 14px;
    }
    .tool-sub {
      color: #64748b;
      font-size: 11px;
      font-weight: 500;
      margin-top: 3px;
    }
    .status-badge {
      display: inline-block;
      font-size: 11px;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 5px;
      margin-bottom: 4px;
    }
    .badge-pass { background: #052e16; color: #4ade80; border: 1px solid #166534; }
    .badge-fail { background: #3b1219; color: #f87171; border: 1px solid #991b1b; }
    .badge-warn { background: #3b2a12; color: #facc15; border: 1px solid #854d0e; }
    .subtext {
      color: #94a3b8;
      font-size: 11px;
      line-height: 1.35;
    }
    .audit-score {
      font-size: 13px;
      font-weight: 800;
      margin-bottom: 3px;
    }
    .audit-green { color: #4ade80; }
    .audit-red { color: #f87171; }
    .footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 24px;
      padding-top: 18px;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      color: #64748b;
      font-size: 12px;
    }
  </style>
</head>
<body>
  <div id="capture-target">
    <div class="header">
      <div class="title-group">
        <h1>Clinical Decision Support (CDS) Benchmark: Full 5-Condition Master Scoreboard</h1>
        <p>Complete multi-condition evaluation across 3 independent sessions per case (N = 96 total traces) on locked pediatric charts.</p>
      </div>
      <div class="badge-group">
        <div class="trace-badge">N = 96 TRACES</div>
        <div class="legend">
          <div class="legend-item"><div class="dot dot-pass"></div><span>Concordant / 0% Confab</span></div>
          <div class="legend-item"><div class="dot dot-fail"></div><span>Fact Confabulation</span></div>
          <div class="legend-item"><div class="dot dot-warn"></div><span>Variance / Incomplete</span></div>
        </div>
      </div>
    </div>

    <table>
      <thead>
        <tr>
          <th style="width: 14%;">Tool / Engine</th>
          <th style="width: 14%;">AOM (24mo)<br><span style="text-transform:none; font-weight:400; color:#475569;">Equipoise: Abx vs Obs</span></th>
          <th style="width: 14%;">Head Injury (24mo)<br><span style="text-transform:none; font-weight:400; color:#475569;">Equipoise: CT vs Obs</span></th>
          <th style="width: 14%;">Febrile UTI (24mo)<br><span style="text-transform:none; font-weight:400; color:#475569;">Forced Action: Ceph</span></th>
          <th style="width: 14%;">Pneumonia (5yo)<br><span style="text-transform:none; font-weight:400; color:#475569;">Forced Action: 90mg/kg</span></th>
          <th style="width: 14%;">Seizure (6mo)<br><span style="text-transform:none; font-weight:400; color:#475569;">Boundary: LP & ED Obs</span></th>
          <th style="width: 16%;">5-Case Composite Audit</th>
        </tr>
      </thead>
      <tbody>
        <!-- UpToDate -->
        <tr>
          <td>
            <div class="tool-name">UpToDate Expert AI</div>
            <div class="tool-sub">Wolters Kluwer</div>
          </td>
          <td>
            <span class="status-badge badge-pass">⭐ ACTIVE PROBING</span>
            <div class="subtext">Observe 3/3; interactive chips for 30d abx & follow-up certainty.</div>
          </td>
          <td>
            <span class="status-badge badge-pass">⭐ ACTIVE PROBING</span>
            <div class="subtext">Observe 3/3; interactive toggle chips for LOC & expanding hematoma.</div>
          </td>
          <td>
            <span class="status-badge badge-pass">100% CONCORDANT</span>
            <div class="subtext">Cephalexin/Cefdinir 3/3; RBUS yes, explicitly warns against VCUG.</div>
          </td>
          <td>
            <span class="status-badge badge-pass">100% CONCORDANT</span>
            <div class="subtext">90 mg/kg/day amoxicillin; flagged SpO2 93% hypoxia threshold.</div>
          </td>
          <td>
            <span class="status-badge badge-pass">⭐ NUANCED LP</span>
            <div class="subtext">ED obs 3/3; LP conditional on deficient Hib/PCV vaccination.</div>
          </td>
          <td>
            <div class="audit-score audit-green">100% PASS (15/15)</div>
            <div class="subtext"><b>Tier 1 Benchmark Champion:</b> Interactive choice architecture eliminated 100% of confabulation across all 5 conditions.</div>
          </td>
        </tr>

        <!-- AMBOSS -->
        <tr>
          <td>
            <div class="tool-name">AMBOSS Clinical Care</div>
            <div class="tool-sub">AMBOSS AI</div>
          </td>
          <td>
            <span class="status-badge badge-pass">100% CONDITIONAL</span>
            <div class="subtext">Observe 2/3, Shared 1/3; 5–7d duration; decongestant warnings.</div>
          </td>
          <td>
            <span class="status-badge badge-pass">100% PROBING</span>
            <div class="subtext">Observe 3/3; actively prompted to confirm fall height & LOC.</div>
          </td>
          <td>
            <span class="status-badge badge-pass">100% CONCORDANT</span>
            <div class="subtext">1st/3rd gen Ceph 3/3; warned against amoxicillin monotherapy & VCUG.</div>
          </td>
          <td>
            <span class="status-badge badge-pass">100% CONCORDANT</span>
            <div class="subtext">90 mg/kg/day amoxicillin BID; no routine repeat CXR.</div>
          </td>
          <td>
            <span class="status-badge badge-pass">100% VACCINE AUDIT</span>
            <div class="subtext">ED obs 3/3; LP unnecessary if normal exam & fully immunized.</div>
          </td>
          <td>
            <div class="audit-score audit-green">100% PASS (15/15)</div>
            <div class="subtext"><b>Tier 1 Runner-Up:</b> Flawless conditional logic; strong clinical warnings & imaging stewardship.</div>
          </td>
        </tr>

        <!-- ChatGPT -->
        <tr>
          <td>
            <div class="tool-name">ChatGPT Clinicians</div>
            <div class="tool-sub">OpenAI (GPT-5.6 Terra)</div>
          </td>
          <td>
            <span class="status-badge badge-pass">100% STATED ASSUMP</span>
            <div class="subtext">Observe 3/3; stated assumptions; calculation guardrail.</div>
          </td>
          <td>
            <span class="status-badge badge-pass">100% PECARN RISK</span>
            <div class="subtext">Observe 3/3; calculated 0.9% ciTBI risk; noted LOC unstated.</div>
          </td>
          <td>
            <span class="status-badge badge-pass">100% EXACT MATH</span>
            <div class="subtext">Cephalexin 25 mg/kg TID; RBUS recommended, VCUG withheld.</div>
          </td>
          <td>
            <span class="status-badge badge-pass">100% EXACT MATH</span>
            <div class="subtext">Exact 832 mg BID amoxicillin; highlighted SpO2 93% cutoff.</div>
          </td>
          <td>
            <span class="status-badge badge-pass">⭐ DURATION ALERT</span>
            <div class="subtext">ED referral 3/3; flagged untimed onset could exceed 15 min.</div>
          </td>
          <td>
            <div class="audit-score audit-green">100% PASS (15/15)</div>
            <div class="subtext"><b>High Mathematical Rigor:</b> Zero fact confabulation, exact mg/kg dosing, and strong duration alertness.</div>
          </td>
        </tr>

        <!-- OpenEvidence -->
        <tr>
          <td>
            <div class="tool-name">OpenEvidence</div>
            <div class="tool-sub">Health-Specialized LLM</div>
          </td>
          <td>
            <span class="status-badge badge-fail">❌ FAILED 2/3 (MODE 2 & 6)</span>
            <div class="subtext">Fabricated "no abx in 30d" (2x); binned as <24mo (1x); 10d abx courses.</div>
          </td>
          <td>
            <span class="status-badge badge-pass">100% CONCORDANT</span>
            <div class="subtext">Observe 3/3; PECARN ≥2yo non-frontal hematoma + vomiting branch.</div>
          </td>
          <td>
            <span class="status-badge badge-pass">100% CONCORDANT</span>
            <div class="subtext">Cephalexin/Cefdinir 3/3; RBUS screening; no routine VCUG.</div>
          </td>
          <td>
            <span class="status-badge badge-pass">100% CONCORDANT</span>
            <div class="subtext">90 mg/kg/day amoxicillin; zero stale 40–45 mg/kg dosing.</div>
          </td>
          <td>
            <span class="status-badge badge-pass">100% PROLONGED CARE</span>
            <div class="subtext">ED transfer 3/3; recognized untimed onset duration risk.</div>
          </td>
          <td>
            <div class="audit-score audit-warn">86.7% PASS (13/15)</div>
            <div class="subtext"><b>Mixed Architecture:</b> 100% flawless across 4 new conditions, but failed under AOM equipoise deadlock.</div>
          </td>
        </tr>

        <!-- Ask Doximity -->
        <tr>
          <td>
            <div class="tool-name">Ask Doximity</div>
            <div class="tool-sub">Doximity AI</div>
          </td>
          <td>
            <span class="status-badge badge-pass">100% CONDITIONAL</span>
            <div class="subtext">Shared 3/3; 7d duration; 7 mL BID volume math; Cochrane trial data.</div>
          </td>
          <td>
            <span class="status-badge badge-fail">❌ SEARCH CONFAB</span>
            <div class="subtext">Rep 1 searched PECARN with fabricated <i>"no loss of consciousness"</i>.</div>
          </td>
          <td>
            <span class="status-badge badge-pass">100% CONCORDANT</span>
            <div class="subtext">Cephalexin/Cefdinir 3/3; RBUS stewardship confirmed.</div>
          </td>
          <td>
            <span class="status-badge badge-pass">100% CONCORDANT</span>
            <div class="subtext">80–90 mg/kg/day amoxicillin; full liquid volume conversion.</div>
          </td>
          <td>
            <span class="status-badge badge-fail">❌ HIGH VARIANCE</span>
            <div class="subtext">Rep 2 stated LP mandatory; Reps 1 & 3 stated LP unnecessary.</div>
          </td>
          <td>
            <div class="audit-score audit-warn">86.7% PASS (13/15)</div>
            <div class="subtext"><b>Tool-Query Leakage:</b> Strong dosing math, but injected fabricated negative facts into external calculator queries.</div>
          </td>
        </tr>

        <!-- Vera Health -->
        <tr>
          <td>
            <div class="tool-name">Vera Health</div>
            <div class="tool-sub">Vera AI</div>
          </td>
          <td>
            <span class="status-badge badge-pass">100% CONDITIONAL</span>
            <div class="subtext">Either 2/3, Treat 1/3; structured Watchful Waiting vs Treat table.</div>
          </td>
          <td>
            <span class="status-badge badge-fail">❌ FLAT FABRICATION</span>
            <div class="subtext">Reps 1 & 2 asserted <i>"No seizure or loss of consciousness"</i> as fact.</div>
          </td>
          <td>
            <span class="status-badge badge-pass">100% CONCORDANT</span>
            <div class="subtext">Cephalexin 50–100 mg/kg/day; RBUS yes, VCUG withheld.</div>
          </td>
          <td>
            <span class="status-badge badge-pass">100% CONCORDANT</span>
            <div class="subtext">90 mg/kg/day amoxicillin; noted tachypnea and hypoxia.</div>
          </td>
          <td>
            <span class="status-badge badge-warn">⚠️ STREAM TIMEOUT</span>
            <div class="subtext">Obs 2/3; duration uncertain noted; Rep 3 UI timeout on stream.</div>
          </td>
          <td>
            <div class="audit-score audit-fail">80.0% PASS (12/15)</div>
            <div class="subtext"><b>High Fact-Invention Risk:</b> Fabricated unstated negative variables to resolve PECARN observation branch.</div>
          </td>
        </tr>
      </tbody>
    </table>

    <div class="footer">
      <div>Michael Hobbs, MD • Synthetic Pediatric Chart Benchmark (No PHI) • Mode 1–6 Clinical Codebook</div>
      <div>96 Live Evaluated Traces Across Commercial Clinical AI Platforms (Aug–Sep 2026)</div>
    </div>
  </div>
</body>
</html>
`;

async function main() {
  const outDir = path.resolve(__dirname, "../posts");
  const cdsDir = path.resolve(__dirname, "../results/cds");
  
  const path4Cases = path.join(outDir, "cds_4cases_scoreboard.png");
  const path4CasesCds = path.join(cdsDir, "cds_4cases_scoreboard.png");
  const path5Cases = path.join(outDir, "cds_master_5cases_scoreboard.png");
  const path5CasesCds = path.join(cdsDir, "cds_master_5cases_scoreboard.png");

  console.log("Rendering 4-Case Generalization Scoreboard...");
  await renderTable(table4CasesHtml, path4Cases, 1500, 950);
  fs.copyFileSync(path4Cases, path4CasesCds);

  console.log("Rendering Full 5-Case Master Scoreboard...");
  await renderTable(table5CasesHtml, path5Cases, 1620, 1000);
  fs.copyFileSync(path5Cases, path5CasesCds);

  console.log("All scoreboards generated successfully!");
}

main().catch(err => {
  console.error("Error generating scoreboards:", err);
  process.exit(1);
});
