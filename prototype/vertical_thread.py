"""Vertical thread prototype: movement -> shockwave -> damage -> telemetry."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List
import math


@dataclass(frozen=True)
class Vec2:
    x: float
    y: float

    def distance_to(self, other: "Vec2") -> float:
        return math.hypot(self.x - other.x, self.y - other.y)


@dataclass
class DamageRecord:
    building_id: str
    amount: float
    position: Vec2


@dataclass
class TelemetryEvent:
    name: str
    payload: dict


@dataclass
class Building:
    building_id: str
    position: Vec2
    integrity: float = 100.0
    damage_log: List[DamageRecord] = field(default_factory=list)

    def apply_damage(self, amount: float) -> None:
        clamped = max(0.0, min(amount, self.integrity))
        self.integrity -= clamped
        self.damage_log.append(
            DamageRecord(building_id=self.building_id, amount=clamped, position=self.position)
        )


@dataclass
class WorldState:
    buildings: List[Building]
    damage_events: List[DamageRecord] = field(default_factory=list)
    telemetry: List[TelemetryEvent] = field(default_factory=list)


def calculate_shockwave_radius(speed: float, threshold: float = 300.0) -> float:
    if speed <= threshold:
        return 0.0
    return (speed - threshold) * 0.4


def emit_shockwave(speed: float, origin: Vec2, world: WorldState) -> None:
    radius = calculate_shockwave_radius(speed)
    event_payload = {"speed": speed, "radius": radius, "origin": origin}

    affected = 0
    if radius > 0.0:
        for building in world.buildings:
            distance = origin.distance_to(building.position)
            if distance <= radius:
                falloff = 1.0 - (distance / radius)
                damage = 35.0 * falloff
                building.apply_damage(damage)
                world.damage_events.append(building.damage_log[-1])
                affected += 1

    world.telemetry.append(
        TelemetryEvent(
            name="shockwave_emitted",
            payload={**event_payload, "affected_buildings": affected},
        )
    )


def run_vertical_thread() -> WorldState:
    world = WorldState(
        buildings=[
            Building("tower-01", Vec2(0.0, 20.0)),
            Building("tower-02", Vec2(40.0, 10.0)),
            Building("tower-03", Vec2(90.0, -10.0)),
        ]
    )
    superman_speed = 520.0
    superman_position = Vec2(0.0, 0.0)

    emit_shockwave(speed=superman_speed, origin=superman_position, world=world)
    return world


if __name__ == "__main__":
    state = run_vertical_thread()
    for record in state.damage_events:
        print(
            f"Damage: {record.building_id} took {record.amount:.1f} at {record.position}"
        )
    for event in state.telemetry:
        print(f"Telemetry: {event.name} -> {event.payload}")
