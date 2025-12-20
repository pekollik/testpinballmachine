"""Entry point for the pinball MVC simulation."""
from __future__ import annotations

from .controller.game_controller import GameController


def main() -> None:
    controller = GameController()
    controller.run()


if __name__ == "__main__":
    main()
