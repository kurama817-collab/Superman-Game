from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional, TextIO


class EventType(str, Enum):
    # Canonical v1 events used in sandbox output
    W_EVALUATION_TICK = "W_EVALUATION_TICK"
    CCS_PRECISION_SAMPLE = "CCS_PRECISION_SAMPLE"
    HCE_SIMULTANEOUS_GOODS_PRESENTED = "HCE_SIMULTANEOUS_GOODS_PRESENTED"
    HCE_FIRST_COMMITMENT_LATCHED = "HCE_FIRST_COMMITMENT_LATCHED"
    CCIP_BRANCH_DENSITY = "CCIP_BRANCH_DENSITY"
    CCIP_PRUNE_EXECUTED = "CCIP_PRUNE_EXECUTED"
    COST_LEDGER_APPEND = "COST_LEDGER_APPEND"


@dataclass(frozen=True)
class TelemetryEvent:
    event: str
    ts_ms: int
    session_id: str
    payload: Dict[str, Any]


class JsonlTelemetryWriter:
    """
    Writes one JSON object per line (JSONL), append-only *within a run*.
    The file handle should be opened by the caller (typically in 'w' to overwrite per run).
    """

    def __init__(self, fp: TextIO):
        self._fp = fp

    def write(self, e: TelemetryEvent) -> None:
        obj = {
            "event": e.event,
            "ts_ms": e.ts_ms,
            "session_id": e.session_id,
            "payload": e.payload or {},
        }
        line = json.dumps(obj, sort_keys=True, separators=(",", ":"))
        self._fp.write(line + "\n")

    def flush(self) -> None:
        self._fp.flush()
