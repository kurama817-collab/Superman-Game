#!/usr/bin/env python3
"""Telemetry sandbox analyzer demo.

Reads a JSONL telemetry file, summarizes events and sessions, and optionally
writes a report JSON alongside the input file.
"""

import argparse
import json
import os
from typing import Any, Dict, Iterable, List, Optional


def build_out_path(inp_path: str) -> str:
    directory = os.path.dirname(inp_path)
    basename = os.path.basename(inp_path)

    if basename.startswith("telemetry_"):
        basename = basename[len("telemetry_") :]
    if basename.endswith(".jsonl"):
        basename = basename[: -len(".jsonl")]

    session_id = basename or "unknown"
    report_name = f"report_{session_id}.json"
    return os.path.join(directory, report_name)


def iter_jsonl(path: str) -> Iterable[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped:
                continue
            try:
                payload = json.loads(stripped)
            except json.JSONDecodeError:
                continue
            if isinstance(payload, dict):
                yield payload


def extract_session_id(event: Dict[str, Any]) -> Optional[str]:
    for key in ("session_id", "session", "sessionId"):
        value = event.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def extract_event_type(event: Dict[str, Any]) -> str:
    value = event.get("event") or event.get("type") or "unknown"
    return value if isinstance(value, str) else "unknown"


def extract_w_value(event: Dict[str, Any]) -> Optional[float]:
    for key in ("W", "w", "W_x", "w_x"):
        value = event.get(key)
        if isinstance(value, (int, float)):
            return float(value)
    return None


def extract_w_state(event: Dict[str, Any]) -> Optional[str]:
    value = event.get("state") or event.get("w_state")
    if isinstance(value, str) and value:
        return value
    return None


def summarize_events(events: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    event_counts: Dict[str, int] = {}
    sessions: List[str] = []
    session_set = set()
    w_values: List[float] = []
    w_state_counts: Dict[str, int] = {}

    for event in events:
        event_type = extract_event_type(event)
        event_counts[event_type] = event_counts.get(event_type, 0) + 1

        session_id = extract_session_id(event)
        if session_id and session_id not in session_set:
            session_set.add(session_id)
            sessions.append(session_id)

        w_value = extract_w_value(event)
        if w_value is not None:
            w_values.append(w_value)
            state = extract_w_state(event)
            if state:
                w_state_counts[state] = w_state_counts.get(state, 0) + 1

    w_stats: Dict[str, Any] = {"count": len(w_values)}
    if w_values:
        w_stats.update(
            {
                "min": min(w_values),
                "mean": sum(w_values) / len(w_values),
                "max": max(w_values),
                "state_counts": w_state_counts,
            }
        )
    else:
        w_stats["state_counts"] = w_state_counts

    return {
        "sessions": {"count": len(sessions), "ids": sessions},
        "event_counts": event_counts,
        "w_stats": w_stats,
    }


def write_report(output_path: str, report: Dict[str, Any]) -> None:
    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)
        handle.write("\n")


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Telemetry sandbox analyzer")
    parser.add_argument(
        "--input",
        "--inp",
        dest="input_path",
        required=True,
        help="Path to a telemetry JSONL file",
    )
    parser.add_argument(
        "--write_json",
        action="store_true",
        help="Write summary report alongside the input",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    events = list(iter_jsonl(args.input_path))
    report = summarize_events(events)

    if args.write_json:
        output_path = build_out_path(args.input_path)
        write_report(output_path, report)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
