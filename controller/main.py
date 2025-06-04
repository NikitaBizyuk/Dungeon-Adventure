import pygame
from controller.dungeon_adventure import DungeonAdventure
from view.game_view import GameView
from model.room import Room
from model.Skeleton import Skeleton
from model.Gremlin import Gremlin
from model.Ogre import Ogre


def main() -> None:
    # ────────────── init Pygame / window ──────────────
    pygame.init()

    info   = pygame.display.Info()
    WIDTH  = info.current_w - 70        # teammate’s margins
    HEIGHT = info.current_h - 100

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dungeon Adventure")

    # ────────────── view / scaling constants ──────────
    FIXED_VIEW_ROWS = 15
    CELL_SIZE       = HEIGHT // FIXED_VIEW_ROWS
    FIXED_VIEW_COLS = WIDTH  // CELL_SIZE

    clock = pygame.time.Clock()
    view  = GameView(screen, CELL_SIZE, FIXED_VIEW_ROWS, FIXED_VIEW_COLS)

    # ────────────── game state variables ──────────────
    state              = "main_menu"   # → "difficulty_menu" → "playing"
    difficulty         = None
    game               = None          # <── create after difficulty chosen
    hero_last_move_ms  = 0
    HERO_MOVE_DELAY_MS = 150

    # ────────────── main loop ─────────────────────────
    running = True
    while running:
        screen.fill((0, 0, 0))

        # ---------- handle events ----------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # ===== MAIN MENU =====
            if state == "main_menu":
                for btn in view.menu_buttons:
                    if btn.is_clicked(event) and btn.text == "PLAY":
                        state = "difficulty_menu"

            # ===== DIFFICULTY MENU =====
            elif state == "difficulty_menu":
                for btn in view.difficulty_buttons:
                    if btn.is_clicked(event):
                        difficulty = btn.text.lower()          # easy | medium | hard
                        Room.set_difficulty(difficulty)        # update monster ranges

                        game = DungeonAdventure()              # build dungeon *after* setting difficulty
                        if hasattr(game, "set_difficulty"):
                            game.set_difficulty(difficulty)

                        print(f"Started game on {difficulty.upper()}")
                        state = "playing"

            # ===== GAME HOTKEYS =====
            elif state == "playing":
                if (
                    event.type == pygame.KEYDOWN
                    and game.in_room
                    and event.key == pygame.K_q
                ):
                    game.exit_room()

        # ---------- per‑frame input ----------
        if state == "playing":
            keys = pygame.key.get_pressed()
            dx = -1 if keys[pygame.K_w] else 1 if keys[pygame.K_s] else 0
            dy = -1 if keys[pygame.K_a] else 1 if keys[pygame.K_d] else 0

            # move hero on a timer
            if dx or dy:
                now = pygame.time.get_ticks()
                if now - hero_last_move_ms >= HERO_MOVE_DELAY_MS:
                    game.move_hero(dx, dy)
                    hero_last_move_ms = now

            game.move_monsters()

        # ---------- draw ----------
        if state == "main_menu":
            view.draw_buttons(view.menu_buttons)

        elif state == "difficulty_menu":
            view.draw_buttons(view.difficulty_buttons)

        elif state == "playing":
            if game.in_room:
                view.draw_room(
                    game.active_room, WIDTH, HEIGHT, Ogre, Skeleton, Gremlin
                )
            else:
                view.draw_maze(game.dungeon, game.dungeon.hero_x, game.dungeon.hero_y)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()