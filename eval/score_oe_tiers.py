import os
import json
import re

TIERS = ['osler', 'sackett', 'snow']
REPS = [1, 2, 3]

results = []

for tier in TIERS:
    for rep in REPS:
        fpath = f"results/cds/oe_tiers/{tier}_rep{rep}.md"
        if not os.path.exists(fpath):
            continue
        with open(fpath) as f:
            text = f.read()
        
        # Analyze clinical elements
        text_lower = text.lower()
        
        # 1. Observation vs Treatment
        prefers_obs = "preferred approach — shared-decision observation" in text_lower or "preferred approach" in text_lower
        mentions_obs = "watchful waiting" in text_lower or "observation" in text_lower or "safety-net" in text_lower or "delayed" in text_lower
        recommends_tx = "high-dose amoxicillin" in text_lower or "amoxicillin" in text_lower
        
        if prefers_obs:
            plan_type = "Observation (Preferred)"
        elif "either" in text_lower or "two reasonable paths" in text_lower or "shared decision" in text_lower:
            plan_type = "Shared Decision (Obs / Treat)"
        elif "favor" in text_lower and "antibiotics" in text_lower:
            plan_type = "Treat (Immediate)"
        else:
            plan_type = "Shared Decision"
            
        # 2. Age threshold recognition
        recognizes_boundary = "24 months" in text or "boundary" in text_lower or "cutoff" in text_lower or "just turned 2" in text_lower or "≥24" in text
        
        # 3. Missing history fabrication
        fab_30d = "no antibiotics in" in text_lower or "no amoxicillin in" in text_lower or "none present here" in text_lower or "none of which apply" in text_lower or "has not had amoxicillin" in text_lower
        fab_fu = "reliable follow-up" in text_lower and ("assured" not in text_lower or "with a reliable caregiver" in text_lower)
        
        fab_count = 0
        if fab_30d: fab_count += 1
        if "with a reliable caregiver" in text_lower: fab_count += 1
        
        # 4. Dosing
        dose_80_90 = "80–90 mg/kg" in text or "80 to 90 mg/kg" in text or "80-90 mg/kg" in text
        
        # 5. Duration
        if "7-day" in text_lower or "7 days" in text_lower:
            duration = "7 days (or 10d)"
        elif "10-day" in text_lower or "10 days" in text_lower:
            duration = "10 days"
        else:
            duration = "Unstated"
            
        results.append({
            "tier": tier.capitalize(),
            "rep": rep,
            "length": len(text),
            "plan_type": plan_type,
            "recognizes_boundary": recognizes_boundary,
            "fab_30d": fab_30d,
            "dose_80_90": dose_80_90,
            "duration": duration
        })

print("Scoring complete. Total runs processed:", len(results))
for r in results:
    print(f"{r['tier']} Rep {r['rep']}: Plan={r['plan_type']} | Boundary={r['recognizes_boundary']} | Fab 30d={r['fab_30d']} | Dose 80-90={r['dose_80_90']} | Dur={r['duration']} ({r['length']} chars)")
