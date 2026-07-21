from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class TaskAnalysis:
    topic: str
    subtype: str
    sought: str
    given: tuple[str, ...]
    concepts: tuple[str, ...]
    formula_keys: tuple[str, ...]
    opening_question: str
    planning_question: str
    checking_question: str
    misconceptions: tuple[str, ...]


@dataclass
class TutorState:
    phase: str = "VERSTEHEN"
    help_level: int = 1
    turns: int = 0
    mistake_counts: dict[str, int] = field(default_factory=dict)
