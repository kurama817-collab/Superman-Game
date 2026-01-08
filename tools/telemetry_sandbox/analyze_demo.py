from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from typing import Any, Dict, List


def read_jsonl(path: str) -> List[Dict[str, Any]]:
    events: List[Dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            events.append(json.loads(line))
    return events


def analyze(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    counts = Counter(e.get("event") for e in events)
    session_ids = sorted(set(e.get("session_id") for e in events if e.get("session_id")))

    wx_vals = []
    wx_states = Counter()
    ccs_precision = []
    ledger_weights = []
    hce_commit_times = []
    prunes = 0
    cpu_saved = 0.0
    branch_density = []

    for e in events:
        ev = e.get("event")
        payload = e.get("payload") or {}

        if ev == "W_EVALUATION_TICK":
            wx_vals.append(payload.get("W_value"))
            wx_states[payload.get("state", "UNKNOWN")] += 1

        elif ev == "CCS_PRECISION_SAMPLE":
            ccs_precision.append(payload.get("precision_index"))

        elif ev == "COST_LEDGER_APPEND":
            ledger_weights.append(payload.get("weight"))

        elif ev == "HCE_FIRST_COMMITMENT_LATCHED":
            hce_commit_times.append(payload.get("time_to_commit_ms"))

        elif ev == "CCIP_PRUNE_EXECUTED":
            prunes += int(payload.get("pruned_branches", 0))
            cpu_saved += float(payload.get("cpu_cycles_saved_estimate", 0.0))

        elif ev == "CCIP_BRANCH_DENSITY":
            branch_density.append(payload.get("active_high_detail_branches"))

    def safe_mean(xs):
        xs = [x for x in xs if isinstance(x, (int, float))]
        return (sum(xs) / len(xs)) if xs else 0.0

    report = {
        "sessions": session_ids,
        "event_counts": dict(sorted(counts.items(), key=lambda kv: kv[0] or "")),
        "W(x)": {
            "mean_W": round(safe_mean(wx_vals), 4),
            "min_W": round(min(wx_vals), 4) if wx_vals else 0.0,
            "max_W": round(max(wx_vals), 4) if wx_vals else 0.0,
            "state_counts": dict(sorted(wx_states.items(), key=lambda kv: kv[0])),
        },
        "CCS": {
            "mean_precision_index": round(safe_mean(ccs_precision), 4),
        },
        "Ledger": {
            "entries": len(ledger_weights),
            "total_weight": round(sum([w for w in ledger_weights if isinstance(w, (int, float))]), 4),
        },
        "HCE": {
            "commit_events": len(hce_commit_times),
            "mean_time_to_commit_ms": round(safe_mean(hce_commit_times), 2),
        },
        "CCIP": {
            "total_pruned_branches": prunes,
            "cpu_cycles_saved_estimate_total": round(cpu_saved, 1),
            "mean_branch_density": round(safe_mean(branch_density), 4),
        },
    }

    return report


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--write_json", action="store_true")
    args = ap.parse_args()

    events = read_jsonl(args.inp)
    report = analyze(events)

    print(json.dumps(report, indent=2, sort_keys=True))

    if args.write_json:
        # Derive session from filename if possible
        session_id = "session"
        base = args.inp.replace("\\", "/").split("/")[-1]
        if base.startswith("telemetry_") and base.endswith(".jsonl"):
            session_id = base[len("telemetry_") : -len(".jsonl")]

        out_path = args.inp.replace("telemetry_", "report_").replace(".jsonl", ".json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, sort_keys=True)
        print(out_path)


if __name__ == "__main__":
    main()
