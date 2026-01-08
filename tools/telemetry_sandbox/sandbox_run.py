from __future__ import annotations

import argparse
import random
from pathlib import Path

from telemetry_schema import EventType, JsonlTelemetryWriter, TelemetryEvent, now_ms

OUT_DIR = Path(__file__).resolve().parent / "out"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Emit deterministic telemetry JSONL.")
    parser.add_argument("--minutes", type=int, default=5, help="Minutes to simulate.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    return parser


def generate_events(minutes: int, rng: random.Random, session_id: str) -> list[TelemetryEvent]:
    events: list[TelemetryEvent] = []
    base_timestamp = now_ms()
    for minute in range(minutes):
        offset_ms = minute * 60_000
        workload = rng.uniform(0.4, 0.95)
        ccs = rng.randint(70, 110)
        hce = rng.uniform(0.6, 0.98)
        ccip = rng.uniform(0.2, 0.7)
        ledger_ops = rng.randint(8, 20)
        events.extend(
            [
                TelemetryEvent(
                    event_type=EventType.WORKLOAD,
                    timestamp_ms=base_timestamp + offset_ms + rng.randint(0, 5000),
                    session_id=session_id,
                    payload={"minute": minute, "value": round(workload, 3)},
                ),
                TelemetryEvent(
                    event_type=EventType.CCS,
                    timestamp_ms=base_timestamp + offset_ms + rng.randint(5000, 10000),
                    session_id=session_id,
                    payload={"minute": minute, "score": ccs},
                ),
                TelemetryEvent(
                    event_type=EventType.HCE,
                    timestamp_ms=base_timestamp + offset_ms + rng.randint(10000, 15000),
                    session_id=session_id,
                    payload={"minute": minute, "efficiency": round(hce, 3)},
                ),
                TelemetryEvent(
                    event_type=EventType.CCIP,
                    timestamp_ms=base_timestamp + offset_ms + rng.randint(15000, 20000),
                    session_id=session_id,
                    payload={"minute": minute, "signal": round(ccip, 3)},
                ),
                TelemetryEvent(
                    event_type=EventType.LEDGER,
                    timestamp_ms=base_timestamp + offset_ms + rng.randint(20000, 25000),
                    session_id=session_id,
                    payload={"minute": minute, "transactions": ledger_ops},
                ),
            ]
        )
    return events


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    rng = random.Random(args.seed)
    session_id = "".join(rng.choice("0123456789abcdef") for _ in range(8))
    output_path = OUT_DIR / f"telemetry_{session_id}.jsonl"

    writer = JsonlTelemetryWriter(output_path)
    for event in generate_events(args.minutes, rng, session_id):
        writer.write_event(event)

    print(str(output_path))


if __name__ == "__main__":
    main()
