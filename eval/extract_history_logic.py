import glob
import json
import re

files = sorted(glob.glob("results/cds/chatgpt_tiers/*_rep*.json"))

print(f"Total files: {len(files)}\n")

categories = {
    "5.6 Luna": [],
    "5.6 Terra": [],
    "5.6 Sol": []
}

for f in files:
    with open(f) as fp:
        d = json.load(fp)
    text = d.get("raw_text", "")
    model = d.get("model", "")
    level = d.get("thinking_level", "")
    rep = d.get("replicate", "")
    
    # Extract sentences discussing amoxicillin 30 days, follow up, or observation criteria
    sentences = re.split(r'(?<=[.!?])\s+', text)
    history_snippets = []
    for s in sentences:
        if any(w in s.lower() for w in ["30 day", "prior amox", "recent amox", "missing", "confirm", "clarify", "if follow-up", "reliable", "safety-net"]):
            history_snippets.append(s.strip())
            
    key = f"{model} ({level} • Rep {rep})"
    for m_key in categories:
        if m_key in model:
            categories[m_key].append((key, history_snippets[:3]))

for m_key, items in categories.items():
    print(f"==================================================")
    print(f"MODEL: {m_key}")
    print(f"==================================================")
    for k, snippets in items[:4]: # show sample
        print(f"\n--- {k} ---")
        for s in snippets:
            print(f"  • {s}")
