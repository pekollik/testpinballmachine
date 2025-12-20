# testpinballmachine

## Tech choice
Suggested stack: **Python + Pygame** for a fast 2D prototype with easy input/rendering.

## MVC layout
- `src/model/`: flipper mechanics (Model 1) + `src/model/music/` (Model 2)
- `src/view/`: playfield rendering with Pygame
- `src/controller/`: game loop and integration between game + music models

## Run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.main
```

## Controls
- **A**: Left flipper
- **D**: Right flipper
