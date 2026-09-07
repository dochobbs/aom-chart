import matplotlib.pyplot as plt

# Create 300 DPI master scoreboard graphic
fig, ax = plt.subplots(figsize=(14.2, 7.2), dpi=300)
fig.patch.set_facecolor('#FDFCFB')
ax.set_facecolor('#FDFCFB')
ax.axis('off')

title_text = "ChatGPT for Clinicians: Full Reasoning Spectrum Benchmark (N = 36 Traces)"
subtitle_text = "Evaluation of 5.6 Sol, 5.6 Terra, and 5.6 Luna Across Light, Medium, High, and Max Thinking Modes"

fig.text(0.5, 0.95, title_text, fontsize=14.5, weight='bold', ha='center', color='#1A1A1A')
fig.text(0.5, 0.91, subtitle_text, fontsize=10, style='italic', ha='center', color='#555555')

columns = [
    "Model Tier",
    "Thinking Level\n& Compute",
    "N",
    "Age Cusp (24mo)\nConcordance",
    "Silent Premise\nFabrication",
    "Active Probing /\nConditional Logic",
    "High-Dose Amoxicillin\n(80–90 mg/kg & 7 mL)",
    "7-Day Duration\nConcordance"
]

rows = [
    # 5.6 Luna
    ["5.6 Luna", "Max (Level 4)", "3", "100% (3/3)", "0% (0/3)", "100% (3/3) (Top)", "100% (7 mL BID)", "100% (7 Days)"],
    ["5.6 Luna", "Medium (Level 1)", "3", "100% (3/3)", "0% (0/3)", "100% (3/3) (Top)", "100% (7 mL BID)", "100% (7 Days)"],
    ["5.6 Luna", "High (Level 2)", "3", "100% (3/3)", "0% (0/3)", "67% (2/3)", "67% (2/3)", "100% (7 Days)"],
    ["5.6 Luna", "Light (Level 0)", "3", "100% (3/3)", "0% (0/3)", "33% (1/3)", "67% (2/3)", "33% (1/3)"],
    
    # 5.6 Terra
    ["5.6 Terra", "Max (Level 4)", "3", "100% (3/3)", "0% (0/3)", "67% (2/3)", "100% (7 mL BID)", "100% (7 Days)"],
    ["5.6 Terra", "High (Level 2)", "3", "100% (3/3)", "0% (0/3)", "0% (Conditional)", "100% (7 mL BID)", "100% (7 Days)"],
    ["5.6 Terra", "Medium (Level 1)", "3", "100% (3/3)", "0% (0/3)", "33% (1/3)", "100% (7 mL BID)", "100% (7 Days)"],
    ["5.6 Terra", "Light (Level 0)", "3", "100% (3/3)", "0% (0/3)", "67% (2/3)", "100% (7 mL BID)", "100% (7 Days)"],
    
    # 5.6 Sol
    ["5.6 Sol", "Max (Level 4)", "3", "100% (3/3)", "0% (0/3)", "0% (Conditional)", "100% (7 mL BID)", "100% (7 Days)"],
    ["5.6 Sol", "High (Level 2)", "3", "100% (3/3)", "0% (0/3)", "0% (Conditional)", "100% (7 mL BID)", "100% (7 Days)"],
    ["5.6 Sol", "Medium (Level 1)", "3", "100% (3/3)", "0% (0/3)", "0% (Conditional)", "100% (7 mL BID)", "100% (7 Days)"],
    ["5.6 Sol", "Light (Level 0)", "3", "100% (3/3)", "0% (0/3)", "0% (Conditional)", "100% (7 mL BID)", "100% (7 Days)"]
]

col_widths = [0.13, 0.15, 0.05, 0.15, 0.13, 0.16, 0.16, 0.13]

table = ax.table(
    cellText=rows,
    colLabels=columns,
    cellLoc='center',
    loc='center',
    colWidths=col_widths,
    bbox=[0.01, 0.03, 0.98, 0.84]
)

table.auto_set_font_size(False)
table.set_fontsize(8.0)

for (i, j), cell in table.get_celld().items():
    cell.set_edgecolor('#CBD5E1')
    cell.set_linewidth(0.8)
    if i == 0:
        cell.set_facecolor('#0F3B32') # OpenAI Deep Teal
        cell.set_text_props(color='white', weight='bold', fontsize=8.4)
    else:
        row_idx = i - 1
        if row_idx < 4:
            cell.set_facecolor('#F0FDF4' if row_idx % 2 == 0 else '#FFFFFF') # Luna tint
        elif row_idx < 8:
            cell.set_facecolor('#F8FAFC' if row_idx % 2 == 0 else '#FFFFFF') # Terra tint
        else:
            cell.set_facecolor('#FDF4FF' if row_idx % 2 == 0 else '#FFFFFF') # Sol tint

        if j == 3 or j == 4 or j == 7:
            cell.set_text_props(color='#15803D', weight='bold')
        elif j == 5 and "100%" in rows[row_idx][5]:
            cell.set_text_props(color='#047857', weight='bold')

fig.savefig('results/cds/chatgpt_tiers/chatgpt_36_matrix_scoreboard.png', dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
print("Saved clean chatgpt_36_matrix_scoreboard.png.")
