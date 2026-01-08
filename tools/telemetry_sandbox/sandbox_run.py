from __future__ import annotations
import argparse
import random
import time
from pathlib import Path

from telemetry_schema import TelemetryEvent, JsonlTelemetryWriter, now_ms

def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--minutes", type=int, default=5, help="How long to run the sandbox.")
    ap.add_argument("--seed", type=int, default=1337)
    args = ap.parse_args()

    random.seed(args.seed)

    session_id = f"demo_{args.minutes:02d}min_{int(time.time())}"
    out_dir = Path("tools/telemetry_sandbox/out")
    out_path = out_dir / f"telemetry_{session_id}.jsonl"
    writer = JsonlTelemetryWriter(out_path)

    tick_ms = 250
    total_ms = args.minutes * 60 * 1000
    ticks = total_ms // tick_ms

    # Internal simulation state
    ledger_entries = 0
    active_high_detail_branches = 1
    last_commit_ts = None

    # Baselines that drift as "player improves"
    precision = 0.55
    shockwave_radius = 1.0  # relative units

    start_ts = now_ms()
    for i in range(int(ticks)):
        ts = start_ts + i * tick_ms

        # Occasionally present an Impossible Split (HCE)
        if i % int((15_000 / tick_ms)) == 0 and i != 0:  # ~ every 15s
            node_count = 3
            writer.emit(TelemetryEvent(
                event="HCE_SIMULTANEOUS_GOODS_PRESENTED",
                ts_ms=ts,
                session_id=session_id,
                payload={"node_count": node_count, "time_pressure": round(random.uniform(0.6, 0.95), 2)}
            ))

            # Raise branch density briefly
            active_high_detail_branches = node_count
            writer.emit(TelemetryEvent(
                event="CCIP_BRANCH_DENSITY",
                ts_ms=ts + 5,
                session_id=session_id,
                payload={"active_high_detail_branches": active_high_detail_branches}
            ))

            # Commitment happens quickly after, pruning the others
            commit_delay = random.randint(900, 2400)
            last_commit_ts = ts + commit_delay
            writer.emit(TelemetryEvent(
                event="HCE_FIRST_COMMITMENT_LATCHED",
                ts_ms=last_commit_ts,
                session_id=session_id,
                payload={"time_to_commit_ms": commit_delay, "chosen_node": random.choice(["BRIDGE", "TRAIN", "FIRE"])}
            ))

            pruned = max(0, node_count - 1)
            if pruned:
                # Estimate CPU savings as a simple proxy
                cpu_saved = pruned * random.uniform(0.25, 0.40)  # "relative cycles saved"
                writer.emit(TelemetryEvent(
                    event="CCIP_PRUNE_EXECUTED",
                    ts_ms=last_commit_ts + 3,
                    session_id=session_id,
                    payload={"pruned_branches": pruned, "cpu_cycles_saved_estimate": round(cpu_saved, 3)}
                ))
            active_high_detail_branches = 1

            # Ledger logs Cost-of-Absence for the non-chosen goods
            for _ in range(pruned):
                ledger_entries += 1
                writer.emit(TelemetryEvent(
                    event="COST_LEDGER_APPEND",
                    ts_ms=last_commit_ts + 10,
                    session_id=session_id,
                    payload={"source": "REJECTED_NODE", "category": "COST_OF_ABSENCE", "weight": round(random.uniform(0.2, 0.8), 2)}
                ))

        # Simulate CCS samples (player gets more controlled over time)
        # Precision trends upward, shockwave trends downward
        precision += random.uniform(-0.003, 0.006)
        precision = clamp(precision, 0.40, 0.92)

        shockwave_radius += random.uniform(-0.006, 0.004)
        shockwave_radius = clamp(shockwave_radius, 0.55, 1.25)

        writer.emit(TelemetryEvent(
            event="CCS_PRECISION_SAMPLE",
            ts_ms=ts,
            session_id=session_id,
            payload={
                "precision_index": round(precision, 3),
                "shockwave_radius": round(shockwave_radius, 3),
                "speed_band": random.choice(["SUBSONIC", "TRANSONIC", "SUPERSONIC"]),
            }
        ))

        # Ledger structural cost sometimes occurs when shockwave is high
        if shockwave_radius > 1.05 and random.random() < 0.04:
            ledger_entries += 1
            writer.emit(TelemetryEvent(
                event="COST_LEDGER_APPEND",
                ts_ms=ts + 7,
                session_id=session_id,
                payload={"source": "STRUCTURAL", "category": "SONIC_DEBT", "weight": round(random.uniform(0.3, 1.0), 2)}
            ))

        # Compute W(x): (gain - lambda*cost) with gentle noise
        # Gain improves with precision; cost increases with shockwave
        gain = clamp(0.35 + 0.55 * precision + random.uniform(-0.05, 0.05), 0.0, 1.0)
        cost = clamp(0.25 + 0.55 * (shockwave_radius - 0.55) + random.uniform(-0.05, 0.06), 0.0, 1.0)
        lam = 1.0
        W = gain - lam * cost

        state = "STABLE" if W >= 0.10 else ("CRITICAL" if W >= 0 else "PRUNE_RISK")

        writer.emit(TelemetryEvent(
            event="W_EVALUATION_TICK",
            ts_ms=ts + 1,
            session_id=session_id,
            payload={
                "gain": round(gain, 3),
                "cost": round(cost, 3),
                "lambda": lam,
                "W_value": round(W, 3),
                "state": state
            }
        ))

    print(f"[OK] Wrote telemetry: {out_path}")
    print("[NEXT] Run analysis:")
    print(f"python3 tools/telemetry_sandbox/analyze_demo.py --input {out_path}")

if __name__ == "__main__":
    main()
