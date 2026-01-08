from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any, Dict, List

SESSION_RE = re.compile(r"telemetry_(?P<session>[a-f0-9]+)\.jsonl$")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze telemetry JSONL output.")
    parser.add_argument("--input", required=True, help="Path to telemetry JSONL.")
    parser.add_argument(
        "--write_json",
        action="store_true",
        help="Write report JSON to tools/telemetry_sandbox/out/report_<session>.json",
    )
    return parser


def load_events(path: Path) -> List[Dict[str, Any]]:
    events: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                events.append(json.loads(line))
    return events


def summarize(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_type: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for event in events:
        by_type[event.get("event_type", "Unknown")].append(event)

    summary: Dict[str, Any] = {}
    summary["W(x)"] = {
        "count": len(by_type.get("W(x)", [])),
        "avg_value": mean([e["payload"]["value"] for e in by_type.get("W(x)", [])])
        if by_type.get("W(x)")
        else 0,
    }
    summary["CCS"] = {
        "count": len(by_type.get("CCS", [])),
        "avg_score": mean([e["payload"]["score"] for e in by_type.get("CCS", [])])
        if by_type.get("CCS")
        else 0,
    }
    summary["HCE"] = {
        "count": len(by_type.get("HCE", [])),
        "avg_efficiency": mean(
            [e["payload"]["efficiency"] for e in by_type.get("HCE", [])]
        )
        if by_type.get("HCE")
        else 0,
    }
    summary["CCIP"] = {
        "count": len(by_type.get("CCIP", [])),
        "avg_signal": mean([e["payload"]["signal"] for e in by_type.get("CCIP", [])])
        if by_type.get("CCIP")
        else 0,
    }
    summary["Ledger"] = {
        "count": len(by_type.get("Ledger", [])),
        "avg_transactions": mean(
            [e["payload"]["transactions"] for e in by_type.get("Ledger", [])]
        )
        if by_type.get("Ledger")
        else 0,
    }
    return summary


def print_summary(summary: Dict[str, Any]) -> None:
    print("Telemetry summary")
    order = ["W(x)", "CCS", "Ledger", "HCE", "CCIP"]
    for key in order:
        metrics = summary.get(key, {})
        detail = ", ".join(f"{name}={value}" for name, value in metrics.items())
        print(f"- {key}: {detail}")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    input_path = Path(args.input)
    events = load_events(input_path)
    summary = summarize(events)
    print_summary(summary)

    if args.write_json:
        match = SESSION_RE.search(str(input_path))
        session = match.group("session") if match else "session"
        report_path = input_path.parent / f"report_{session}.json"
        report_path.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
        print(f"Wrote {report_path}")


if __name__ == "__main__":
    main()
