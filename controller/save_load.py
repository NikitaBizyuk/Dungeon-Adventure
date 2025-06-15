import os
import pickle
from typing import Optional
from controller.dungeon_adventure import DungeonAdventure

SAVE_FILE = "save_data.pkl"


def save_game(game: DungeonAdventure, filename: str = SAVE_FILE) -> None:
    try:
        full_path = os.path.abspath(filename)
        with open(full_path, "wb") as f:
            pickle.dump(game, f)
        print(f"✅ Game saved! File location: {full_path}")
    except Exception as e:
        print(f"❌ Failed to save game: {e}")


def load_game(filename: str = SAVE_FILE) -> Optional[DungeonAdventure]:
    full_path = os.path.abspath(filename)

    if not os.path.exists(full_path):
        print(f"⚠️ No saved game found at: {full_path}")
        return None

    try:
        with open(full_path, "rb") as f:
            game = pickle.load(f)
        print(f"✅ Game loaded from: {full_path}")
        return game
    except Exception as e:
        print(f"❌ Failed to load game from {full_path}: {e}")
        return None
