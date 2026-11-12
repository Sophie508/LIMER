"""Verify the public export and derive review tables; no raw archive replay."""
import argparse
from collections import Counter
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def files():
    excluded = {'.git', '__pycache__', '.pytest_cache', '.venv', 'outputs', 'build'}
    return {p.relative_to(ROOT).as_posix(): sha(p) for p in ROOT.rglob('*')
            if p.is_file() and not excluded.intersection(p.relative_to(ROOT).parts)
            and p.name != 'release-manifest.json'}


def source_identity(registration, snapshot, index):
    entries = []
    for name, value in registration['source_hashes'].items():
        if isinstance(value, dict):
            entries.extend((str(Path(name) / n), h) for n, h in value.items())
        else:
            entries.append((name, value))
    checked, redacted = 0, 0
    for name, expected in entries:
        if any(part.startswith('._') for part in Path(name).parts):
            continue
        target = snapshot / name
        assert target.is_file(), 'Missing source: ' + str(target.relative_to(ROOT))
        if sha(target) != expected:
            public_name = target.relative_to(ROOT).as_posix()
            origin = index['files'][public_name]
            assert name == 'tools/research_report.py', 'Scientific source differs: ' + public_name
            assert origin['metadata_redacted'] and origin['original_sha256'] == expected
            redacted += 1
        checked += 1
    return dict(checked=checked, descriptive_tool_redactions=redacted)


def verify_gate(directory, rows):
    registration = read(directory / 'registration.json')
    summary = read(directory / 'gray_gate_summary.json')
    cases = {c['name']: c for c in registration['plan']['cases']}
    scores = {r['name']: r for r in summary['rows']}
    assert cases.keys() == scores.keys(), 'Registered denominator changed'
    counts = Counter(registered=len(cases))
    for name, case in cases.items():
        row = scores[name]
        attempt_path = directory / 'attempts' / (name + '.json')
        attempted = attempt_path.is_file()
        assert row['attempted'] == attempted
        if not attempted:
            assert not row['valid'] and row['communication_ms'] is None
            counts['unrun'] += 1
        else:
            counts['attempted'] += 1
            attempt = read(attempt_path)
            assert attempt['valid'] == row['valid']
            if not row['valid']:
                assert row['communication_ms'] is None
                counts['invalid'] += 1
            else:
                counts['valid'] += 1
                result = read(directory / 'runs' / name / 'result.json')
                assert result['scene'] == case['scene'] and result['method'] == case['method']
                assert result['audit']['pass'] and result['observation_audit']['pass']
                status = result['status']
                completed = status['status'] == 'completed'
                assert row['completed'] == completed
                assert row['classification'] == attempt['score']['classification']
                assert row['all_paths_timely'] == attempt['score']['all_paths_timely_success']
                assert row['all_paths_delay_ms'] == attempt['score']['all_paths_delay_ms']
                if completed:
                    expected = (status['job_done_ns'] - 1_000_000) / 1e6
                    assert row['communication_ms'] == expected
                    counts['completed'] += 1
                else:
                    assert row['communication_ms'] is None
                    assert row['capped_ms'] == (case['scene']['horizon_ns'] - 1_000_000) / 1e6
                    counts['unfinished'] += 1
                if row['classification'] == 'miss':
                    assert not row['all_paths_timely']
                    assert row['all_paths_delay_ms'] is None
        rows.append(dict(study=directory.name, condition=case['condition'], arm=case['arm'],
                         seed=case['scene']['seed'], attempted=attempted, valid=row['valid'],
                         completed=row['completed'], classification=row['classification'],
                         communication_ms=row['communication_ms'],
                         healthy_ratio=row['healthy_ratio'],
                         detection_ms=row['all_paths_delay_ms']))
    for key in ('registered', 'attempted', 'valid', 'completed'):
        assert summary[key] == counts[key], key
    for row in summary['rows']:
        if row['completed']:
            reference = scores[row['healthy_reference']]
            if reference['completed']:
                assert row['healthy_ratio'] == reference['communication_ms'] / row['communication_ms']
            else:
                assert row['healthy_ratio'] is None, 'Unrun healthy control cannot supply a denominator'
    return dict(counts)


def verify_throughput(directory, report_path, rows):
    registration, report = read(directory / 'registration.json'), read(report_path)
    cases = {c['name']: c for c in registration['cases']}
    scores = {r['name']: r for r in report['rows']}
    assert cases.keys() == scores.keys()
    counts = Counter(registered=len(cases))
    for name, case in cases.items():
        row = scores[name]
        attempt_path = directory / 'attempts' / (name + '.json')
        attempted = attempt_path.is_file()
        if not attempted:
            assert not row['valid']
            counts['unrun'] += 1
        else:
            counts['attempted'] += 1
            attempt = read(attempt_path)
            assert attempt['valid'] == row['valid']
            if not row['valid']:
                counts['invalid'] += 1
            else:
                counts['valid'] += 1
                result = attempt['result']
                assert result['scene'] == case['scene'] and result['method'] == case['method']
                assert result['audit']['pass'] and result['observation_audit']['pass']
                assert row['status'] == result['status']['status']
                assert row['communication_ms'] == result['performance']['communication_ms']
                if row['status'] == 'completed':
                    assert row['communication_ms'] == (result['status']['job_done_ns'] - 1_000_000) / 1e6
                    counts['completed'] += 1
                else:
                    counts['unfinished'] += 1
        if row['old_healthy_normalized_percent'] is not None:
            assert row['old_healthy_normalized_percent'] == 100 * 480.178448 / row['communication_ms']
        rows.append(dict(study='throughput-' + directory.name, condition=row['family'], arm=row['policy'],
                         seed=row['seed'], attempted=attempted, valid=row['valid'],
                         completed=row['status'] == 'completed',
                         classification=row.get('detector_classification'),
                         communication_ms=row['communication_ms'],
                         healthy_ratio=(row['healthy_normalized_percent'] / 100
                                        if row['healthy_normalized_percent'] is not None else None),
                         detection_ms=row.get('detection_ms')))
    assert report['registered'] == counts['registered'] and report['valid'] == counts['valid']
    assert report['completed'] == counts['completed']
    return dict(counts)


def verify_detection(directory, rows):
    registration = read(directory / 'registration.json')
    report = read(directory / 'research_summary.json')
    with (directory / 'research_trials.csv').open(newline='') as stream:
        table = list(csv.DictReader(stream))
    assert {r['name'] for r in table} == {c['name'] for c in registration['plan']['cases']}
    assert len(table) == report['registered']
    for group in report['groups']:
        selected = [r for r in table if all(r[k] == group[k] for k in ('condition', 'detector', 'arm'))]
        assert len(selected) == group['registered']
        assert sum(r['valid'] == 'True' for r in selected) == group['verified']
        assert sum(r['all_paths_timely'] == 'True' for r in selected) == group['timely_trials']
        assert dict(Counter(r['classification'] for r in selected)) == group['classifications']
        if group['condition'] == 'healthy':
            assert sum(r['healthy_false_alarm'] == 'True' for r in selected) == group['healthy_false_alarm_trials']
            assert group['p95_all_trials_ms'] is None
        else:
            assert group['healthy_false_alarm_trials'] is None
            ordered = sorted(float(r['all_paths_delay_ms'])
                             if r['valid'] == 'True' and r['all_paths_delay_ms']
                             else float('inf') for r in selected)
            p95 = ordered[math.ceil(.95 * len(ordered)) - 1]
            assert group['p95_all_trials_ms'] == (p95 if math.isfinite(p95) else None)
        for row in selected:
            if row['all_paths_timely'] == 'True':
                assert row['valid'] == 'True' and float(row['all_paths_delay_ms']) < 100
    # Do not pool the primary and supplemental weak-loss streams.
    headline = [g for g in report['groups'] if g['arm'] == 'benefit' and
                g['condition'] in ({'weak_loss'} if directory.name.endswith('v4')
                                   else {'blackhole', 'quarter', 'delay'})]
    for group in headline:
        rows.append(dict(study='historical-detection-' + directory.name,
                         condition=group['condition'], arm=group['arm'],
                         registered=group['registered'], timely=group['timely_trials'],
                         detection_p95_ms=group['p95_all_trials_ms']))
    return dict(registered=len(table), valid=sum(r['valid'] == 'True' for r in table),
                invalid=sum(r['valid'] != 'True' for r in table))


def verify_repair_locality():
    original = ROOT / 'data/gate/evidence/confirmation-v2'
    repaired = ROOT / 'data/gate/evidence-terminal-fix/confirmation-terminal-fix'
    old_reg, new_reg = read(original / 'registration.json'), read(repaired / 'registration.json')
    assert old_reg['plan'] == new_reg['plan']
    changed = sorted(p for p in old_reg['source_hashes']
                     if old_reg['source_hashes'][p] != new_reg['source_hashes'][p])
    assert changed == ['src/simulator/recovery/proxy.h', 'src/simulator/runtime/completion.h']
    selected = [r for r in read(repaired / 'gray_gate_summary.json')['rows'] if r['attempted']]
    for row in selected:
        before, after = (p / 'runs' / row['name'] for p in (original, repaired))
        old_status, new_status = read(before / 'run_status.json'), read(after / 'run_status.json')
        done = new_status['job_done_ns']
        assert old_status['job_done_ns'] == done
        for name in ['policy_decisions.jsonl', 'service_alarms.csv']:
            assert sha(before / name) == sha(after / name)
        old_controls = list(csv.DictReader((before / 'control_events.csv').open(newline='')))
        new_controls = list(csv.DictReader((after / 'control_events.csv').open(newline='')))
        assert [r for r in old_controls if int(r['sent_ns']) < done] == [
            r for r in new_controls if int(r['sent_ns']) < done]
        if row['arm'] == 'candidate_gate':
            phase = str(new_status['phases_expected'] - 1)
            requested = {r['version'] for r in new_controls if r['phase'] == phase and r['event'] == 'LEND_TX'}
            released = {r['version'] for r in new_controls if r['phase'] == phase and r['event'] == 'LEND_RELEASED'}
            assert requested <= released
    return dict(selected_runs=len(selected), unchanged_precompletion=True,
                final_phase_releases_verified=True, native_changed_files=changed)


def verify(out=None):
    manifest = read(ROOT / 'release-manifest.json')
    actual = files()
    assert actual == manifest['files'], 'Public release content differs from its manifest'
    links = {p.relative_to(ROOT).as_posix(): str(p.readlink())
             for p in ROOT.rglob('*') if p.is_symlink() and '.git' not in p.parts}
    assert links == manifest['symlinks'], 'Snapshot dependency links changed'
    assert all((ROOT / p).exists() and ROOT in (ROOT / p).resolve().parents for p in links), 'External dependency link'
    index = read(ROOT / 'provenance/public-export.json')
    rows, campaigns = [], []
    for campaign in index['campaigns']:
        directory = ROOT / campaign['directory']
        registration = read(directory / 'registration.json')
        snapshot = ROOT / index['source_snapshots'][campaign['source']]['directory']
        identities = source_identity(registration, snapshot, index)
        if campaign['kind'] == 'gate':
            counts = verify_gate(directory, rows)
        elif campaign['kind'] == 'throughput':
            counts = verify_throughput(directory, ROOT / campaign['report'], rows)
            identities['native_build_source'] = source_identity(
                read(directory / 'native-build.json'), snapshot, index)
        else:
            counts = verify_detection(directory, rows)
        campaigns.append(dict(directory=campaign['directory'], counts=counts, source=identities))
    # The failed historical detector's tables stay visible even without a certified v3 snapshot.
    failed = verify_detection(ROOT / 'data/detection/validation-v1', [])
    assert failed == dict(registered=580, valid=530, invalid=50)
    repaired = [r for r in rows if r['study'] == 'confirmation-terminal-fix']
    assert len(repaired) == 30 and sum(r['attempted'] for r in repaired) == 10
    misses = [r for r in repaired if r['condition'] == 'sustained_50_early']
    assert len(misses) == 4 and all(r['classification'] == 'miss' for r in misses)
    assert all(r['valid'] and r['completed'] for r in repaired if r['attempted'])
    result = dict(schema='limer-public-verification-v1', public_files_checked=len(actual),
                  internal_symlinks_checked=len(links),
                  campaigns=campaigns, failed_detector_history=failed,
                  repaired_50_percent_capacity_misses=len(misses),
                  repair_locality=verify_repair_locality(),
                  scope='Public integrity, source identities and compact result derivation; no native runs or raw archive replay.')
    if out is not None:
        out.mkdir(parents=True, exist_ok=True)
        (out / 'generated.json').write_text(json.dumps(result, indent=2) + '\n')
        fields = list(dict.fromkeys(k for row in rows for k in row))
        with (out / 'summary.csv').open('w', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader(); writer.writerows(rows)
    print(json.dumps(result, indent=2))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-tables', type=Path)
    args = parser.parse_args()
    if not __debug__:
        parser.error('Run without Python optimization so integrity assertions are active')
    verify(args.write_tables)
