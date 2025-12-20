"""Pygame renderer for the pinball simulation."""
from __future__ import annotations

from dataclasses import dataclass

from ..model.game_state import GameState


@dataclass
class RenderConfig:
    width: int = 800
    height: int = 1200
    fps: int = 60


class Renderer:
    def __init__(self, config: RenderConfig | None = None) -> None:
        self.config = config or RenderConfig()
        self._pygame = None
        self._screen = None
        self._font = None

    def initialize(self) -> None:
        import pygame

        pygame.init()
        pygame.display.set_caption("Pinball MVC")
        self._pygame = pygame
        self._screen = pygame.display.set_mode((self.config.width, self.config.height))
        self._font = pygame.font.SysFont("Arial", 24)

    def close(self) -> None:
        if self._pygame:
            self._pygame.quit()

    def draw(self, state: GameState) -> None:
        if not self._pygame or not self._screen:
            raise RuntimeError("Renderer not initialized")

        self._screen.fill((15, 18, 28))

        for bumper in state.bumpers:
            self._pygame.draw.circle(
                self._screen, (200, 180, 60), (int(bumper.x), int(bumper.y)), int(bumper.radius)
            )

        for flipper in state.flippers:
            rect = self._pygame.Rect(
                flipper.x - flipper.width / 2,
                flipper.y - flipper.height / 2,
                flipper.width,
                flipper.height,
            )
            color = (220, 90, 90) if flipper.is_active else (180, 80, 80)
            self._pygame.draw.rect(self._screen, color, rect)

        self._pygame.draw.circle(
            self._screen,
            (240, 240, 240),
            (int(state.ball.x), int(state.ball.y)),
            int(state.ball.radius),
        )

        score_surface = self._font.render(f"Score: {state.score}", True, (240, 240, 240))
        self._screen.blit(score_surface, (20, 20))

        self._pygame.display.flip()
