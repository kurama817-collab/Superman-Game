from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict


class EventType(str, Enum):
    WORKLOAD = "W(x)"
    CCS = "CCS"
    HCE = "HCE"
    CCIP = "CCIP"
    LEDGER = "Ledger"


@dataclass
class TelemetryEvent:
    event_type: EventType
    timestamp_ms: int
    session_id: str
    payload: Dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> str:
        data = asdict(self)
        data["event_type"] = self.event_type.value
        return json.dumps(data, sort_keys=True)


def now_ms() -> int:
    return int(time.time() * 1000)


class JsonlTelemetryWriter:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write_event(self, event: TelemetryEvent) -> None:
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(event.to_json())
            handle.write("\n")
