import pygame
import math
from view.menu_button import Button
class GameView:
    def __init__(self, screen, cell_size, view_rows, view_cols):
        self.screen = screen
        self.cell_size = cell_size
        self.view_rows = view_rows
        self.view_cols = view_cols
<<<<<<< Updated upstream
        self.last_attack_time = 0
        self.attack_duration = 150
        self.font = pygame.font.Font(None, 60)

        self.menu_buttons = self.create_menu_buttons()
        self.difficulty_buttons = self.create_difficulty_buttons()

    def create_menu_buttons(self):
=======

        # attack-animation timing
        self.last_attack_time = 0
        self.attack_duration = 150  # ms

        self.font = pygame.font.Font(None, 60)

        # menus
        self.menu_buttons = self._create_menu_buttons()
        self.difficulty_buttons = self._create_difficulty_buttons()
        self.hero_buttons = self._create_hero_buttons()
        self.pause_buttons = self._create_pause_menu_buttons()

        # inventory pop-up & transient messages
        self.show_inventory = False
        self.message = ""
        self.message_start_time = 0
        self.message_duration = 0

        # menu background
        img_path = os.path.join(
            os.path.dirname(__file__), "..", "assets", "DungeonBackground.png"
        )
        self.menu_bg = pygame.transform.scale(
            pygame.image.load(img_path).convert(), self.screen.get_size()
        )

    # ────────────────────────── button factories ──────────────────────────
    def _create_menu_buttons(self):
>>>>>>> Stashed changes
        w, h = self.screen.get_size()
        mk = lambda txt, y: Button(
            txt, pygame.Rect(w // 2 - 100, y, 200, 60),
            self.font, (200, 200, 200), (255, 255, 0)
        )
        return [
<<<<<<< Updated upstream
            Button("PLAY", pygame.Rect(w // 2 - 100, h // 2 - 150, 200, 60), self.font, (200, 200, 200), (255, 255, 0)),
            Button("LOAD", pygame.Rect(w // 2 - 100, h // 2 - 50, 200, 60), self.font, (200, 200, 200), (255, 255, 0)),
            Button("ABOUT", pygame.Rect(w // 2 - 100, h // 2 + 50, 200, 60), self.font, (200, 200, 200), (255, 255, 0)),
            Button("QUIT", pygame.Rect(w // 2 - 100, h // 2 + 150, 200, 60), self.font, (200, 200, 200), (255, 255, 0)),
=======
            mk("PLAY",  h // 2 - 150),
            mk("LOAD",  h // 2 -  50),
            mk("ABOUT", h // 2 +  50),
            mk("QUIT",  h // 2 + 150),
>>>>>>> Stashed changes
        ]

    def _create_difficulty_buttons(self):
        w, h = self.screen.get_size()
        return [
<<<<<<< Updated upstream
            Button("EASY", pygame.Rect(w // 2 - 100, h // 2 - 100, 200, 60), self.font, (200, 200, 200), (0, 255, 0)),
            Button("MEDIUM", pygame.Rect(w // 2 - 100, h // 2, 200, 60), self.font, (200, 200, 200), (255, 165, 0)),
            Button("HARD", pygame.Rect(w // 2 - 100, h // 2 + 100, 200, 60), self.font, (200, 200, 200), (255, 0, 0)),
        ]

    def draw_buttons(self, buttons):
        for button in buttons:
            button.draw(self.screen)

    def draw_maze(self, game):
=======
            Button("EASY",   pygame.Rect(w // 2 - 100, h // 2 - 100, 200, 60),
                   self.font, (200, 200, 200), (  0, 255,   0)),
            Button("MEDIUM", pygame.Rect(w // 2 - 100, h // 2,       200, 60),
                   self.font, (200, 200, 200), (255, 165,   0)),
            Button("HARD",   pygame.Rect(w // 2 - 100, h // 2 + 100, 200, 60),
                   self.font, (200, 200, 200), (255,   0,   0)),
        ]

    def _create_hero_buttons(self):
        w, h = self.screen.get_size()
        return [
            Button("WARRIOR",  pygame.Rect(w // 2 - 150, h // 2 - 120, 300, 60),
                   self.font, (200, 200, 200), (255, 255,   0)),
            Button("PRIESTESS",pygame.Rect(w // 2 - 150, h // 2 -  40, 300, 60),
                   self.font, (200, 200, 200), (  0, 255, 255)),
            Button("THIEF",    pygame.Rect(w // 2 - 150, h // 2 +  40, 300, 60),
                   self.font, (200, 200, 200), (255, 165,   0)),
        ]

    def _create_pause_menu_buttons(self):
        w, h = self.screen.get_size()
        return [
            Button("RESUME", pygame.Rect(w // 2 - 100, h // 2 - 150, 200, 60),
                   self.font, (200, 200, 200), (  0, 255,   0)),
            Button("SAVE",   pygame.Rect(w // 2 - 100, h // 2 -  50, 200, 60),
                   self.font, (200, 200, 200), (255, 255,   0)),
            Button("ABOUT",  pygame.Rect(w // 2 - 100, h // 2 +  50, 200, 60),
                   self.font, (200, 200, 200), (  0, 128, 255)),
            Button("BACK",   pygame.Rect(w // 2 - 100, h // 2 + 150, 200, 60),
                   self.font, (200, 200, 200), (255,   0,   0)),
        ]

    # ────────────────────────── generic helpers ───────────────────────────
    def draw_buttons(self, buttons):
        self.screen.blit(self.menu_bg, (0, 0))
        for b in buttons:
            b.draw(self.screen)

    def display_message(self, msg: str, duration: int = 2000):
        self.message = msg
        self.message_start_time = pygame.time.get_ticks()
        self.message_duration = duration

    def draw_message(self):
        if (
            self.message and
            pygame.time.get_ticks() - self.message_start_time < self.message_duration
        ):
            txt = pygame.font.Font(None, 36).render(self.message, True, (255, 255, 0))
            self.screen.blit(txt, (30, 60))
        else:
            self.message = ""

    # ────────────────────────── HUD widgets ───────────────────────────────
    def health_bar(self, width, height, hero):
        """HP bar uses hero’s true max HP (fixes 125/100 bug)."""
        max_hp = getattr(hero, "_max_health_points", 100)
        hp     = max(0, hero.health_points)

        max_bar_w = width - 800
        bar_h = 20
        bar_x = 20
        bar_y = height - bar_h - 10

        ratio = hp / max_hp if max_hp else 0
        bar_w = int(max_bar_w * ratio)

        pygame.draw.rect(self.screen, (0, 255, 0),
                         pygame.Rect(bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(self.screen, (0, 0, 0),
                         pygame.Rect(bar_x, bar_y, max_bar_w, bar_h), 2)

        lbl = pygame.font.Font(None, 30).render(f"HP: {hp}/{max_hp}",
                                                True, (255, 255, 255))
        self.screen.blit(lbl, lbl.get_rect(
            center=(bar_x + max_bar_w // 2, bar_y + bar_h // 2)))

    def draw_status_bar(self, screen, text):
        font = pygame.font.SysFont("Arial", 28)
        surf = font.render(text, True, (255, 255, 255))
        rect = pygame.Rect(10, 10, surf.get_width() + 20, surf.get_height() + 10)
        pygame.draw.rect(screen, (0, 0, 0), rect)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2)
        screen.blit(surf, (rect.x + 10, rect.y + 5))

    # ────────────────────────── maze view ────────────────────────────────
    def draw_maze(self, game, W, H, hero, backpack):
>>>>>>> Stashed changes
        dungeon = game.dungeon
        hr, hc = dungeon.hero_x, dungeon.hero_y
        aim_dx, aim_dy = game.aim_vector
        view_rows, view_cols = self.view_rows, self.view_cols

<<<<<<< Updated upstream
        start_r = max(0, min(dungeon.rows - view_rows, hero_x - view_rows // 2))
        start_c = max(0, min(dungeon.cols - view_cols, hero_y - view_cols // 2))
        end_r = min(start_r + view_rows, dungeon.rows)
        end_c = min(start_c + view_cols, dungeon.cols)
=======
        sr = max(0, min(dungeon.rows - self.view_rows, hr - self.view_rows // 2))
        sc = max(0, min(dungeon.cols - self.view_cols, hc - self.view_cols // 2))
        er = sr + self.view_rows
        ec = sc + self.view_cols
>>>>>>> Stashed changes

        colors = {
            "wall":    (30, 30, 30),
            "hallway": (220, 220, 220),
<<<<<<< Updated upstream
            "door": (0, 128, 255),
            "exit": (0, 255, 128)
        }
    #update varianles better
        for r in range(start_r, end_r):
            for c in range(start_c, end_c):
=======
            "door":    (0, 128, 255),
            "exit":    (0, 255, 128),
        }

        for r in range(sr, er):
            for c in range(sc, ec):
>>>>>>> Stashed changes
                cell = dungeon.maze[r][c]
                sx = (c - sc) * self.cell_size
                sy = (r - sr) * self.cell_size
                rect = pygame.Rect(sx, sy, self.cell_size, self.cell_size)

<<<<<<< Updated upstream
                if not cell.explored:
                    color = (0, 0, 0)
                elif not cell.visible:
                    base = base_colors.get(cell.cell_type, (100, 100, 100))
                    color = tuple(int(x * 0.35) for x in base)
                else:
                    color = base_colors.get(cell.cell_type, (255, 0, 255))
=======
                now = pygame.time.get_ticks()
                vision_on = (
                    game.vision_reveal_start and
                    now - game.vision_reveal_start < game.vision_reveal_duration
                )

                if not cell.explored:
                    col = (0, 0, 0)
                elif vision_on or cell.visible:
                    col = colors.get(cell.cell_type, (255, 0, 255))
                else:
                    base = colors.get(cell.cell_type, (100, 100, 100))
                    col = tuple(int(x * 0.35) for x in base)
>>>>>>> Stashed changes

                pygame.draw.rect(self.screen, col, rect)

<<<<<<< Updated upstream
                if r == hero_x and c == hero_y:
                    pygame.draw.circle(self.screen, (255, 0, 0), rect.center, self.cell_size // 3)


                aim_dx, aim_dy = game.aim_vector
                center_x = (hero_y - start_c) * self.cell_size + self.cell_size // 2
                center_y = (hero_x - start_r) * self.cell_size + self.cell_size // 2
                end_x = int(center_x + aim_dx * 40)
                end_y = int(center_y + aim_dy * 40)
                pygame.draw.line(self.screen, (255, 255, 0), (center_x, center_y), (end_x, end_y), 2)

                current_time = pygame.time.get_ticks()
                if current_time - self.last_attack_time < self.attack_duration:
                    style = game.hero.get_melee_style()
                    attack_angle = math.atan2(aim_dy, aim_dx)
                    color = style["color"]
                    arc_width = style["arc_width"]
                    reach = style["reach"]
                    swings = style.get("swings", 1)

                    for i in range(swings):
                        offset = (-1 + 2 * i) * (arc_width / 2) if swings > 1 else 0
                        angle = attack_angle + offset
                        ax = int(center_x + reach * math.cos(angle))
                        ay = int(center_y + reach * math.sin(angle))
                        pygame.draw.line(self.screen, color, (center_x, center_y), (ax, ay), 4)

    def draw_room(self, game, width, height,ogre,skeleton,gremlin):
        room = game.active_room
        view_rows = self.view_rows
        view_cols = self.view_cols

        hero_r, hero_c = room.get_hero_position()
        monsters = room.get_monsters()
        start_r = max(0, min(max(0, room.height - view_rows), hero_r - view_rows // 2))
        start_c = max(0, min(max(0, room.width - view_cols), hero_c - view_cols // 2))
        end_r = min(start_r + view_rows, room.height)
        end_c = min(start_c + view_cols, room.width)
=======
        # hero icon
        hrect = pygame.Rect((hc - sc) * self.cell_size,
                            (hr - sr) * self.cell_size,
                            self.cell_size, self.cell_size)
        pygame.draw.circle(self.screen, (255, 0, 0),
                           hrect.center, self.cell_size // 3)

        # aim line
        cx, cy = hrect.center
        ex = int(cx + aim_dx * 40)
        ey = int(cy + aim_dy * 40)
        pygame.draw.line(self.screen, (255, 255, 0),
                         (cx, cy), (ex, ey), 2)

        # melee arc animation
        if pygame.time.get_ticks() - self.last_attack_time < self.attack_duration:
            style = game.hero.get_melee_style()
            ang   = math.atan2(aim_dy, aim_dx)
            reach = style["reach"]
            aw    = style["arc_width"]
            swings= style.get("swings", 1)
            col   = style["color"]
            for i in range(swings):
                off = (-1 + 2 * i) * aw / 2 if swings > 1 else 0
                a   = ang + off
                ax  = int(cx + reach * math.cos(a))
                ay  = int(cy + reach * math.sin(a))
                pygame.draw.line(self.screen, col, (cx, cy), (ax, ay), 4)

        self.health_bar(W, H, hero)
        if self.show_inventory:
            self.draw_inventory(backpack)
        self.draw_message()

    # ────────────────────────── room view ────────────────────────────────
    def draw_room(
        self, game, W, H, hero, backpack,
        Ogre, Skeleton, Gremlin,
        enc_sym, poly_sym, inh_sym, abs_sym
    ):
        room = game.active_room
        hr, hc = room.get_hero_position()

        sr = max(0, min(max(0, room.height - self.view_rows), hr - self.view_rows // 2))
        sc = max(0, min(max(0, room.width  - self.view_cols), hc - self.view_cols  // 2))
        er = min(sr + self.view_rows, room.height)
        ec = min(sc + self.view_cols, room.width)

        rw = ec - sc
        rh = er - sr
        cell = min(W // rw, H // rh)

        off_x = (W - rw * cell) // 2
        off_y = (H - rh * cell) // 2
>>>>>>> Stashed changes

        colors = {
            "wall": (40, 40, 40),
            "floor": (230, 230, 230),
            "door": (0, 128, 255),
<<<<<<< Updated upstream
            "Encapsulation": (255, 215, 0),
            "Polymorphism": (255, 215, 0),
            "Abstraction": (255, 215, 0),
            "Inheritance": (255, 215, 0),
            "Health Potion": (255, 192, 203),
            "Vision Potion": (255, 192, 203)
        }

        room_tile_width = end_c - start_c
        room_tile_height = end_r - start_r

        cell_w = width // room_tile_width
        cell_h = height // room_tile_height
        cell_size = min(cell_w, cell_h)  # Make tiles square

        # Draw tiles
        for r in range(start_r, end_r):
            for c in range(start_c, end_c):
                tile = room.get_tile(r, c)
                screen_x = (c - start_c) * cell_size
                screen_y = (r - start_r) * cell_size
                rect = pygame.Rect(screen_x, screen_y, cell_size, cell_size)
                color = base_colors.get(tile, (255, 0, 255))
                pygame.draw.rect(self.screen, color, rect)

        # Draw hero
        center_x = (hero_c - start_c) * cell_size + cell_size // 2
        center_y = (hero_r - start_r) * cell_size + cell_size // 2
        pygame.draw.circle(self.screen, (255, 0, 0), (center_x, center_y), cell_size // 3)

        # Draw aim direction
        aim_dx, aim_dy = game.aim_vector
        end_x = int(center_x + aim_dx * 40)
        end_y = int(center_y + aim_dy * 40)
        pygame.draw.line(self.screen, (255, 255, 0), (center_x, center_y), (end_x, end_y), 2)

        for monster, (mr, mc) in monsters.items():
            screen_x = (mc - start_c) * self.cell_size
            screen_y = (mr - start_r) * self.cell_size

            # Determine monster base color
            if isinstance(monster, ogre):
                base_color = (0, 250, 0)
            elif isinstance(monster, skeleton):
                base_color = (0, 0, 0)
            elif isinstance(monster, gremlin):
                base_color = (0, 0, 250)
            else:
                base_color = (255, 0, 255)  # fallback

            pos = (screen_x + self.cell_size // 2, screen_y + self.cell_size // 2)

            # Flashing outline if recently hit
            if hasattr(monster, "is_flashing") and monster.is_flashing():
                pygame.draw.circle(self.screen, (255, 0, 0), pos, self.cell_size // 2)  # red outer outline

            pygame.draw.circle(self.screen, base_color, pos, self.cell_size // 3)  # inner color

        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time < self.attack_duration:
            style = game.hero.get_melee_style()
            attack_angle = math.atan2(aim_dy, aim_dx)
            color = style["color"]
            arc_width = style["arc_width"]
            reach = style["reach"]
            swings = style.get("swings", 1)

=======
            "pit": (0, 0, 0),          # black pits
            enc_sym: (255, 215, 0),
            poly_sym: (255, 215, 0),
            inh_sym: (255, 215, 0),
            abs_sym: (255, 215, 0),
            "Health Potion": (255, 192, 203),
            "Vision Potion": (128,   0, 128),
        }

        for r in range(sr, er):
            for c in range(sc, ec):
                tile = room.get_tile(r, c)
                sx = off_x + (c - sc) * cell
                sy = off_y + (r - sr) * cell
                pygame.draw.rect(
                    self.screen,
                    colors.get(tile, (255, 0, 255)),
                    pygame.Rect(sx, sy, cell, cell)
                )

        # hero circle
        cx = off_x + (hc - sc) * cell + cell // 2
        cy = off_y + (hr - sr) * cell + cell // 2
        pygame.draw.circle(self.screen, (255, 0, 0), (cx, cy), cell // 3)

        # aim line
        ax, ay = game.aim_vector
        ex = int(cx + ax * 40)
        ey = int(cy + ay * 40)
        pygame.draw.line(self.screen, (255, 255, 0), (cx, cy), (ex, ey), 2)

        # monsters
        for m, (mr, mc) in room.get_monsters().items():
            sx = off_x + (mc - sc) * cell + cell // 2
            sy = off_y + (mr - sr) * cell + cell // 2
            if isinstance(m, Ogre):
                col = (  0, 250,   0)
            elif isinstance(m, Skeleton):
                col = (230, 230, 230)
            elif isinstance(m, Gremlin):
                col = (  0,   0, 250)
            else:
                col = (255,   0, 255)
            if getattr(m, "is_flashing", lambda: False)():
                pygame.draw.circle(self.screen, (255,   0,   0), (sx, sy), cell // 2)
            pygame.draw.circle(self.screen, col, (sx, sy), cell // 3)

        # projectiles
        for p in game.projectiles:
            px, py = p.get_position()
            dx = off_x + px - sc * cell
            dy = off_y + py - sr * cell
            pygame.draw.circle(self.screen, (255, 255, 255), (int(dx), int(dy)), 5)

        # melee arc animation
        if pygame.time.get_ticks() - self.last_attack_time < self.attack_duration:
            st = game.hero.get_melee_style()
            ang = math.atan2(ay, ax)
            reach = st["reach"]
            aw = st["arc_width"]
            swings = st.get("swings", 1)
            col = st["color"]
>>>>>>> Stashed changes
            for i in range(swings):
                off = (-1 + 2 * i) * aw / 2 if swings > 1 else 0
                a = ang + off
                x2 = int(cx + reach * math.cos(a))
                y2 = int(cy + reach * math.sin(a))
                pygame.draw.line(self.screen, col, (cx, cy), (x2, y2), 4)

<<<<<<< Updated upstream
    def show_melee_attack(self):
        self.last_attack_time = pygame.time.get_ticks()
=======
        self.health_bar(W, H, hero)
        if self.show_inventory:
            self.draw_inventory(backpack)
        self.draw_message()

    # ────────────────────────── misc helpers ─────────────────────────────
    def show_melee_attack(self):
        self.last_attack_time = pygame.time.get_ticks()

    def draw_inventory(self, backpack):
        rect = pygame.Rect(100, 100, 400, 300)
        pygame.draw.rect(self.screen, (50, 50, 50), rect)
        pygame.draw.rect(self.screen, (255, 255, 255), rect, 3)

        font = pygame.font.Font(None, 30)
        self.screen.blit(font.render("Inventory", True, (255, 255, 0)),
                         (rect.x + 10, rect.y + 10))

        items = {}
        if backpack.get_healing_cntr() > 0:
            items["Health Potion"] = backpack.get_healing_cntr()
        if backpack.get_vision_cntr() > 0:
            items["Vision Potion"] = backpack.get_vision_cntr()

        from collections import Counter
        for k, v in Counter(backpack.get_inventory()).items():
            if k in {"A", "E", "I", "P"}:
                items[k] = v

        y = rect.y + 40
        for item, cnt in items.items():
            txt = font.render(f"- {item}: {cnt}", True, (255, 255, 255))
            self.screen.blit(txt, (rect.x + 20, y))
            y += 25

    def draw_about_screen(self):
        self.screen.fill((0, 0, 0))
        lines = [
            "Dungeon Adventure Game",
            "Version: 1.0 (June 2025)",
            "Authors: Rudolf Arakelyan, Nikita Bizyuk,",
            "         Collins Mbugua, Ian Fuhr",
            "",
            "OBJECTIVE:",
            "Find all 4 Pillars of OOP:",
            "- Abstraction (A)",
            "- Encapsulation (E)",
            "- Inheritance (I)",
            "- Polymorphism (P)",
            "",
            "Enter rooms, defeat monsters, survive traps.",
            "Reach the exit with all pillars to win!",
            "",
            "Press ESC to return.",
        ]
        font = pygame.font.SysFont("georgia", 36, bold=True)
        y = 80
        box_w = self.screen.get_width() - 200
        box_h = len(lines) * 45 + 40
        pygame.draw.rect(self.screen, (30, 30, 30),
                         (100, y - 30, box_w, box_h))
        pygame.draw.rect(self.screen, (210, 140, 70),
                         (100, y - 30, box_w, box_h), 4)
        for line in lines:
            txt = font.render(line, True, (210, 140, 70))
            self.screen.blit(txt, txt.get_rect(
                center=(self.screen.get_width() // 2, y)))
            y += 45
>>>>>>> Stashed changes
