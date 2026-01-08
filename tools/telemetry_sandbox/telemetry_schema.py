from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any
import json
import time


class EventType(str, Enum):
    W_X = "W_X"
    CCS = "CCS"
    HCE = "HCE"
    CCIP = "CCIP"
    LEDGER = "LEDGER"


@dataclass
class TelemetryEvent:
    event_type: EventType
    timestamp_ms: int
    session_id: str
    payload: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type.value,
            "timestamp_ms": self.timestamp_ms,
            "session_id": self.session_id,
            "payload": self.payload,
        }


class JsonlTelemetryWriter:
    def __init__(self, path: str) -> None:
        self.path = path

    def write_event(self, event: TelemetryEvent) -> None:
        with open(self.path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(event.to_dict(), sort_keys=True))
            handle.write("\n")


def now_ms() -> int:
    return int(time.time() * 1000)
