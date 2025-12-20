"""Rule-based music model that reacts to game events."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from ..game_state import GameEvent, GameEventType


@dataclass
class MusicState:
    tempo: int = 120
    intensity: int = 0
    motif: List[str] = field(default_factory=list)


class MusicModel:
    def __init__(self) -> None:
        self.state = MusicState()

    def handle_event(self, event: GameEvent) -> None:
        if event.event_type == GameEventType.BUMPER_HIT:
            self.state.intensity = min(self.state.intensity + 1, 10)
            self.state.motif.append("C#")
        elif event.event_type == GameEventType.BALL_LAUNCHED:
            self.state.tempo = min(self.state.tempo + 10, 200)
            self.state.motif.append("E")
        elif event.event_type == GameEventType.FLIPPER_USED:
            self.state.motif.append("G")
        elif event.event_type == GameEventType.BALL_DRAINED:
            self.state.intensity = max(self.state.intensity - 2, 0)
            self.state.motif.append("A")

    def drain_motif(self) -> List[str]:
        motif = list(self.state.motif)
        self.state.motif.clear()
        return motif
