import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(16.0, 8.8), dpi=300)
fig.patch.set_facecolor('#FDFCFB')
ax.set_facecolor('#FDFCFB')
ax.axis('off')

title_text = "Clinical AI Benchmark: OpenEvidence Tiers vs. ChatGPT for Clinicians (All Thinking Levels)"
subtitle_text = "Standardized 24-Month Pediatric AOM Evaluation Across Multi-Tier Clinical Reasoning Architectures (N = 45 Live Traces)"

fig.text(0.5, 0.96, title_text, fontsize=15.0, weight='bold', ha='center', color='#1A1A1A')
fig.text(0.5, 0.925, subtitle_text, fontsize=10.5, style='italic', ha='center', color='#555555')

columns = [
    "Platform &\nModel Architecture",
    "Thinking / Reasoning\nLevels Evaluated",
    "Sample\nSize",
    "24mo Age Cusp\nConcordance",
    "Silent Premise\nFabrication Rate",
    "Active Probing /\nConditional Logic",
    "Dosing & Liquid\nVolume Math",
    "Guideline Duration\n(7d vs. 10d)"
]

rows = [
    # OpenEvidence Tiers
    [
        "OpenEvidence\nOsler",
        "Fast / POC (~5s)",
        "N = 3",
        "100% (3/3)\nQualifies for Obs",
        "[FAIL] 100% (3/3)\nAsserts 'no abx in 30d' as fact",
        "0% (0/3)\nNo probing or branches",
        "90 mg/kg/day\n(Volume unstated)",
        "[DRIFT] 33% (1/3)\n(10d, unstated, 7d)"
    ],
    [
        "OpenEvidence\nSackett",
        "Balanced (~30s)",
        "N = 3",
        "100% (3/3)\nQualifies for Obs",
        "[FAIL] 100% (3/3)\nAsserts 'no abx in 30d' as fact",
        "0% (0/3)\nNo probing or branches",
        "90 mg/kg/day\n6.25 mL BID (400/5)",
        "100% (3/3)\n7 Days (Cochrane)"
    ],
    [
        "OpenEvidence\nSnow",
        "Deep (~5m)",
        "N = 3",
        "100% (3/3)\nPrefers Obs",
        "[FAIL] 100% (3/3)\nAsserts 'no abx in 30d' as fact",
        "0% (0/3)\nNo probing or branches",
        "90 mg/kg/day\n(Trial synthesis)",
        "100% (3/3)\n7 Days (<2yo RCT)"
    ],
    
    # ChatGPT Clinicians Models (Full N=12 aggregates)
    [
        "ChatGPT Clinicians\n5.6 Luna (All Levels)",
        "Light, Medium, High, Max\n(N=3 reps each)",
        "N = 12",
        "100% (12/12)\nQualifies for Obs",
        "[PASS] 0% (0/12)\nZero premise fabrication",
        "[TOP] 100% (12/12)\nActive probing & branches\n(Top in Medium & Max)",
        "90 mg/kg/day\n83% 7 mL BID\n(558 mg BID)",
        "83% (10/12)\n7 Days\n(100% in Med/High/Max)"
    ],
    [
        "ChatGPT Clinicians\n5.6 Terra (All Levels)",
        "Light, Medium, High, Max\n(N=3 reps each)",
        "N = 12",
        "100% (12/12)\nQualifies for Obs",
        "[PASS] 0% (0/12)\nZero premise fabrication",
        "[PASS] 100% (12/12)\nDirective verification\n& Augmentin branches",
        "90 mg/kg/day\n92% 7 mL BID\n(1,120 mg/day)",
        "100% (12/12)\n7 Days (Age-tiered)"
    ],
    [
        "ChatGPT Clinicians\n5.6 Sol (All Levels)",
        "Light, Medium, High, Max\n(N=3 reps each)",
        "N = 12",
        "100% (12/12)\nQualifies for Obs",
        "[PASS] 0% (0/12)\nZero premise fabrication",
        "[PASS] 100% (12/12)\nExplicit assumptions\n& Augmentin branches",
        "90 mg/kg/day\n100% 7 mL BID\n(560 mg BID)",
        "100% (12/12)\n7 Days (Age-tiered)"
    ]
]

col_widths = [0.15, 0.16, 0.06, 0.13, 0.16, 0.15, 0.12, 0.13]

table = ax.table(
    cellText=rows,
    colLabels=columns,
    cellLoc='center',
    loc='center',
    colWidths=col_widths,
    bbox=[0.01, 0.03, 0.98, 0.86]
)

table.auto_set_font_size(False)
table.set_fontsize(7.8)

for (i, j), cell in table.get_celld().items():
    cell.set_edgecolor('#CBD5E1')
    cell.set_linewidth(0.8)
    if i == 0:
        cell.set_facecolor('#1E293B') # Slate Navy Header
        cell.set_text_props(color='white', weight='bold', fontsize=8.2)
    else:
        row_idx = i - 1
        if row_idx < 3:
            cell.set_facecolor('#F8FAFC' if row_idx % 2 == 0 else '#FFFFFF')
        else:
            cell.set_facecolor('#F0FDF4' if row_idx % 2 == 0 else '#FFFFFF')
            
        if row_idx < 3 and j == 4:
            cell.set_text_props(color='#B91C1C', weight='bold') # Red for OE fabrication
        elif row_idx >= 3 and j == 4:
            cell.set_text_props(color='#047857', weight='bold') # Green for 0% fabrication
            
        if j == 3:
            cell.set_text_props(color='#15803D', weight='bold')

fig.savefig('results/cds/oe_vs_chatgpt_master_comparison.png', dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
print("Saved oe_vs_chatgpt_master_comparison.png successfully.")
