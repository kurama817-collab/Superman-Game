from __future__ import annotations

import json
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable


class EventType(str, Enum):
    W_EVALUATION_TICK = "W_EVALUATION_TICK"
    CCS_PRECISION_SAMPLE = "CCS_PRECISION_SAMPLE"
    HCE_SIMULTANEOUS_GOODS_PRESENTED = "HCE_SIMULTANEOUS_GOODS_PRESENTED"
    HCE_FIRST_COMMITMENT_LATCHED = "HCE_FIRST_COMMITMENT_LATCHED"
    CCIP_BRANCH_DENSITY = "CCIP_BRANCH_DENSITY"
    CCIP_PRUNE_EXECUTED = "CCIP_PRUNE_EXECUTED"
    COST_LEDGER_APPEND = "COST_LEDGER_APPEND"


def now_ms() -> int:
    return int(time.time() * 1000)


@dataclass(frozen=True)
class TelemetryEvent:
    event_type: EventType
    ts_ms: int
    payload: Dict[str, Any]
    session_id: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event": self.event_type.value,
            "ts_ms": self.ts_ms,
            "session_id": self.session_id,
            "payload": self.payload,
        }


class JsonlTelemetryWriter:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._fh = self.path.open("w", encoding="utf-8")

    def write(self, event: TelemetryEvent) -> None:
        self._fh.write(json.dumps(event.to_dict()) + "\n")

    def write_many(self, events: Iterable[TelemetryEvent]) -> None:
        for event in events:
            self.write(event)

    def close(self) -> None:
        self._fh.close()

    def __enter__(self) -> "JsonlTelemetryWriter":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
