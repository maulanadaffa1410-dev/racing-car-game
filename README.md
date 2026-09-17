A simple arcade racing game built with Python and Pygame. The player drives a car through traffic, avoids crashing, shoots incoming obstacles, and survives as the difficulty increases.

## Features

- 3-lane highway gameplay
- Keyboard controls for moving left and right
- Projectile shooting mechanic
- Randomized traffic and enemy vehicles
- Progressively increasing difficulty
- Score system and level progression
- Game over and restart flow
- Police car enemy behavior
- Optional custom truck sprite support

## Gameplay

The game begins on a start screen. Press R to begin playing. Use the arrow keys or A/D to move left and right, and press Space to shoot enemy vehicles. Avoid crashing into traffic and try to survive as long as possible while accumulating points.

## Controls

| Key | Action |
| --- | --- |
| Left Arrow / A | Move left |
| Right Arrow / D | Move right |
| Space | Shoot |
| R | Start or restart the game |

## Requirements

- Python 3.9+
- Pygame

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/maulanadaffa1410-dev/racing-car-game.git
   cd racing-car-game
   ```

2. Install dependencies:
   ```bash
   pip install pygame
   ```

3. Run the game:
   ```bash
   python main.py
   ```

## Project Structure

```text
racing-car-game/
├── main.py
└── README.md
```

## Notes

- The game is implemented as a single Python file: `main.py`.
- The script currently references a Windows-specific image path for the truck:
  ```python
  TRUCK_IMAGE_PATH = r"C:\Users\user\OneDrive\Pictures\Screenshots\Image20260910190209.png"
  ```
- If that file is not found, the game falls back to a drawn truck graphic.

## License

This project does not currently include a license file. It is provided as-is for learning and personal use.
