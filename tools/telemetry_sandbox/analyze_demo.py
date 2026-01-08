from __future__ import annotations

import argparse
import json
from collections import defaultdict
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze demo telemetry output.")
    parser.add_argument("--input", required=True, help="Input JSONL file.")
    parser.add_argument("--write_json", action="store_true", help="Write JSON report.")
    return parser.parse_args()


def load_events(path: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                events.append(json.loads(line))
    return events


def analyze(events: list[dict[str, Any]]) -> dict[str, Any]:
    counts: dict[str, int] = defaultdict(int)
    w_state_counts: dict[str, int] = defaultdict(int)
    ledger_by_source: dict[str, int] = defaultdict(int)

    for event in events:
        event_type = event.get("event_type", "UNKNOWN")
        counts[event_type] += 1
        payload = event.get("payload", {})

        if event_type == "W_X":
            state = payload.get("state", "unknown")
            w_state_counts[state] += 1
        elif event_type == "LEDGER":
            source = payload.get("source", "unknown")
            ledger_by_source[source] += 1

    report = {
        "summary": dict(sorted(counts.items())),
        "w_x": {
            "state_counts": dict(sorted(w_state_counts.items())),
        },
        "ledger": {
            "by_source": dict(sorted(ledger_by_source.items())),
        },
    }
    return report


def write_report(report: dict[str, Any], input_path: str) -> str:
    base_name = input_path.rsplit("/", 1)[-1]
    session_name = base_name.replace("telemetry_", "").replace(".jsonl", "")
    output_path = f"report_{session_name}.json"
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(json.dumps(report, indent=2, sort_keys=True))
        handle.write("\n")
    return output_path


def main() -> None:
    args = parse_args()
    events = load_events(args.input)
    report = analyze(events)

    print(json.dumps(report, indent=2, sort_keys=True))

    if args.write_json:
        output_path = write_report(report, args.input)
        print(f"Wrote report to {output_path}")


if __name__ == "__main__":
    main()
