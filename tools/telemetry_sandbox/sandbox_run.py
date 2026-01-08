from __future__ import annotations

import argparse
import os
import random

from telemetry_schema import EventType, JsonlTelemetryWriter, TelemetryEvent

TICK_INTERVAL_MS = 250


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Emit demo telemetry events.")
    parser.add_argument("--minutes", type=int, default=1, help="Duration in minutes.")
    parser.add_argument("--seed", type=int, default=1337, help="Random seed.")
    parser.add_argument("--session", type=str, default=None, help="Session ID override.")
    return parser.parse_args()


def build_session_id(minutes: int, seed: int, override: str | None) -> str:
    if override:
        return override
    return f"demo_{minutes:02d}min_seed{seed}"


def main() -> None:
    args = parse_args()
    session_id = build_session_id(args.minutes, args.seed, args.session)
    output_dir = os.path.join(os.path.dirname(__file__), "out")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"telemetry_{session_id}.jsonl")

    rng = random.Random(args.seed)
    writer = JsonlTelemetryWriter(output_path)

    total_ticks = int(args.minutes * 60 * 1000 / TICK_INTERVAL_MS)
    timestamp_ms = 0
    for tick in range(total_ticks):
        state = rng.choice(["idle", "scan", "combat", "recover"])
        payload = {
            "tick": tick,
            "state": state,
            "energy": rng.randint(0, 100),
        }
        writer.write_event(
            TelemetryEvent(
                event_type=EventType.W_X,
                timestamp_ms=timestamp_ms,
                session_id=session_id,
                payload=payload,
            )
        )

        if tick % 40 == 0:
            writer.write_event(
                TelemetryEvent(
                    event_type=EventType.CCS,
                    timestamp_ms=timestamp_ms,
                    session_id=session_id,
                    payload={"checkpoint": tick // 40, "status": "ok"},
                )
            )

        if tick % 55 == 0:
            writer.write_event(
                TelemetryEvent(
                    event_type=EventType.HCE,
                    timestamp_ms=timestamp_ms,
                    session_id=session_id,
                    payload={
                        "event": rng.choice(["spawn", "impact", "alert"]),
                        "severity": rng.choice(["low", "med", "high"]),
                    },
                )
            )

        if tick % 70 == 0:
            writer.write_event(
                TelemetryEvent(
                    event_type=EventType.CCIP,
                    timestamp_ms=timestamp_ms,
                    session_id=session_id,
                    payload={"policy": rng.choice(["alpha", "beta", "gamma"])},
                )
            )

        if tick % 90 == 0:
            writer.write_event(
                TelemetryEvent(
                    event_type=EventType.LEDGER,
                    timestamp_ms=timestamp_ms,
                    session_id=session_id,
                    payload={
                        "source": rng.choice(["bridge", "engine", "ops"]),
                        "delta": rng.randint(-5, 5),
                    },
                )
            )

        timestamp_ms += TICK_INTERVAL_MS

    print(f"Wrote telemetry to {output_path}")


if __name__ == "__main__":
    main()
