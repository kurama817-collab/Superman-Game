from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, Any, Literal
import json
import time
from pathlib import Path

EventType = Literal[
    "W_EVALUATION_TICK",
    "HCE_SIMULTANEOUS_GOODS_PRESENTED",
    "HCE_FIRST_COMMITMENT_LATCHED",
    "CCIP_BRANCH_DENSITY",
    "CCIP_PRUNE_EXECUTED",
    "COST_LEDGER_APPEND",
    "CCS_PRECISION_SAMPLE",
]

@dataclass(frozen=True)
class TelemetryEvent:
    event: EventType
    ts_ms: int
    session_id: str
    payload: Dict[str, Any]

    def to_json(self) -> str:
        return json.dumps(asdict(self), separators=(",", ":"), ensure_ascii=False)

def now_ms() -> int:
    return int(time.time() * 1000)

class JsonlTelemetryWriter:
    """Append-only JSONL writer (one event per line)."""
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def emit(self, event: TelemetryEvent) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(event.to_json() + "\n")
