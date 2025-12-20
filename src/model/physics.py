"""Simple physics update for the pinball game."""
from __future__ import annotations

import math

from .game_state import Bumper, GameEventType, GameState


class PhysicsEngine:
    def step(self, state: GameState, dt: float) -> None:
        ball = state.ball
        table = state.table

        ball.vy += table.gravity * dt
        ball.x += ball.vx * dt
        ball.y += ball.vy * dt

        self._handle_walls(state)
        self._handle_bumpers(state)
        self._handle_flippers(state)
        self._handle_drain(state)

    def _handle_walls(self, state: GameState) -> None:
        ball = state.ball
        table = state.table
        if ball.x - ball.radius <= 0 or ball.x + ball.radius >= table.width:
            ball.vx *= -1
            ball.x = max(ball.radius, min(table.width - ball.radius, ball.x))
            state.push_event(GameEventType.BUMPER_HIT, {"axis": "x"})
        if ball.y - ball.radius <= 0:
            ball.vy *= -1
            ball.y = ball.radius
            state.push_event(GameEventType.BUMPER_HIT, {"axis": "y"})

    def _handle_bumpers(self, state: GameState) -> None:
        for bumper in state.bumpers:
            if self._circle_collision(state.ball.x, state.ball.y, state.ball.radius, bumper):
                state.ball.vy *= -1
                state.ball.vx *= -1
                state.add_score(bumper.score)
                state.push_event(GameEventType.BUMPER_HIT, {"bumper": bumper})

    def _circle_collision(self, bx: float, by: float, br: float, bumper: Bumper) -> bool:
        distance = math.hypot(bx - bumper.x, by - bumper.y)
        return distance <= br + bumper.radius

    def _handle_flippers(self, state: GameState) -> None:
        for flipper in state.flippers:
            if not flipper.is_active:
                continue
            within_x = flipper.x - flipper.width / 2 <= state.ball.x <= flipper.x + flipper.width / 2
            within_y = flipper.y - flipper.height <= state.ball.y + state.ball.radius <= flipper.y + flipper.height
            if within_x and within_y:
                state.ball.vy = -abs(state.ball.vy) - flipper.strength
                state.ball.vx += (state.ball.x - flipper.x) * 2
                state.push_event(GameEventType.FLIPPER_USED, {"flipper": flipper})

    def _handle_drain(self, state: GameState) -> None:
        if state.ball.y - state.ball.radius > state.table.height:
            state.push_event(GameEventType.BALL_DRAINED)
            state.ball.x = state.table.width / 2
            state.ball.y = 200.0
            state.ball.vx = 0.0
            state.ball.vy = 0.0
