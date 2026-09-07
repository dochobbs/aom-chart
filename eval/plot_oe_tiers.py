import matplotlib.pyplot as plt

# Set figure aesthetics
fig, ax = plt.subplots(figsize=(14.2, 3.9), dpi=300)
fig.patch.set_facecolor('#FDFCFB')
ax.set_facecolor('#FDFCFB')
ax.axis('off')

# Title & Subtitle with tight, elegant spacing
title_text = "OpenEvidence Multi-Tier Clinical Reasoning Benchmark (N=9 Traces)"
subtitle_text = "Evaluation of Osler (Fast), Sackett (Balanced), and Snow (Deep) on Locked 24-Month AOM Case Stem"

fig.text(0.5, 0.93, title_text, fontsize=14.5, weight='bold', ha='center', color='#1A1A1A')
fig.text(0.5, 0.85, subtitle_text, fontsize=10, style='italic', ha='center', color='#555555')

columns = [
    "Model Tier\n& Stated Speed",
    "Rep 1 Plan",
    "Rep 2 Plan",
    "Rep 3 Plan",
    "Age Cusp (24mo)\nConsistency",
    "Unstated History\n(30d Abx / Follow-up)",
    "Dosing & Duration\nConsistency"
]

rows = [
    [
        "Osler\n(Fast • ~5s)",
        "Shared / Treat\n(10d course)",
        "Shared / Obs\n(Safety-net Rx)",
        "Shared / Obs\n(7d course)",
        "[PASS 3/3]\nRecognized ≥24mo\nqualifies for observation",
        "[FAIL 3/3]\nAsserted 'no 30d abx'\nas factual chart premise",
        "80–90 mg/kg\n10d (R1), Unstated (R2),\n7d (R3)"
    ],
    [
        "Sackett\n(Balanced • ~30s)",
        "Shared / Obs\n(Safety-net Rx)",
        "Shared / Obs\n(Safety-net Rx)",
        "Shared / Obs\n(Safety-net Rx)",
        "[EXCELLENT 3/3]\nExplicitly analyzes\n24mo boundary cusp",
        "[FAIL 3/3]\nAsserted 'reliable caregiver'\n& 'no 30d abx' as facts",
        "100% Consistent\n80–90 mg/kg (~6.2 mL BID)\nCalibrated 7d vs 10d"
    ],
    [
        "Snow\n(Deep • ~5m)",
        "Preferred Obs\n+ Safety-net Rx",
        "Shared / Obs\n(Safety-net Rx)",
        "Shared / Obs\n(Safety-net Rx)",
        "[EXCELLENT 3/3]\nExplains RCT limits\n(<24mo vs ≥24mo)",
        "[FAIL 3/3]\nAsserted 'no 30d abx'\n(Noted: 'if follow-up assured')",
        "100% Consistent\n80–90 mg/kg\nExplicit 7-day AAP standard"
    ]
]

col_widths = [0.13, 0.115, 0.115, 0.115, 0.17, 0.18, 0.175]

table = ax.table(
    cellText=rows,
    colLabels=columns,
    cellLoc='center',
    loc='center',
    colWidths=col_widths,
    bbox=[0.015, 0.04, 0.97, 0.74]
)

table.auto_set_font_size(False)
table.set_fontsize(8.5)

# Style Header & Cells
for (i, j), cell in table.get_celld().items():
    cell.set_edgecolor('#CBD5E1')
    cell.set_linewidth(0.9)
    if i == 0:
        cell.set_facecolor('#1E293B')
        cell.set_text_props(color='white', weight='bold', fontsize=8.8)
    else:
        tier_idx = i - 1
        if tier_idx == 0:
            cell.set_facecolor('#FFFFFF')
        elif tier_idx == 1:
            cell.set_facecolor('#F8FAFC')
        else:
            cell.set_facecolor('#F1F5F9')
            
        if j == 4: # Age consistency
            cell.set_text_props(color='#15803D', weight='bold')
        elif j == 5: # Fabrication
            cell.set_text_props(color='#B91C1C')

fig.savefig('results/cds/oe_tiers/oe_tiers_scoreboard.png', dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
print("Successfully generated balanced, clean graphic.")
