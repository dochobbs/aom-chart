import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(15.8, 8.2), dpi=300)
fig.patch.set_facecolor('#FDFCFB')
ax.set_facecolor('#FDFCFB')
ax.axis('off')

title_text = "Clinical AI Benchmark: OpenEvidence Tiers vs. ChatGPT for Clinicians"
subtitle_text = "Standardized 24-Month Pediatric AOM Benchmark Across Multi-Tier Clinical Reasoning Architectures"

fig.text(0.5, 0.95, title_text, fontsize=15, weight='bold', ha='center', color='#1A1A1A')
fig.text(0.5, 0.91, subtitle_text, fontsize=10.5, style='italic', ha='center', color='#555555')

columns = [
    "Platform &\nReasoning Tier",
    "Compute /\nSpeed",
    "Age Cusp (24mo)\nConcordance",
    "Missing History Handling\n(30d Abx & Follow-Up)",
    "Dosing &\nLiquid Volume Math",
    "Guideline Duration\n(7d vs. 10d)",
    "Core Behavior &\nClinical Failure Mode"
]

rows = [
    # OpenEvidence Tiers
    [
        "OpenEvidence\nOsler",
        "Fast\n(~5s)",
        "100% (3/3)\nQualifies for Obs",
        "[FAIL] 100% Fabrication\nAsserts 'no abx in 30d'\nas factual chart premise",
        "90 mg/kg/day\n(Volume unstated)",
        "[DRIFT] 33% (1/3)\nDuration drift across runs\n(10d, unstated, 7d)",
        "Rapid guideline summary;\nDuration drift across runs"
    ],
    [
        "OpenEvidence\nSackett",
        "Balanced\n(~30s)",
        "100% (3/3)\nQualifies for Obs",
        "[FAIL] 100% Fabrication\nAsserts 'no abx in 30d'\nas factual chart premise",
        "90 mg/kg/day\n6.25 mL BID (400 mg/5 mL)",
        "100% (3/3)\n7 Days\n(Cochrane NNT/NNH)",
        "100% consistent evidence;\nFabricates missing chart history"
    ],
    [
        "OpenEvidence\nSnow",
        "Deep\n(~5m)",
        "100% (3/3)\nPrefers Obs",
        "[FAIL] 100% Fabrication\nAsserts 'no abx in 30d'\nas factual chart premise",
        "90 mg/kg/day\n(Full trial synthesis)",
        "100% (3/3)\n7 Days\n(Distinguishes <2yo trial)",
        "Deep evidence synthesis;\nFabricates missing chart history"
    ],
    
    # ChatGPT for Clinicians Tiers
    [
        "ChatGPT Clinicians\n5.6 Luna",
        "Deep / Max\n(~2–3m)",
        "100% (3/3)\nQualifies for Obs",
        "[TOP] 100% Active Probing\n'First clarify missing determinant:\nreliable follow-up & 30d abx'",
        "90 mg/kg/day\n7 mL BID (558 mg BID)",
        "100% (3/3)\n7 Days (Age-tiered)",
        "Best-in-class active probing;\nZero premise fabrication"
    ],
    [
        "ChatGPT Clinicians\n5.6 Terra",
        "Standard\n(~1m)",
        "100% (3/3)\nQualifies for Obs",
        "[PASS] 100% Verification\n'First confirm amox in 30d...'\nDual-branch Augmentin backup",
        "90 mg/kg/day\n7 mL BID (1,120 mg/day)",
        "100% (3/3)\n7 Days (Age-tiered)",
        "Workhorse CDS; Dual branches;\nZero premise fabrication"
    ],
    [
        "ChatGPT Clinicians\n5.6 Sol",
        "Max\n(~2m)",
        "100% (3/3)\nQualifies for Obs",
        "[PASS] 100% Assumptions\n'This assumes no amox in 30d'\nDual-branch Augmentin backup",
        "90 mg/kg/day\n7 mL BID (560 mg BID)",
        "100% (3/3)\n7 Days (Age-tiered)",
        "Pediatric tool lookup skill;\nZero premise fabrication"
    ]
]

col_widths = [0.14, 0.10, 0.13, 0.23, 0.14, 0.12, 0.14]

table = ax.table(
    cellText=rows,
    colLabels=columns,
    cellLoc='center',
    loc='center',
    colWidths=col_widths,
    bbox=[0.01, 0.03, 0.98, 0.84]
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
            
        if row_idx < 3 and j == 3:
            cell.set_text_props(color='#B91C1C', weight='bold') # Red for OE fabrication
        elif row_idx >= 3 and j == 3:
            cell.set_text_props(color='#047857', weight='bold') # Green for ChatGPT probing/verification
            
        if j == 2:
            cell.set_text_props(color='#15803D', weight='bold')

fig.savefig('results/cds/comparison_oe_vs_chatgpt_tiers.png', dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
print("Re-rendered comparison_oe_vs_chatgpt_tiers.png cleanly.")
