from __future__ import annotations

import argparse
import os
import random
from typing import Dict, Any

from telemetry_schema import EventType, TelemetryEvent, JsonlTelemetryWriter

TICK_INTERVAL_MS = 250  # concrete cadence


def build_session_id(minutes: int, seed: int) -> str:
    return f"demo_{minutes:02d}min_seed{seed}"


def deterministic_base_ts_ms(seed: int) -> int:
    # Deterministic "epoch" derived from seed; stable across runs
    # Keep it large enough to look realistic but never wall-clock.
    return 1_700_000_000_000 + (seed * 10_000)


def emit_events(writer: JsonlTelemetryWriter, session_id: str, minutes: int, seed: int) -> str:
    rng = random.Random(seed)
    base_ts = deterministic_base_ts_ms(seed)

    total_ticks = int((minutes * 60 * 1000) / TICK_INTERVAL_MS)

    # Simple state for demo
    active_branches = 3
    ledger_total = 0.0
    prune_count = 0

    for i in range(total_ticks):
        ts = base_ts + (i * TICK_INTERVAL_MS)

        # W(x) tick
        gain = rng.uniform(0.40, 0.95)
        cost = rng.uniform(0.20, 0.90)
        w_val = gain - cost
        state = "STABLE" if w_val >= 0.10 else ("CRITICAL" if w_val >= 0.0 else "PRUNE_RISK")

        writer.write(
            TelemetryEvent(
                event=EventType.W_EVALUATION_TICK.value,
                ts_ms=ts,
                session_id=session_id,
                payload={
                    "gain": round(gain, 3),
                    "cost": round(cost, 3),
                    "lambda": 1.0,
                    "W_value": round(w_val, 3),
                    "state": state,
                },
            )
        )

        # CCS sample
        precision = rng.uniform(0.45, 0.90)
        shockwave = rng.uniform(0.55, 1.20)
        band = "SUPERSONIC" if shockwave > 1.0 else "SUBSONIC"

        writer.write(
            TelemetryEvent(
                event=EventType.CCS_PRECISION_SAMPLE.value,
                ts_ms=ts,
                session_id=session_id,
                payload={
                    "precision_index": round(precision, 3),
                    "shockwave_radius": round(shockwave, 3),
                    "speed_band": band,
                },
            )
        )

        # Periodically present an Impossible Split + commitment latch
        if i % 20 == 0:
            node_count = 2
            time_pressure = rng.uniform(0.6, 1.0)
            writer.write(
                TelemetryEvent(
                    event=EventType.HCE_SIMULTANEOUS_GOODS_PRESENTED.value,
                    ts_ms=ts,
                    session_id=session_id,
                    payload={"node_count": node_count, "time_pressure": round(time_pressure, 3)},
                )
            )

            time_to_commit = rng.randint(350, 2800)
            chosen = "A" if rng.random() < 0.5 else "B"
            writer.write(
                TelemetryEvent(
                    event=EventType.HCE_FIRST_COMMITMENT_LATCHED.value,
                    ts_ms=ts + time_to_commit,
                    session_id=session_id,
                    payload={"time_to_commit_ms": time_to_commit, "chosen_node": chosen},
                )
            )

        # CCIP branch density + prune behavior
        # Simulate that when W goes negative, we prune branches and estimate CPU saved.
        writer.write(
            TelemetryEvent(
                event=EventType.CCIP_BRANCH_DENSITY.value,
                ts_ms=ts,
                session_id=session_id,
                payload={"active_high_detail_branches": active_branches},
            )
        )

        if w_val < 0.0:
            pruned = rng.randint(1, 3)
            prune_count += pruned
            active_branches = max(1, active_branches - pruned)
            cpu_saved = float(pruned) * rng.uniform(1000.0, 6000.0)

            writer.write(
                TelemetryEvent(
                    event=EventType.CCIP_PRUNE_EXECUTED.value,
                    ts_ms=ts,
                    session_id=session_id,
                    payload={
                        "pruned_branches": pruned,
                        "cpu_cycles_saved_estimate": round(cpu_saved, 1),
                    },
                )
            )

            # Ledger append due to cost/absence (simplified)
            weight = rng.uniform(0.2, 1.0)
            ledger_total += weight
            writer.write(
                TelemetryEvent(
                    event=EventType.COST_LEDGER_APPEND.value,
                    ts_ms=ts,
                    session_id=session_id,
                    payload={
                        "source": "STRUCTURAL",
                        "category": "SONIC_DEBT",
                        "weight": round(weight, 3),
                    },
                )
            )

    writer.flush()
    return session_id


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--minutes", type=int, default=1)
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--session", type=str, default="")
    args = ap.parse_args()

    minutes = max(1, args.minutes)
    seed = int(args.seed)

    session_id = args.session.strip() if args.session.strip() else build_session_id(minutes, seed)

    out_dir = os.path.join("tools", "telemetry_sandbox", "out")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"telemetry_{session_id}.jsonl")

    # IMPORTANT: open in 'w' to overwrite for determinism
    with open(out_path, "w", encoding="utf-8") as f:
        writer = JsonlTelemetryWriter(f)
        emit_events(writer, session_id, minutes, seed)

    print(out_path)


if __name__ == "__main__":
    main()
