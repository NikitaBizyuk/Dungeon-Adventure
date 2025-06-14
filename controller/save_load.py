import pickle
from typing import Optional
from controller.dungeon_adventure import DungeonAdventure

def save_game(game: DungeonAdventure, filename: str = "save_data.pkl") -> None:
    try:
        with open(filename, "wb") as f:
            pickle.dump(game, f)
        print("✅ Game saved!")
    except Exception as e:
        print(f"❌ Failed to save game: {e}")

def load_game(filename: str = "save_data.pkl") -> Optional[DungeonAdventure]:
    try:
        with open(filename, "rb") as f:
            game = pickle.load(f)
        print("✅ Game loaded!")
        return game
    except FileNotFoundError:
        print("⚠️ No saved game found.")
        return None
    except Exception as e:
        print(f"❌ Failed to load game: {e}")
        return None
