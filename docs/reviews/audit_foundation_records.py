#!/usr/bin/env python3
"""Read-only source audit. No provider calls or imports from experiment runners.

The 17-folder selection reproduces the quoted 1,778-row inventory. It is not
proof of execution dates, distinct API requests, or clinical correctness.
"""
import collections
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
FOLDERS = [
    'all5_cases_claude_cure', 'brake_branching_validation',
    'claude_cure_and_bias_verification', 'claude_cure_exploration',
    'claude_family_cure', 'credential_vs_gender', 'cure_6models_turn2_parallel',
    'cure_turn2_parallel_n3', 'demographics_4cases', 'factorial_2cubed_ablation',
    'factorial_2cubed_aom', 'factorial_2cubed_crosslab', 'high_thinking_4cases',
    'mitigation_4cases', 'reps_4cases', 'smoke_3cases', 'smoke_remaining2cases',
]


def digest(b):
    return hashlib.sha256(b).hexdigest()


def rows_in(data):
    if isinstance(data, list):
        return '', data
    for key in ('traces', 'results', 'rows'):
        if isinstance(data.get(key), list):
            return key, data[key]
    return '', []


def main():
    files, records, groups = [], [], collections.defaultdict(list)
    for folder in FOLDERS:
        for path in sorted((ROOT / 'results' / folder).glob('*.json')):
            raw = path.read_bytes()
            data = json.loads(raw)
            key, rows = rows_in(data)
            selected = [(i, r) for i, r in enumerate(rows) if isinstance(r, dict)
                        and any(k in r for k in ('text', 't1_text'))]
            files.append({'path': str(path.relative_to(ROOT)), 'sha256': digest(raw),
                          'rows': len(selected),
                          'recorded_timestamp': data.get('timestamp') if isinstance(data, dict) else None})
            for i, r in selected:
                ref = str(path.relative_to(ROOT)) + '#' + key + f'[{i}]'
                fields = {k: r.get(k) for k in ('text', 't1_text', 't2_text') if k in r}
                identity = digest(json.dumps(fields, sort_keys=True, ensure_ascii=False).encode())
                turns = []
                for field, text in fields.items():
                    token_key = {'text': 'output_tokens', 't1_text': 't1_tokens', 't2_text': 't2_tokens'}[field]
                    tokens = r.get(token_key, r.get('tokens') if field == 'text' else None)
                    latency_key = {'text': 'latency_s', 't1_text': 't1_latency', 't2_text': 't2_latency'}[field]
                    turns.append({'field': field, 'chars': len(text or ''), 'empty': not bool(text),
                                  'sha256': digest((text or '').encode()), 'output_tokens': tokens,
                                  'at_exactly_4000_tokens': tokens == 4000,
                                  'latency_present': latency_key in r or (field == 'text' and any(k in r for k in ('latency', 'dur'))),
                                  'stop_reason': r.get('stop_reason'),
                                  'ending': (text or '')[-160:]})
                record = {'ref': ref, 'folder': folder, 'text_record_sha256': identity,
                          'model': r.get('model_key', r.get('model')), 'model_id': r.get('model_id'),
                          'vendor': r.get('vendor'), 'case': r.get('case_id', r.get('task_type')),
                          'cell': r.get('cell_id'), 'experiment': r.get('exp_id'),
                          'rep': r.get('replicate', r.get('rep')), 'error_field_present': 'error' in r,
                          'recorded_error': r.get('error'), 'turns': turns}
                records.append(record)
                groups[identity].append(ref)
    canonical = [next(r for r in records if r['ref'] == refs[0]) for refs in groups.values()]
    turns = [(r['ref'], t) for r in canonical for t in r['turns']]
    validation = {
        'scope': '17 named folders reproducing the supplied audit; records may lack execution timestamps',
        'stored_records': len(records), 'folders': len(FOLDERS),
        'distinct_text_records': len(groups),
        'extra_master_or_component_copies': len(records) - len(groups),
        'distinct_text_records_is_not_a_verified_request_count': True,
        'represented_answer_fields_after_text_deduplication': len(turns),
        'empty_answer_fields': [{'ref': ref, 'field': t['field']} for ref, t in turns if t['empty']],
        'recorded_nonempty_error_fields': sum(bool(r['recorded_error']) for r in canonical),
        'records_without_error_field': sum(not r['error_field_present'] for r in canonical),
        'answer_fields_without_stop_reason': sum(t['stop_reason'] is None for _, t in turns),
        'answer_fields_without_output_tokens': sum(t['output_tokens'] is None for _, t in turns),
        'answer_fields_without_latency': sum(not t['latency_present'] for _, t in turns),
        'answer_fields_at_exactly_4000_tokens': sum(t['at_exactly_4000_tokens'] for _, t in turns),
        'token_limit_screen_is_not_an_adjudicated_truncation_count': True,
        'mean_chars_per_answer_field_including_empty': sum(t['chars'] for _, t in turns) / len(turns),
        'minimum_nonempty_answer_chars': min(t['chars'] for _, t in turns if t['chars']),
        'records_by_folder_before_deduplication': dict(collections.Counter(r['folder'] for r in records)),
        'duplicates': [refs for refs in groups.values() if len(refs) > 1],
    }
    extra = ROOT / 'results/mantra_smoke/canary_smoke_1788785688.json'
    if extra.exists():
        validation['additional_mantra_file_outside_quoted_17_folders'] = {
            'path': str(extra.relative_to(ROOT)), 'rows': len(json.loads(extra.read_text())),
            'sha256': digest(extra.read_bytes()), 'date_from_filename_epoch_is_not_request_provenance': True}
    evidence_path = OUT / 'FOUNDATION_EVIDENCE_2026-09-08.json'
    if evidence_path.exists():
        evidence = json.loads(evidence_path.read_text())
        for e in evidence:
            path = ROOT / e['source']
            assert digest(path.read_bytes()) == e['source_sha256'], e['id']
            if e.get('json_field'):
                data = json.loads(path.read_text())
                for part in e['json_field']:
                    data = data[part]
            else:
                data = path.read_text()
            assert data[e['start']:e['end']] == e['quote'], e['id']
        validation['evidence_spans_verified'] = len(evidence)
    (OUT / 'FOUNDATION_RECORD_INVENTORY_2026-09-08.json').write_text(
        json.dumps({'files': files, 'records': records}, indent=2, ensure_ascii=False) + '\n')
    (OUT / 'FOUNDATION_VALIDATION_2026-09-08.json').write_text(
        json.dumps(validation, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({k: v for k, v in validation.items() if k not in ('duplicates',)}, indent=2))


if __name__ == '__main__':
    main()
