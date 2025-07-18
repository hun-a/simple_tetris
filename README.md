# Tetris Game

A classic Tetris game implementation in Python using Pygame.

## Features

- **Classic Tetris gameplay** with all 7 traditional tetrominoes (I, O, T, S, Z, J, L)
- **Smooth controls** with continuous movement when holding direction keys
- **Progressive difficulty** - game speed increases with each level
- **Scoring system** - earn points for clearing lines and dropping pieces
- **Line clearing mechanics** - complete horizontal lines disappear
- **Next piece preview** - see what tetromino is coming next
- **Lock delay system** - brief grace period to adjust pieces after they land
- **Dual control schemes** - use arrow keys OR WASD keys
- **Improved game over detection** - only triggers when blocks truly reach the top
- **Visual feedback** with colored pieces and grid display

## Controls

### Movement Controls (Choose your preference)
| Arrow Keys | WASD Keys | Action |
|------------|-----------|--------|
| ← → | A/D | Move piece left/right (continuous when held) |
| ↓ | S | Soft drop (continuous when held) |
| ↑ | W | Rotate piece clockwise |

### Special Controls
| Key | Action |
|-----|--------|
| Space | Hard drop (instant drop) |
| R | Restart game (when game over) |

## Installation

### Using UV (Recommended)

1. **Install UV:**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

### Using pip (Legacy)

1. **Install Python 3.12+**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## How to Play

1. **Run the game:**
   ```bash
   # Using UV
   uv run python tetris.py
   
   # Or using python directly
   python3 tetris.py
   ```

2. **Gameplay:**
   - Pieces fall from the top of the screen
   - Use arrow keys OR WASD keys to move and rotate pieces
   - See the next piece in the preview area on the right
   - Complete horizontal lines to clear them and score points
   - Use the lock delay to adjust pieces after they land
   - Game speed increases as you progress through levels
   - Game ends when pieces reach the top

## Game Mechanics

- **Scoring:** 100 points per line cleared × current level
- **Level progression:** Advance level every 10 lines cleared
- **Speed increase:** Fall speed increases with each level
- **Soft drop bonus:** +1 point for each cell dropped manually
- **Hard drop bonus:** +2 points for hard dropping
- **Lock delay:** 500ms grace period to move pieces after they land
- **Next piece system:** Preview the upcoming tetromino to plan ahead
- **Responsive controls:** First key press moves immediately, held keys repeat

## Technical Details

- **Language:** Python 3.12+
- **Framework:** Pygame 2.5.2+
- **Resolution:** 650×650 pixels
- **Grid size:** 10×20 cells
- **Frame rate:** 60 FPS

## Project Structure

```
tetris_with_claude/
├── tetris.py           # Main game file
├── pyproject.toml      # Project configuration and dependencies (UV)
├── requirements.txt    # Legacy pip dependencies
└── README.md          # This file
```

## License

This project is open source and available under the MIT License.