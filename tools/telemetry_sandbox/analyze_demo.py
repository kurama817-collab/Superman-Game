from __future__ import annotations
import argparse
import json
from collections import defaultdict
import statistics as stats
from pathlib import Path

def safe_mean(xs):
    return stats.mean(xs) if xs else None

def read_events(path: Path):
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Path to telemetry JSONL file")
    ap.add_argument("--write_json", action="store_true", help="Also write report_<session>.json to out/")
    args = ap.parse_args()

    in_path = Path(args.input)
    w_values = []
    w_states = defaultdict(int)
    w_negative_ms = 0
    last_w_ts = None
    last_w_val = None

    ccs_precision = []
    shockwave_samples = []

    ledger_total = 0
    ledger_by_source = defaultdict(int)
    cost_of_absence = 0

    hce_splits = 0
    hce_commit_times = []

    branch_density = []
    prunes = 0
    cpu_saved = []

    session_id = None

    for e in read_events(in_path):
        session_id = session_id or e.get("session_id")
        ev = e.get("event")
        ts = e.get("ts_ms")
        p = e.get("payload", {})

        if ev == "W_EVALUATION_TICK":
            W = float(p.get("W_value", 0.0))
            w_values.append(W)
            st = p.get("state", "UNKNOWN")
            w_states[st] += 1

            if last_w_ts is not None and last_w_val is not None:
                dt = ts - last_w_ts
                if last_w_val < 0:
                    w_negative_ms += max(dt, 0)
            last_w_ts = ts
            last_w_val = W

        elif ev == "CCS_PRECISION_SAMPLE":
            if "precision_index" in p:
                ccs_precision.append(float(p["precision_index"]))
            if "shockwave_radius" in p:
                shockwave_samples.append(float(p["shockwave_radius"]))

        elif ev == "COST_LEDGER_APPEND":
            ledger_total += 1
            src = p.get("source", "UNKNOWN")
            ledger_by_source[src] += 1
            if src == "REJECTED_NODE":
                cost_of_absence += 1

        elif ev == "HCE_SIMULTANEOUS_GOODS_PRESENTED":
            hce_splits += 1

        elif ev == "HCE_FIRST_COMMITMENT_LATCHED":
            if "time_to_commit_ms" in p:
                hce_commit_times.append(int(p["time_to_commit_ms"]))

        elif ev == "CCIP_BRANCH_DENSITY":
            if "active_high_detail_branches" in p:
                branch_density.append(float(p["active_high_detail_branches"]))

        elif ev == "CCIP_PRUNE_EXECUTED":
            prunes += 1
            if "cpu_cycles_saved_estimate" in p:
                cpu_saved.append(float(p["cpu_cycles_saved_estimate"]))

    report = {
        "session_id": session_id,
        "input": str(in_path),
        "W(x)": {
            "avg": safe_mean(w_values),
            "min": min(w_values) if w_values else None,
            "max": max(w_values) if w_values else None,
            "time_below_zero_ms": w_negative_ms,
            "state_counts": dict(w_states),
            "tick_count": len(w_values),
        },
        "CCS": {
            "precision_avg": safe_mean(ccs_precision),
            "shockwave_avg": safe_mean(shockwave_samples),
            "precision_samples": len(ccs_precision),
        },
        "Ledger": {
            "total_entries": ledger_total,
            "by_source": dict(ledger_by_source),
            "cost_of_absence_entries": cost_of_absence,
        },
        "HCE": {
            "impossible_splits_presented": hce_splits,
            "avg_time_to_commit_ms": safe_mean(hce_commit_times),
            "commit_samples": len(hce_commit_times),
        },
        "CCIP": {
            "avg_high_detail_branch_density": safe_mean(branch_density),
            "prune_events": prunes,
            "avg_cpu_cycles_saved_estimate": safe_mean(cpu_saved),
        }
    }

    print(json.dumps(report, indent=2))

    if args.write_json and session_id:
        out_dir = Path("tools/telemetry_sandbox/out")
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"report_{session_id}.json"
        out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"[OK] Wrote report: {out_path}")

if __name__ == "__main__":
    main()
