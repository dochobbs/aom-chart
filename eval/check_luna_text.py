import glob
import json

for f in sorted(glob.glob("results/cds/chatgpt_tiers/5_6_luna_*.json")):
    with open(f) as fp:
        d = json.load(fp)
    t = d.get("raw_text", "")
    print(f"\n--- {f} ---")
    print(t[:300].replace('\n', ' '))
