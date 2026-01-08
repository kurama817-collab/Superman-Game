"""Telemetry schema and utilities for the Protocol Ψ sandbox."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import time
from typing import Dict, Literal, TextIO

EventType = Literal[
    "wx_tick",
    "ccs_sample",
    "hce_impossible_split",
    "ccip_branch",
    "ccip_prune",
    "ledger_append",
]


@dataclass
class TelemetryEvent:
    event: EventType
    ts_ms: int
    session_id: str
    payload: Dict[str, object]

    def to_json(self) -> str:
        return json.dumps(asdict(self), separators=(",", ":"), sort_keys=True)


def now_ms() -> int:
    return int(time.time() * 1000)


class JsonlTelemetryWriter:
    def __init__(self, file: TextIO) -> None:
        self._file = file

    def write(self, event: TelemetryEvent) -> None:
        self._file.write(event.to_json() + "\n")
        self._file.flush()
