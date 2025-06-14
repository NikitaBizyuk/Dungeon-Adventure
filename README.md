# Dungeon Adventure Game – TCSS 360

## Overview
A real time dungeon game implemented in Python. It uses a MVC architecture and is designed to help players collect the four pillars of OOP while navigating obstacles and battling monsters.

## Structure
- `model/`: Game logic and entity classes (Hero, Monster, Room)
- `controller/`: Game loop and input handling
- `view/`: CLI or GUI rendering (Pygame)
- `data/`: SQLite database and save files
- `assets/`: Sprites, sounds, etc.
- `tests/`: Unit tests (to be added)

## Setup
1. Clone the repo
2. Create a virtual environment:
## 🐉 Monster Database Setup

This game uses a SQLite database (`monsters.db`) to store monster stats (HP, damage range, heal chance, etc.).

### ⚠️ Note:
The `monsters.db` file is **not included** in the repository (it's ignored by Git), so you'll need to generate it locally before running the game.

### ✅ To Generate the Monster Database:

1. Make sure you have Python installed.
2. Run the following command in your terminal:

```bash
python data/init_monster_db.py

