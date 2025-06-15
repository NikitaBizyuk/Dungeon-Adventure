# 🕹️ Dungeon Adventure – TCSS 360 Course Project

A real-time dungeon crawler game implemented in Python using the **Model-View-Controller (MVC)** architecture. Navigate through a procedurally generated dungeon, battle animated monsters, and collect the four pillars of OOP to escape.

---

## 📦 Project Structure

```
DungeonAdventure/
│
├── assets/           # Sprites, fonts, and other game assets
├── controller/       # Game loop, input, and main program (main.py)
├── data/             # SQLite monster database and save files
├── model/            # Game logic and OOP entities (Hero, Monster, Room, etc.)
├── view/             # Rendering and UI with Pygame
└── tests/            # Unit tests for models and logic
```

---

## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.10 or higher
- `pygame` library
- `sqlite3` (comes with Python)

### 📥 Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/NikitaBizyuk/TCSS-360-Course-Project.git
   cd TCSS-360-Course-Project
   ```


3. **Install Dependencies:**
   ```bash
   pip install pygame
   ```

---

## 🐉 Monster Database Setup

The game uses a SQLite database (`monsters.db`) to store monster stats such as HP, damage, and healing range.

> ⚠️ The `monsters.db` file is **not committed to Git** (it’s in `.gitignore`), so you’ll need to generate it locally before playing.

### ✅ Generate Monster Database

```bash
python data/init_monster_db.py
```

You should see a `monsters.db` file created in the `data/` directory.

---

## 🧠 Gameplay Overview

- Select your hero class (Warrior, Priestess, Thief).
- Defeat animated monsters and bosses in real-time combat.
- Collect the **four Pillars of OOP** hidden in rooms:
  - Abstraction
  - Inheritance
  - Polymorphism
  - Encapsulation
- Escape through the dungeon exit after collecting all four.

---

## 💾 Saving and Loading

- You can save and load your game progress from the pause menu.
- Save files are stored locally as `save_data.pkl`.
- Save/load supports all hero stats and animation state restoration.

---

## 🎮 Controls

| Action            | Key / Mouse              |
|-------------------|--------------------------|
| Move              | Arrow keys / WASD        |
| Attack (Melee)    | Left Click               |
| Shoot (Ranged)    | Right Click              |
| Open Menu / Pause | `Esc`                    |
| Interact          | Spacebar                 |

---

## 🛠️ Features

- 🧱 Procedural dungeon generation
- 👾 Animated monsters with fireball and melee attacks
- 🦸 Custom hero classes with different skills and animations
- 💾 Save/load system with sprite reload support
- 📊 SQLite-based monster stats
- 🧭 Full camera tracking and UI overlay

---

## 📚 Acknowledgements

- Sprites from https://craftpix.net/freebies/
- Game built for TCSS 360: Software Development at the University of Washington

---

## 📬 Team

Created by:
- Rudolf Arakelyan
- Nikita Bizyuk
- Collin Mbugua
- Ian Fuhr


---
