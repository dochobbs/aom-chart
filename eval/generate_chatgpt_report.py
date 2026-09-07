import os
import matplotlib.pyplot as plt

# High-res scoreboard graphic with refined padding
fig, ax = plt.subplots(figsize=(14.2, 4.1), dpi=300)
fig.patch.set_facecolor('#FDFCFB')
ax.set_facecolor('#FDFCFB')
ax.axis('off')

title_text = "ChatGPT for Clinicians Frontier Benchmark (5.6 Sol • Terra • Luna)"
subtitle_text = "Evaluation of Reasoning Depth, Missing History Handling, and Boundary Logic on 24-Month AOM Case"

fig.text(0.5, 0.93, title_text, fontsize=14.5, weight='bold', ha='center', color='#1A1A1A')
fig.text(0.5, 0.85, subtitle_text, fontsize=10, style='italic', ha='center', color='#555555')

columns = [
    "Model Tier\n& Reasoning Time",
    "Primary Plan\n& Strategy",
    "Age Cusp (24mo)\nConsistency",
    "Missing History Handling\n(30d Abx & Follow-Up)",
    "Dosing & Liquid Volume\n(12.4 kg Child)",
    "Duration &\nGuardrails"
]

rows = [
    [
        "5.6 Sol\n(Max • 2m 12s)",
        "Shared / Observation\n(48–72h Safety-Net Rx)",
        "[EXCELLENT]\nRecognizes exactly 24mo\nqualifies for observation",
        "[EXCELLENT]\n'After confirming no 30d abx'\nProvides Augmentin branch",
        "Amoxicillin 400 mg/5 mL:\n7 mL PO BID (560 mg BID)\n~90 mg/kg/day",
        "7 Days\nAcetaminophen / Ibuprofen\nWarns vs routine alternating"
    ],
    [
        "5.6 Terra\n(Standard • 1m 45s)",
        "Shared / Watchful Waiting\n(48–72h Safety-Net Rx)",
        "[EXCELLENT]\nRecognizes 24mo boundary\nconcordant with observation",
        "[EXCELLENT]\n'First confirm amox exposure...'\nProvides ES-600 branch (4.7 mL)",
        "Amoxicillin 400 mg/5 mL:\n7 mL PO BID (1,120 mg/day)\n~90 mg/kg/day",
        "7 Days\nAvoid aspirin & OTC cough/cold\nClear red-flag return criteria"
    ],
    [
        "5.6 Luna\n(Max • 3m 36s)",
        "Shared / Observation\n(48–72h Safety-Net Rx)",
        "[EXCELLENT]\nExplicitly notes 24mo\nqualifies for observation",
        "[BEST-IN-CLASS]\n'First clarify missing determinant:\nreliable follow-up & 30d abx'",
        "Amoxicillin 400 mg/5 mL:\n7 mL PO BID (558 mg BID)\n~90 mg/kg/day",
        "7 Days\nOral syringe verification\nAvoid combination cold meds"
    ]
]

col_widths = [0.14, 0.15, 0.16, 0.22, 0.17, 0.16]

table = ax.table(
    cellText=rows,
    colLabels=columns,
    cellLoc='center',
    loc='center',
    colWidths=col_widths,
    bbox=[0.015, 0.04, 0.97, 0.74]
)

table.auto_set_font_size(False)
table.set_fontsize(8.2)

for (i, j), cell in table.get_celld().items():
    cell.set_edgecolor('#CBD5E1')
    cell.set_linewidth(0.9)
    if i == 0:
        cell.set_facecolor('#0F3B32') # Deep OpenAI Teal
        cell.set_text_props(color='white', weight='bold', fontsize=8.6)
    else:
        tier_idx = i - 1
        if tier_idx == 0:
            cell.set_facecolor('#FFFFFF')
        elif tier_idx == 1:
            cell.set_facecolor('#F4FBF9')
        else:
            cell.set_facecolor('#E8F6F3')
            
        if j == 2:
            cell.set_text_props(color='#15803D', weight='bold')
        elif j == 3:
            cell.set_text_props(color='#047857', weight='bold')

fig.savefig('results/cds/chatgpt_tiers/chatgpt_tiers_scoreboard.png', dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
print("Re-rendered chatgpt_tiers_scoreboard.png.")
