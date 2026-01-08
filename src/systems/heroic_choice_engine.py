"""Heroic Choice Engine stub.

Builds choice prompts and resolves their consequences.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class HeroicChoice:
    choice_id: str
    prompt: str
    options: List[str]


@dataclass
class ChoiceOutcome:
    choice_id: str
    option: str
    reputation_delta: int
    city_health_delta: float


class HeroicChoiceEngine:
    """Placeholder implementation for player choice generation."""

    def __init__(self) -> None:
        self.active_choices: Dict[str, HeroicChoice] = {}

    def queue_choice(self, choice: HeroicChoice) -> None:
        self.active_choices[choice.choice_id] = choice

    def resolve_choice(self, choice_id: str, option: str) -> ChoiceOutcome:
        choice = self.active_choices.pop(choice_id)
        return ChoiceOutcome(
            choice_id=choice.choice_id,
            option=option,
            reputation_delta=0,
            city_health_delta=0.0,
        )
