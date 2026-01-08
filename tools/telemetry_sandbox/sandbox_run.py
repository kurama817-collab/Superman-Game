from __future__ import annotations

import argparse
import random
from pathlib import Path

from telemetry_schema import EventType, JsonlTelemetryWriter, TelemetryEvent, now_ms

TICK_INTERVAL_MS = 250


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Telemetry sandbox generator")
    parser.add_argument("--minutes", type=float, default=1.0, help="Duration in minutes")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for determinism")
    return parser


def generate_events(minutes: float, seed: int, session_id: str) -> list[TelemetryEvent]:
    rng = random.Random(seed)
    total_ms = int(minutes * 60 * 1000)
    ticks = max(1, total_ms // TICK_INTERVAL_MS)
    start_ms = now_ms()

    events: list[TelemetryEvent] = []

    for i in range(ticks):
        ts_ms = start_ms + i * TICK_INTERVAL_MS
        w_value = rng.uniform(0.5, 1.5)
        events.append(
            TelemetryEvent(
                event_type=EventType.W_EVALUATION_TICK,
                ts_ms=ts_ms,
                payload={"w_value": w_value},
                session_id=session_id,
            )
        )

        if i % 4 == 0:
            precision = rng.uniform(0.7, 0.99)
            events.append(
                TelemetryEvent(
                    event_type=EventType.CCS_PRECISION_SAMPLE,
                    ts_ms=ts_ms,
                    payload={"precision": precision},
                    session_id=session_id,
                )
            )

        if i % 10 == 0:
            goods_count = rng.randint(1, 6)
            events.append(
                TelemetryEvent(
                    event_type=EventType.HCE_SIMULTANEOUS_GOODS_PRESENTED,
                    ts_ms=ts_ms,
                    payload={"goods_count": goods_count},
                    session_id=session_id,
                )
            )

        if i % 15 == 0:
            commitment_id = rng.randint(1000, 9999)
            events.append(
                TelemetryEvent(
                    event_type=EventType.HCE_FIRST_COMMITMENT_LATCHED,
                    ts_ms=ts_ms,
                    payload={"commitment_id": commitment_id},
                    session_id=session_id,
                )
            )

        if i % 6 == 0:
            density = rng.uniform(0.1, 0.9)
            events.append(
                TelemetryEvent(
                    event_type=EventType.CCIP_BRANCH_DENSITY,
                    ts_ms=ts_ms,
                    payload={"density": density},
                    session_id=session_id,
                )
            )

        if i % 12 == 0:
            pruned = rng.randint(1, 5)
            events.append(
                TelemetryEvent(
                    event_type=EventType.CCIP_PRUNE_EXECUTED,
                    ts_ms=ts_ms,
                    payload={"pruned": pruned},
                    session_id=session_id,
                )
            )

        if i % 5 == 0:
            cost = rng.uniform(0.05, 1.2)
            events.append(
                TelemetryEvent(
                    event_type=EventType.COST_LEDGER_APPEND,
                    ts_ms=ts_ms,
                    payload={"cost": cost},
                    session_id=session_id,
                )
            )

    return events


def main() -> None:
    args = build_parser().parse_args()
    session_id = f"{now_ms()}_{args.seed}"
    output_path = Path(__file__).parent / "out" / f"telemetry_{session_id}.jsonl"

    events = generate_events(args.minutes, args.seed, session_id)

    with JsonlTelemetryWriter(output_path) as writer:
        writer.write_many(events)

    print(f"Wrote {len(events)} events to {output_path}")


if __name__ == "__main__":
    main()
