"""Analyze Protocol Ψ telemetry sandbox output."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Iterable

TICK_MS = 250


def load_events(path: Path) -> Iterable[Dict[str, object]]:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def summarize(events: Iterable[Dict[str, object]]) -> Dict[str, object]:
    wx_values = []
    wx_below_zero = 0

    ccs_precision = []
    ccs_radius = []

    ledger_total = 0
    ledger_by_source: Dict[str, int] = {}
    ledger_cost_absence = 0

    hce_count = 0
    hce_commit_total = 0

    ccip_density = []
    ccip_prune_count = 0
    ccip_pruned_total = 0

    for event in events:
        event_type = event.get("event")
        payload = event.get("payload", {})

        if event_type == "wx_tick":
            value = float(payload.get("value", 0.0))
            wx_values.append(value)
            if value < 0:
                wx_below_zero += 1
        elif event_type == "ccs_sample":
            ccs_precision.append(float(payload.get("precision", 0.0)))
            ccs_radius.append(float(payload.get("shockwave_radius", 0.0)))
        elif event_type == "ledger_append":
            ledger_total += 1
            source = str(payload.get("source", "unknown"))
            ledger_by_source[source] = ledger_by_source.get(source, 0) + 1
            if payload.get("cost_of_absence"):
                ledger_cost_absence += 1
        elif event_type == "hce_impossible_split":
            hce_count += 1
            hce_commit_total += int(payload.get("commit_ms", 0))
        elif event_type == "ccip_branch":
            ccip_density.append(float(payload.get("branch_density", 0.0)))
        elif event_type == "ccip_prune":
            ccip_prune_count += 1
            ccip_pruned_total += int(payload.get("pruned_branches", 0))

    wx_avg = sum(wx_values) / len(wx_values) if wx_values else 0.0
    wx_min = min(wx_values) if wx_values else 0.0
    wx_max = max(wx_values) if wx_values else 0.0
    wx_below_zero_ms = wx_below_zero * TICK_MS

    ccs_precision_avg = sum(ccs_precision) / len(ccs_precision) if ccs_precision else 0.0
    ccs_radius_avg = sum(ccs_radius) / len(ccs_radius) if ccs_radius else 0.0

    hce_avg_commit = hce_commit_total / hce_count if hce_count else 0.0

    ccip_density_avg = sum(ccip_density) / len(ccip_density) if ccip_density else 0.0
    cpu_savings_estimate = ccip_pruned_total * 4.5

    return {
        "wx": {
            "avg": round(wx_avg, 4),
            "min": round(wx_min, 4),
            "max": round(wx_max, 4),
            "time_below_zero_ms": wx_below_zero_ms,
        },
        "ccs": {
            "precision_avg": round(ccs_precision_avg, 4),
            "shockwave_radius_avg": round(ccs_radius_avg, 4),
        },
        "ledger": {
            "total_entries": ledger_total,
            "by_source": ledger_by_source,
            "cost_of_absence_count": ledger_cost_absence,
        },
        "hce": {
            "impossible_split_count": hce_count,
            "avg_commit_ms": round(hce_avg_commit, 2),
        },
        "ccip": {
            "branch_density_avg": round(ccip_density_avg, 4),
            "prune_count": ccip_prune_count,
            "cpu_savings_estimate": round(cpu_savings_estimate, 2),
        },
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze Protocol Ψ telemetry.")
    parser.add_argument("--input", required=True, help="Path to telemetry JSONL file.")
    parser.add_argument(
        "--write-report",
        action="store_true",
        help="Write report JSON next to telemetry output.",
    )
    return parser


def main() -> None:
    args = build_arg_parser().parse_args()
    input_path = Path(args.input)
    events = list(load_events(input_path))
    report = summarize(events)
    print(json.dumps(report, indent=2))

    if args.write_report:
        name = input_path.stem
        session = name.replace("telemetry_", "") if name.startswith("telemetry_") else name
        output_path = input_path.parent / f"report_{session}.json"
        with output_path.open("w", encoding="utf-8") as handle:
            json.dump(report, handle, indent=2)
        print(f"Report written to {output_path}")


if __name__ == "__main__":
    main()
