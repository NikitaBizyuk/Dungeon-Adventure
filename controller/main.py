import pygame
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


def main():
    pygame.init()

    info = pygame.display.Info()
    WIDTH, HEIGHT = info.current_w, info.current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Dungeon Adventure")

    FIXED_ROWS = 15
    CELL       = HEIGHT // FIXED_ROWS
    FIXED_COLS = WIDTH  // CELL

    clock = pygame.time.Clock()
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

    running = True
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
                running = False

            # ------------- MAIN MENU -------------
            elif state == "main_menu":
                for b in view.menu_buttons:
                    if b.is_clicked(ev):
                        if b.text == "PLAY":
                            state = "difficulty_menu"
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
                            running = False

            # ------------- DIFFICULTY MENU -------------
            elif state == "difficulty_menu":
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

        # ───────────────────── RENDERING ──────────────────────────
        if state == "main_menu":
            view.draw_buttons(view.menu_buttons)

        elif state == "difficulty_menu":
            view.draw_buttons(view.difficulty_buttons)

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


if __name__ == "__main__":
    main()