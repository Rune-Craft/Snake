# Snake Game

A classic Snake game built with Python and curses, featuring Firebase Firestore integration for online leaderboards.

## Features
- Classic snake gameplay
- Customizable colors and board size
- Adjustable game speed
- **Shared online leaderboard** using Firebase Firestore - compete with players worldwide!
- Local settings saved to SQLite

## Requirements
- Python 3.7+
- firebase-admin
- curses (included on Linux/Mac, use `windows-curses` on Windows)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Rune-Craft/Snake.git
cd Snake
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```
   Or install manually:
```bash
pip install firebase-admin requests
# On Windows only:
pip install windows-curses
```

3. Run the game:
```bash
python Main.py
```

The game will automatically connect to the shared leaderboard!

## Controls
- **W/A/S/D** or **Arrow Keys**: Move snake
- **P**: Pause game
- **Q**: Quit current game
- **S** (in menu): Settings

## Configuration
Settings are saved locally in `snake_game.db` and include:
- Snake, apple, and border colors
- Board dimensions
- Game speed

The leaderboard is shared globally across all players and stored in Firebase Firestore.
