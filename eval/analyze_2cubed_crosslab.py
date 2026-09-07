#!/usr/bin/env python3
"""
Analyze Cross-Lab 2^3 Factorial Matrix on Head Trauma:
Testing all 8 combinations of Query (A), Brake (B), and Branching (C)
on OpenAI (gpt-5.6-terra) and Google (gemini-3.1-pro-preview).
"""

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
RESULTS_DIR = REPO_ROOT / "results" / "factorial_2cubed_crosslab"

def calc_ci(k, n):
    if n == 0: return 0.0, 0.0
    p = k / n
    z = 1.95996
    denom = 1 + z**2 / n
    centre = (p + z**2 / (2 * n)) / denom
    spread = z * math.sqrt((p * (1 - p) + z**2 / (4 * n)) / n) / denom
    return max(0.0, (centre - spread) * 100), min(100.0, (centre + spread) * 100)

def analyze_file(file_path: Path):
    with open(file_path) as f:
        data = json.load(f)
        
    case = data.get("case", "unknown")
    traces = data["traces"]
    print(f"Loaded {len(traces)} traces from {file_path.name} (Case: {case})\n")
    
    cells = [
        ("cell_1_none", "1. None (Baseline)"),
        ("cell_2_A_only", "2. A only (Query)"),
        ("cell_3_B_only", "3. B only (Brake)"),
        ("cell_4_C_only", "4. C only (Branching)"),
        ("cell_5_AB", "5. A + B (Query + Brake)"),
        ("cell_6_AC", "6. A + C (Query + Branching)"),
        ("cell_7_BC", "7. B + C (Brake + Branching)"),
        ("cell_8_ABC", "8. A + B + C (Full Compound)"),
    ]
    
    models = [
        ("terra", "GPT-5.6 Terra (OpenAI)"),
        ("gemini-pro", "Gemini 3.1 Pro (Google)"),
    ]
    
    lines = []
    lines.append(f"# Cross-Lab 2^3 Factorial Ablation: `{case}`")
    lines.append(f"\n**Timestamp:** {data.get('timestamp')}")
    lines.append(f"**Total Traces:** {len(traces)} (8 cells x 2 models x 3 replicates)")
    lines.append(f"**Total Execution Time:** {data.get('wall_clock_seconds', 0):.1f}s\n")
    lines.append("| Cell ID | Configuration | GPT-5.6 Terra | Gemini 3.1 Pro | **Total Confab** | **Confab Rate** | 95% Score CI | Branching Rate |")
    lines.append("| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |")
    
    for cid, cname in cells:
        ct_traces = [t for t in traces if t["cell_id"] == cid]
        n_cell = len(ct_traces)
        cell_confab = 0
        cell_branch = 0
        
        m_res = {}
        for mkey, mname in models:
            m_traces = [t for t in ct_traces if t["model_key"] == mkey]
            n_m = len(m_traces)
            k_m = sum(1 for t in m_traces if t["audit"]["confab"])
            m_res[mkey] = f"{k_m}/{n_m}"
            cell_confab += k_m
            cell_branch += sum(1 for t in m_traces if t["audit"]["has_branching"])
            
        rate = (cell_confab / n_cell * 100) if n_cell else 0
        low, high = calc_ci(cell_confab, n_cell)
        br_rate = (cell_branch / n_cell * 100) if n_cell else 0
        
        lines.append(f"| `{cid}` | {cname} | {m_res['terra']} | {m_res['gemini-pro']} | **{cell_confab}/{n_cell}** | **{rate:.1f}%** | [{low:.1f}%, {high:.1f}%] | {cell_branch}/{n_cell} ({br_rate:.0f}%) |")
        
    report = "\n".join(lines)
    report_file = RESULTS_DIR / f"CROSS_LAB_FACTORIAL_REPORT_{case.upper()}.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    print(report)
    print(f"\nReport written to {report_file}\n" + "=" * 80 + "\n")

def main():
    files = list(RESULTS_DIR.glob("factorial_2cubed_crosslab_*traces.json"))
    if not files:
        print("No cross-lab result files found yet.")
        return
        
    for f in sorted(files):
        analyze_file(f)

if __name__ == "__main__":
    main()
