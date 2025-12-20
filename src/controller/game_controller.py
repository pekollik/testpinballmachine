"""Game controller that bridges game mechanics and music model."""
from __future__ import annotations

from ..model.game_state import GameEventType, GameState
from ..model.music.music_model import MusicModel
from ..model.physics import PhysicsEngine
from ..view.renderer import Renderer


class GameController:
    def __init__(self) -> None:
        self.state = GameState()
        self.physics = PhysicsEngine()
        self.music = MusicModel()
        self.renderer = Renderer()

    def run(self) -> None:
        self.renderer.initialize()
        pygame = self.renderer._pygame
        clock = pygame.time.Clock()

        running = True
        self.state.push_event(GameEventType.BALL_LAUNCHED)

        while running:
            dt = clock.tick(self.renderer.config.fps) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if self.state.flippers:
                self.state.flippers[0].is_active = bool(keys[pygame.K_a])
                self.state.flippers[1].is_active = bool(keys[pygame.K_d])

            self.physics.step(self.state, dt)

            for event in self.state.drain_events():
                self.music.handle_event(event)

            _ = self.music.drain_motif()
            self.renderer.draw(self.state)

        self.renderer.close()
