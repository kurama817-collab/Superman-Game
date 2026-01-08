"""Run a deterministic telemetry sandbox for Protocol Ψ analytics."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import math
from pathlib import Path
import random

from telemetry_schema import JsonlTelemetryWriter, TelemetryEvent

OUT_DIR = Path(__file__).resolve().parent / "out"
TICK_MS = 250


@dataclass
class SandboxConfig:
    minutes: int
    seed: int

    @property
    def session_id(self) -> str:
        return f"sandbox_{self.minutes}m_seed{self.seed}"


def simulate(config: SandboxConfig, writer: JsonlTelemetryWriter) -> None:
    rng = random.Random(config.seed)
    total_ms = config.minutes * 60 * 1000
    steps = total_ms // TICK_MS
    session_id = config.session_id

    for step in range(int(steps)):
        ts_ms = step * TICK_MS
        phase = ts_ms / 1000.0

        wx_value = math.sin(phase / 3.5) + rng.uniform(-0.15, 0.15)
        writer.write(
            TelemetryEvent(
                event="wx_tick",
                ts_ms=ts_ms,
                session_id=session_id,
                payload={"value": round(wx_value, 4)},
            )
        )

        if step % 2 == 0:
            ccs_precision = max(0.0, min(1.0, 0.92 + rng.uniform(-0.08, 0.05)))
            shockwave_radius = 12 + 4 * math.cos(phase / 2.0) + rng.uniform(-0.5, 0.5)
            writer.write(
                TelemetryEvent(
                    event="ccs_sample",
                    ts_ms=ts_ms,
                    session_id=session_id,
                    payload={
                        "precision": round(ccs_precision, 4),
                        "shockwave_radius": round(shockwave_radius, 3),
                    },
                )
            )

        if ts_ms % 20_000 == 0 and ts_ms > 0:
            commit_time_ms = rng.randint(80, 220)
            writer.write(
                TelemetryEvent(
                    event="hce_impossible_split",
                    ts_ms=ts_ms,
                    session_id=session_id,
                    payload={"commit_ms": commit_time_ms},
                )
            )

        if ts_ms % 1000 == 0:
            branch_density = 2.5 + 1.5 * math.sin(phase / 5.0) + rng.uniform(-0.2, 0.2)
            writer.write(
                TelemetryEvent(
                    event="ccip_branch",
                    ts_ms=ts_ms,
                    session_id=session_id,
                    payload={"branch_density": round(branch_density, 4)},
                )
            )

        if ts_ms % 10_000 == 0 and ts_ms > 0:
            pruned = rng.randint(1, 4)
            writer.write(
                TelemetryEvent(
                    event="ccip_prune",
                    ts_ms=ts_ms,
                    session_id=session_id,
                    payload={"pruned_branches": pruned},
                )
            )

        if ts_ms % 750 == 0:
            sources = ["player", "system", "npc"]
            source = sources[(step // 3) % len(sources)]
            cost_of_absence = rng.random() < 0.08
            entry_type = "cost_of_absence" if cost_of_absence else "state_delta"
            writer.write(
                TelemetryEvent(
                    event="ledger_append",
                    ts_ms=ts_ms,
                    session_id=session_id,
                    payload={
                        "source": source,
                        "entry_type": entry_type,
                        "cost_of_absence": cost_of_absence,
                    },
                )
            )


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Protocol Ψ telemetry sandbox.")
    parser.add_argument("--minutes", type=int, required=True, help="Minutes to simulate.")
    parser.add_argument("--seed", type=int, default=7, help="Deterministic seed.")
    return parser


def main() -> None:
    args = build_arg_parser().parse_args()
    config = SandboxConfig(minutes=args.minutes, seed=args.seed)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUT_DIR / f"telemetry_{config.session_id}.jsonl"
    with output_path.open("a", encoding="utf-8") as handle:
        writer = JsonlTelemetryWriter(handle)
        simulate(config, writer)
    print(f"Telemetry written to {output_path}")


if __name__ == "__main__":
    main()
