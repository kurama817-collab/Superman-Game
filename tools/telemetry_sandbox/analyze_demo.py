from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean
from typing import Any, Dict, List

from telemetry_schema import EventType


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze telemetry sandbox output")
    parser.add_argument("--input", required=True, help="Path to telemetry JSONL file")
    parser.add_argument(
        "--output",
        help="Optional path to write JSON report (defaults to tools/telemetry_sandbox/out/report_<session>.json)",
    )
    return parser


def load_events(path: Path) -> List[Dict[str, Any]]:
    events: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            events.append(json.loads(line))
    return events


def compute_report(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    w_ticks = [e for e in events if e["event"] == EventType.W_EVALUATION_TICK.value]
    ccs_samples = [e for e in events if e["event"] == EventType.CCS_PRECISION_SAMPLE.value]
    hce_goods = [e for e in events if e["event"] == EventType.HCE_SIMULTANEOUS_GOODS_PRESENTED.value]
    hce_commitments = [e for e in events if e["event"] == EventType.HCE_FIRST_COMMITMENT_LATCHED.value]
    ccip_density = [e for e in events if e["event"] == EventType.CCIP_BRANCH_DENSITY.value]
    ccip_prune = [e for e in events if e["event"] == EventType.CCIP_PRUNE_EXECUTED.value]
    ledger_entries = [e for e in events if e["event"] == EventType.COST_LEDGER_APPEND.value]

    w_values = [e["payload"]["w_value"] for e in w_ticks]
    tick_intervals = [
        w_ticks[i + 1]["ts_ms"] - w_ticks[i]["ts_ms"] for i in range(len(w_ticks) - 1)
    ]

    report = {
        "wx": {
            "tick_count": len(w_ticks),
            "avg_w_value": mean(w_values) if w_values else None,
            "avg_tick_interval_ms": mean(tick_intervals) if tick_intervals else None,
        },
        "ccs": {
            "sample_count": len(ccs_samples),
            "avg_precision": mean([e["payload"]["precision"] for e in ccs_samples])
            if ccs_samples
            else None,
        },
        "hce": {
            "goods_presented": sum(e["payload"]["goods_count"] for e in hce_goods)
            if hce_goods
            else 0,
            "commitments_latched": len(hce_commitments),
        },
        "ccip": {
            "avg_branch_density": mean([e["payload"]["density"] for e in ccip_density])
            if ccip_density
            else None,
            "prune_events": len(ccip_prune),
            "pruned_total": sum(e["payload"]["pruned"] for e in ccip_prune) if ccip_prune else 0,
        },
        "ledger": {
            "entries": len(ledger_entries),
            "total_cost": sum(e["payload"]["cost"] for e in ledger_entries)
            if ledger_entries
            else 0,
            "avg_cost": mean([e["payload"]["cost"] for e in ledger_entries])
            if ledger_entries
            else None,
        },
    }

    return report


def print_report(report: Dict[str, Any]) -> None:
    print("Telemetry Report")
    print("----------------")
    print(f"W(x) ticks: {report['wx']['tick_count']}")
    print(f"W(x) avg value: {report['wx']['avg_w_value']}")
    print(f"W(x) avg interval ms: {report['wx']['avg_tick_interval_ms']}")
    print(f"CCS samples: {report['ccs']['sample_count']}")
    print(f"CCS avg precision: {report['ccs']['avg_precision']}")
    print(f"HCE goods presented: {report['hce']['goods_presented']}")
    print(f"HCE commitments latched: {report['hce']['commitments_latched']}")
    print(f"CCIP avg branch density: {report['ccip']['avg_branch_density']}")
    print(f"CCIP prune events: {report['ccip']['prune_events']}")
    print(f"CCIP pruned total: {report['ccip']['pruned_total']}")
    print(f"Ledger entries: {report['ledger']['entries']}")
    print(f"Ledger total cost: {report['ledger']['total_cost']}")
    print(f"Ledger avg cost: {report['ledger']['avg_cost']}")


def default_report_path(input_path: Path) -> Path:
    name = input_path.stem
    if name.startswith("telemetry_"):
        session = name.replace("telemetry_", "", 1)
    else:
        session = name
    return input_path.parent / f"report_{session}.json"


def main() -> None:
    args = build_parser().parse_args()
    input_path = Path(args.input)
    events = load_events(input_path)
    report = compute_report(events)
    print_report(report)

    output_path = Path(args.output) if args.output else default_report_path(input_path)
    with output_path.open("w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print(f"Wrote report to {output_path}")


if __name__ == "__main__":
    main()
