"""Read-only source audit; writes derived review artifacts beside this script.
Run from any directory with python3 docs/reviews/audit_commercial_cds.py.
No browser, model calls, or mutation of the underlying results.
"""
from pathlib import Path
import collections, hashlib, json, re
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def group(p):
    rel = p.relative_to(ROOT).as_posix()
    if '/chatgpt_tiers/' in rel: return 'chatgpt_tiers'
    if '/oe_tiers/' in rel: return 'oe_tiers'
    if '/demographics/' in rel: return 'demographics'
    if '/mitigation/' in rel: return 'mitigation'
    if '/18mo/' in rel: return 'age_control'
    if 'results/cds_eval/' in rel: return 'baseline_aom'
    return 'four_new_cases'

files = sorted(list((ROOT/'results/cds').rglob('*.json')) + list((ROOT/'results/cds_eval').rglob('*.json')))
rows = []
by_hash = collections.defaultdict(list)
for p in files:
    d = json.loads(p.read_text())
    field = 'raw_text' if 'raw_text' in d else 'text'
    text = d[field]
    rel = p.relative_to(ROOT).as_posix()
    text_hash = hashlib.sha256(text.encode()).hexdigest()
    by_hash[text_hash].append(rel)
    rows.append(dict(source=rel, source_sha256=sha(p), text_field=field,
        text_sha256=text_hash, text_characters=len(text), group=group(p),
        tool=d.get('tool'), case_id=d.get('case_id'), variant_id=d.get('variant_id'),
        model=d.get('model'), intended_thinking_level=d.get('thinking_level'),
        configured_pill=d.get('configured_pill'), replicate=d.get('replicate'), timestamp=d.get('timestamp'),
        content_screen='inventory, duplicate and capture screening; not a whole-answer clinical pass'))

known_no_answer = []
# Exact Glass screens have been visually read as interface text, not answers.
for r in rows:
    if 'glass' in r['source'] and not r['source'].endswith('/glass.json'):
        r['capture_review'] = 'No case answer: interface-only capture'
        known_no_answer.append(r['source'])
# Manually checked Vera four-case processing-only snapshots.
for case, reps in {'head_24mo':[3], 'uti_24mo':[1,2], 'cap_5y':[1,2,3], 'seizure_6mo':[3]}.items():
    for rep in reps:
        target=f'results/cds/{case}/vera_health_rep{rep}.json'
        r=next(r for r in rows if r['source']==target)
        r['capture_review']='No final answer retained: prompt and/or processing text only'
        known_no_answer.append(target)

trial_files = sorted((ROOT/'results/cds/chatgpt_tiers').glob('*_rep*.json'))
metrics=collections.Counter(); config=[]; missing=[]; counterexamples=[]
for p in trial_files:
    d=json.loads(p.read_text()); s=d['raw_text']; pill=d.get('configured_pill')
    if pill is None: missing.append(p.name)
    elif not pill.endswith(d['thinking_level']): config.append({'file':p.name,'intended':d['thinking_level'],'visible_setting':pill})
    for k,pattern in {'original_regex_7ml':r'7\s*mL','original_regex_7days':r'7\s*days','seven_day_or_days':r'7[\s–-]*days?','aspirin_word':r'aspirin'}.items():
        metrics[k]+=bool(re.search(pattern,s,re.I))
    if not re.search(r'7\s*days',s,re.I):counterexamples.append({'file':p.name,'seven_day_hyphenated_present':bool(re.search(r'7[–-]day',s,re.I))})

# Verify selected findings as exact source spans and tie them back to the inventory.
evidence_path=OUT/'COMMERCIAL_CDS_EVIDENCE_2026-09-08.json'
evidence=json.loads(evidence_path.read_text()) if evidence_path.exists() else []
for e in evidence:
    p=ROOT/e['source'];d=json.loads(p.read_text());field='raw_text' if 'raw_text' in d else 'text';s=d[field]
    assert e['quote'] in s,(e['id'],e['quote'])
    e.update(source_sha256=sha(p),field=field,start=s.index(e['quote']),end=s.index(e['quote'])+len(e['quote']))
    r=next(r for r in rows if r['source']==e['source'])
    r.setdefault('review_finding_ids',[]).append(e['id'])
if evidence: evidence_path.write_text(json.dumps(evidence,indent=2,ensure_ascii=False)+'\n')

case_stems={}
for case in ['head_24mo','uti_24mo','cap_5y','seizure_6mo']:
    fs=list((ROOT/'results/cds'/case).glob('*_rep*.json'))
    stems={json.loads(p.read_text())['stem'] for p in fs}
    assert len(fs)==18 and len(stems)==1,(case,len(fs),len(stems))
    case_stems[case]={'replicate_files':len(fs),'distinct_stored_stems':len(stems)}
summary=dict(json_files=len(rows),doximity_files=sum('doximity' in r['source'] for r in rows),
    other_product_files=sum('doximity' not in r['source'] for r in rows),
    files_by_group=dict(collections.Counter(r['group'] for r in rows)),
    identical_text_groups=[fs for fs in by_hash.values() if len(fs)>1],
    known_no_answer_subset=known_no_answer,
    capture_warning='Known no-answer list is a verified subset, not exhaustive completion adjudication.',
    four_case_stems=case_stems,
    chatgpt_tier_checks={'files':len(trial_files),'mismatched_settings':config,'missing_setting_readback':missing,'text_presence_checks':dict(metrics),'hyphenated_duration_false_negatives':counterexamples,'interpretation':'Text presence counts are not clinical accuracy rates.'},
    exact_evidence_spans_verified=len(evidence),new_model_calls=0,original_results_modified=False)
(OUT/'COMMERCIAL_CDS_RECORD_AUDIT_2026-09-08.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
(OUT/'COMMERCIAL_CDS_VALIDATION_2026-09-08.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k in ['json_files','doximity_files','other_product_files','files_by_group','exact_evidence_spans_verified']},indent=2))
print('ChatGPT setting mismatches:',len(config),'; missing readbacks:',len(missing),'; presence checks:',dict(metrics))
