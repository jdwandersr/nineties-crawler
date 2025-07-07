# Nineties Crawler

A retro-inspired dungeon crawler in Python with Pygame, blending the procedural dungeons and party mechanics of "The Dark Heart of Uukrul" with the real-time feel of "Diablo".  
This is a personal learning project with a focus on clean code, modularity, and test coverage.

## Features (MVP)
- Procedurally generated single dungeon floor
- Four-character party: Fighter, Thief, Cleric, Wizard
- Real-time exploration, turn-based combat
- Randomized quest and puzzle per run
- Persistent floor state, resettable dungeons
- Simple placeholder graphics (pixel-art ready)
- Pytest and Ruff for testing and linting

## Getting Started

### Requirements

- Python 3.10+
- [Pygame](https://www.pygame.org/)
- [pytest](https://docs.pytest.org/)
- [ruff](https://docs.astral.sh/ruff/)

Install dependencies:

```bash
pip install -r requirements.txt
```

### Run the Game

```bash
python -m src.main
```

### Run Tests

```bash
pytest
```

### Lint

```bash
ruff src tests
```

## License

MIT License (see LICENSE file)
