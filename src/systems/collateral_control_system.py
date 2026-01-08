"""Collateral Control System stub.

Tracks city health, district damage, and collateral events.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class CollateralEvent:
    event_id: str
    district: str
    magnitude: float
    description: str


@dataclass
class DistrictStatus:
    name: str
    health: float = 100.0
    active_events: List[CollateralEvent] = field(default_factory=list)


class CollateralControlSystem:
    """Placeholder implementation for tracking collateral impact."""

    def __init__(self) -> None:
        self.city_health: float = 100.0
        self.districts: Dict[str, DistrictStatus] = {}

    def register_district(self, name: str) -> None:
        if name not in self.districts:
            self.districts[name] = DistrictStatus(name=name)

    def log_event(self, event: CollateralEvent) -> None:
        """Record a collateral event and update district health."""
        self.register_district(event.district)
        status = self.districts[event.district]
        status.active_events.append(event)
        status.health = max(0.0, status.health - event.magnitude)
        self._recalculate_city_health()

    def resolve_event(self, event_id: str) -> None:
        """Remove a resolved event from all districts."""
        for status in self.districts.values():
            status.active_events = [
                event for event in status.active_events if event.event_id != event_id
            ]

    def _recalculate_city_health(self) -> None:
        if not self.districts:
            self.city_health = 100.0
            return
        self.city_health = sum(status.health for status in self.districts.values()) / len(
            self.districts
        )
