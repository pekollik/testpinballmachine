"""Core game state for the pinball simulation."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class GameEventType(str, Enum):
    BALL_LAUNCHED = "ball_launched"
    BUMPER_HIT = "bumper_hit"
    FLIPPER_USED = "flipper_used"
    SCORE_CHANGED = "score_changed"
    BALL_DRAINED = "ball_drained"


@dataclass
class GameEvent:
    event_type: GameEventType
    payload: dict


@dataclass
class BallState:
    x: float
    y: float
    vx: float
    vy: float
    radius: float = 10.0


@dataclass
class Bumper:
    x: float
    y: float
    radius: float
    score: int = 100


@dataclass
class Flipper:
    x: float
    y: float
    width: float
    height: float
    strength: float = 480.0
    is_active: bool = False


@dataclass
class TableConfig:
    width: float = 800.0
    height: float = 1200.0
    gravity: float = 900.0


@dataclass
class GameState:
    table: TableConfig = field(default_factory=TableConfig)
    ball: BallState = field(default_factory=lambda: BallState(400.0, 200.0, 0.0, 0.0))
    bumpers: List[Bumper] = field(
        default_factory=lambda: [
            Bumper(250.0, 350.0, 35.0),
            Bumper(550.0, 350.0, 35.0),
            Bumper(400.0, 500.0, 40.0),
        ]
    )
    flippers: List[Flipper] = field(
        default_factory=lambda: [
            Flipper(260.0, 1050.0, 140.0, 20.0),
            Flipper(540.0, 1050.0, 140.0, 20.0),
        ]
    )
    score: int = 0
    events: List[GameEvent] = field(default_factory=list)

    def push_event(self, event_type: GameEventType, payload: dict | None = None) -> None:
        self.events.append(GameEvent(event_type=event_type, payload=payload or {}))

    def drain_events(self) -> List[GameEvent]:
        drained = list(self.events)
        self.events.clear()
        return drained

    def add_score(self, points: int) -> None:
        self.score += points
        self.push_event(GameEventType.SCORE_CHANGED, {"points": points, "score": self.score})
