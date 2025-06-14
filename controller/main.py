import pygame
<<<<<<< Updated upstream
from controller.dungeon_adventure import DungeonAdventure
from view.game_view import GameView
from view.menu_button import Button
from model.Skeleton import Skeleton
from model.Gremlin import Gremlin
from model.Ogre import Ogre
=======
import math

# ─── controller helpers ─────────────────────────────────────────
from controller.dungeon_adventure import DungeonAdventure
from controller.save_load       import save_game, load_game

# ─── view ───────────────────────────────────────────────────────
from view.game_view import GameView

# ─── game data / models ─────────────────────────────────────────
from model.room      import Room
from model.OOPillars import OOPillars

#  Monster classes (needed for draw_room)
from model.Ogre      import Ogre
from model.Skeleton  import Skeleton
from model.Gremlin   import Gremlin

#  Hero classes
from model.warrior   import Warrior
from model.Priestess import Priestess
from model.Thief     import Thief

>>>>>>> Stashed changes

def main():
    pygame.init()

    # Fullscreen mode
    info = pygame.display.Info()
    WIDTH, HEIGHT = info.current_w, info.current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Dungeon Adventure")

    FIXED_ROWS = 15
    CELL       = HEIGHT // FIXED_ROWS
    FIXED_COLS = WIDTH  // CELL

    clock = pygame.time.Clock()
<<<<<<< Updated upstream
    game = DungeonAdventure()
    view = GameView(screen, CELL_SIZE, view_rows=FIXED_VIEW_ROWS, view_cols=FIXED_VIEW_COLS)
=======
    view  = GameView(screen, CELL, FIXED_ROWS, FIXED_COLS)

    hero_move_delay = 150         # ms between moves
    hero_last_move  = 0

    # ─── high-level game state flags ────────────────────────────
    state        = "main_menu"
    pause_state  = False
    resume_cnt   = 0
    prev_menu    = None
    game         = None
    pending_diff = None           # difficulty selected, waiting for hero pick
    dead_start   = None           # timestamp when Game-Over screen appears
>>>>>>> Stashed changes

    running = True
<<<<<<< Updated upstream
    state = "main_menu" 
    game = None

    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
=======
    while running:
        screen.fill((0, 0, 0))

        # show/hide OS cursor
        if state in {"main_menu", "difficulty_menu", "about_screen", "pause_menu"}:
            pygame.mouse.set_visible(True)
            pygame.event.set_grab(False)
        else:
            pygame.mouse.set_visible(False)
            pygame.event.set_grab(True)

        # compute hero screen-space position for aim smoothing
        if game and state == "playing":
            if game.in_room:
                hr, hc = game.active_room.get_hero_position()
            else:
                hr, hc = game.dungeon.hero_x, game.dungeon.hero_y
            sr = max(0, min(game.dungeon.rows - FIXED_ROWS, hr - FIXED_ROWS // 2))
            sc = max(0, min(game.dungeon.cols - FIXED_COLS, hc - FIXED_COLS // 2))
            hero_sx = (hc - sc) * CELL + CELL // 2
            hero_sy = (hr - sr) * CELL + CELL // 2

        # ─────────────────── EVENT HANDLING ──────────────────────
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
>>>>>>> Stashed changes
                running = False

            # ------------- MAIN MENU -------------
            elif state == "main_menu":
                for b in view.menu_buttons:
                    if b.is_clicked(ev):
                        if b.text == "PLAY":
                            state = "difficulty_menu"
<<<<<<< Updated upstream
                        elif button.text == "LOAD":
                            print("NOT IMPLEMENTED YET")
                        elif button.text == "ABOUT":
                            print("Dungeon Adventures VERSION 1.0")
                        elif button.text == "QUIT":
=======
                        elif b.text == "LOAD":
                            g = load_game()
                            if g:
                                game = g
                                state = "playing"
                                view.display_message("✅ Game Loaded!", 2000)
                            else:
                                view.display_message("⚠️ No save found!", 2000)
                        elif b.text == "ABOUT":
                            prev_menu = "main_menu"
                            state = "about_screen"
                        elif b.text == "QUIT":
>>>>>>> Stashed changes
                            running = False

            # ------------- DIFFICULTY MENU -------------
            elif state == "difficulty_menu":
<<<<<<< Updated upstream
                for button in view.difficulty_buttons:
                    if button.is_clicked(event):
                        difficulty = button.text.lower()
                        from model.room import Room
                        Room.set_difficulty(difficulty)
                        game = DungeonAdventure()
                        if hasattr(game, "set_difficulty"):
                            game.set_difficulty(difficulty)
                        print(f"Started game on {difficulty.upper()}")
                        state = "playing"

            elif state == "playing":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = "main_menu"
                    elif game.in_room and event.key == pygame.K_q:
                        game.exit_room()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    game.perform_melee_attack()
                    view.show_melee_attack()
=======
                for b in view.difficulty_buttons:
                    if b.is_clicked(ev):
                        Room.set_difficulty(b.text.lower())
                        pending_diff = b.text.lower()
                        state = "hero_menu"

            # ------------- HERO MENU -------------
            elif state == "hero_menu":
                for b in view.hero_buttons:
                    if b.is_clicked(ev):
                        cls = {"WARRIOR": Warrior,
                               "PRIESTESS": Priestess,
                               "THIEF":     Thief}[b.text]
                        game = DungeonAdventure(cls, "Rudy")
                        state = "playing"

            # ------------- ABOUT SCREEN -------------
            elif state == "about_screen":
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    state = prev_menu or "main_menu"
                    pause_state = (state == "pause_menu")
                    prev_menu = None

            # ------------- PLAYING -------------
            elif state == "playing":
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    state = "pause_menu"
                    pause_state = True

                elif not pause_state:
                    if ev.type == pygame.KEYDOWN:
                        if ev.key == pygame.K_TAB:
                            view.show_inventory = not view.show_inventory
                        elif game.in_room and ev.key == pygame.K_q:
                            game._leave_room()
                        elif ev.key == pygame.K_e:
                            game.perform_ranged_attack(CELL)
                        elif ev.key == pygame.K_SPACE and game.in_room:
                            view.display_message(game.perform_special_attack())
                        elif ev.key == pygame.K_h and game.get_backpack().get_healing_cntr() > 0:
                            bp = game.get_backpack()
                            bp.use_healing_potion()
                            hero = game.get_hero()
                            hero.health_points = min(
                                hero.health_points + 20, hero._max_health_points)
                            view.display_message("Healing Potion +20", 2000)
                        elif ev.key == pygame.K_v and game.get_backpack().use_vision_potion():
                            game.vision_reveal_start = pygame.time.get_ticks()
                            view.display_message("Vision Potion!", 2000)

                    if ev.type == pygame.MOUSEBUTTONDOWN:
                        if ev.button == 1:
                            game.perform_melee_attack()
                            view.show_melee_attack()
                        elif ev.button == 3:
                            game.perform_ranged_attack(CELL)

                    if ev.type == pygame.MOUSEMOTION:
                        mx, my = pygame.mouse.get_pos()
                        dx, dy = mx - hero_sx, my - hero_sy
                        if dx or dy:
                            vec = pygame.math.Vector2(dx, dy).normalize()
                            game.aim_vector = pygame.math.Vector2(game.aim_vector).lerp(vec, 0.1)

            # ------------- PAUSE MENU -------------
            elif state == "pause_menu":
                for b in view.pause_buttons:
                    if b.is_clicked(ev):
                        if b.text == "RESUME":
                            resume_cnt = 180   # 3-second countdown at 60 FPS
                            state = "countdown"
                        elif b.text == "SAVE":
                            try:
                                save_game(game)
                                view.display_message("✅ Game Saved", 2000)
                            except Exception:
                                view.display_message("❌ Save Failed", 2000)
                        elif b.text == "ABOUT":
                            prev_menu = "pause_menu"
                            state = "about_screen"
                        elif b.text == "BACK":
                            game = None
                            state = "main_menu"
                            pause_state = False
>>>>>>> Stashed changes

        # ───────────────────── RENDERING ──────────────────────────
        if state == "main_menu":
            view.draw_buttons(view.menu_buttons)
        elif state == "difficulty_menu":
            view.draw_buttons(view.difficulty_buttons)
<<<<<<< Updated upstream
        elif state == "playing":
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[pygame.K_w]: dx -= 1
            if keys[pygame.K_s]: dx += 1
            if keys[pygame.K_a]: dy -= 1
            if keys[pygame.K_d]: dy += 1

            game.move_monsters()
            if dx != 0 or dy != 0:
                current_time = pygame.time.get_ticks()
                if current_time - hero_last_move_time >= hero_move_delay:
                    game.move_hero(dx, dy)
                    hero_last_move_time = current_time

            if game.in_room:
                hero_r, hero_c = game.active_room.get_hero_position()
                room = game.active_room
            else:
                hero_r = game.dungeon.hero_x
                hero_c = game.dungeon.hero_y

            start_r = max(0, min(game.dungeon.rows - FIXED_VIEW_ROWS, hero_r - FIXED_VIEW_ROWS // 2))
            start_c = max(0, min(game.dungeon.cols - FIXED_VIEW_COLS, hero_c - FIXED_VIEW_COLS // 2))
            hero_screen_x = (hero_c - start_c) * CELL_SIZE + CELL_SIZE // 2
            hero_screen_y = (hero_r - start_r) * CELL_SIZE + CELL_SIZE // 2

            mouse_x, mouse_y = pygame.mouse.get_pos()
            aim_dx = mouse_x - hero_screen_x
            aim_dy = mouse_y - hero_screen_y
            length = (aim_dx ** 2 + aim_dy ** 2) ** 0.5
            if length != 0:
                game.aim_vector = (aim_dx / length, aim_dy / length)

            if game.in_room:
                view.draw_room(game, WIDTH, HEIGHT, Ogre, Skeleton, Gremlin)
            else:
                view.draw_maze(game)
=======

        elif state == "hero_menu":
            view.draw_buttons(view.hero_buttons)

        elif state == "about_screen":
            view.draw_about_screen()

        elif state == "pause_menu":
            view.draw_buttons(view.pause_buttons)

        elif state == "countdown":
            pause_state = True
            view.draw_buttons(view.pause_buttons)
            sec = resume_cnt // 60 + 1
            txt = pygame.font.Font(None, 200).render(str(sec), True, (255, 255, 255))
            screen.blit(txt, txt.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            resume_cnt -= 1
            if resume_cnt <= 0:
                state = "playing"
                pause_state = False

        elif state == "playing":
            if not pause_state:
                keys = pygame.key.get_pressed()
                dx = keys[pygame.K_s] - keys[pygame.K_w]
                dy = keys[pygame.K_d] - keys[pygame.K_a]

                game.move_monsters()
                game.monster_attack_hero()
                game.update_projectiles(CELL)

                if dx or dy:
                    now = pygame.time.get_ticks()
                    if now - hero_last_move >= hero_move_delay:
                        game.move_hero(dx, dy)
                        hero_last_move = now

                # if out of lives → go to dead screen
                if game.game_over:
                    view.display_message("💀 Game Over: No lives left!", 3000)
                    dead_start = pygame.time.get_ticks()
                    state = "dead"
                    continue

            if game.in_room:
                view.draw_room(
                    game, WIDTH, HEIGHT, game.get_hero(), game.get_backpack(),
                    Ogre, Skeleton, Gremlin,
                    OOPillars.ENCAPSULATION.symbol, OOPillars.POLYMORPHISM.symbol,
                    OOPillars.INHERITANCE.symbol,  OOPillars.ABSTRACTION.symbol
                )
            else:
                view.draw_maze(game, WIDTH, HEIGHT,
                               game.get_hero(), game.get_backpack())

            # special ability status
            now = pygame.time.get_ticks()
            if game.special_active and now - game.last_special_used > game.special_duration:
                game.special_active = False

            if game.special_active:
                left = (game.special_duration - (now - game.last_special_used)) / 1000
                status = f"Special: Active ({left:.1f}s)"
            elif now - game.last_special_used < game.special_cooldown:
                cd = (game.special_cooldown - (now - game.last_special_used)) / 1000
                status = f"Special: Cooldown ({cd:.1f}s)"
            else:
                status = "Special: Ready"

            status = f"Lives: {game.get_lives()}   |   {status}"
            view.draw_status_bar(screen, status)
>>>>>>> Stashed changes

        elif state == "dead":
            # draw Game-Over screen
            font_big   = pygame.font.Font(None, 120)
            font_small = pygame.font.Font(None,  50)

            txt = font_big.render("GAME OVER", True, (220, 20, 20))
            sub = font_small.render("Returning to main menu...", True, (255, 255, 255))

            screen.blit(txt, txt.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
            screen.blit(sub, sub.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40)))

            # after 3 s, return to main menu
            if dead_start and pygame.time.get_ticks() - dead_start > 3000:
                state = "main_menu"
                pause_state = False
                game = None
                dead_start = None
                view.message = ""  # clear any lingering HUD message

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
if __name__ == "__main__":
    main()