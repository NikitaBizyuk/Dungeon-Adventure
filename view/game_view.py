import pygame


class Button:
    def __init__(self, text, rect, font, color, hover_color):
        self.text = text
        self.rect = rect
        self.font = font
        self.color = color
        self.hover_color = hover_color

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        text_surf = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


class GameView:
    """Handles menu UI and dungeon rendering."""

    def __init__(self, screen, cell_size, view_rows, view_cols):
        self.screen = screen
        self.cell_size = cell_size
        self.view_rows = view_rows
        self.view_cols = view_cols
        self.font = pygame.font.Font(None, 60)
        self.menu_buttons = self._create_menu_buttons()
        self.difficulty_buttons = self._create_difficulty_buttons()

    # -------------------- menus -------------------- #
    def _create_menu_buttons(self):
        w, h = self.screen.get_size()
        return [
            Button("PLAY", pygame.Rect(w // 2 - 100, h // 2 - 100, 200, 60),
                   self.font, (200, 200, 200), (255, 255, 0)),
            Button("LOAD", pygame.Rect(w // 2 - 100, h // 2, 200, 60),
                   self.font, (200, 200, 200), (255, 255, 0)),
            Button("ABOUT", pygame.Rect(w // 2 - 100, h // 2 + 100, 200, 60),
                   self.font, (200, 200, 200), (255, 255, 0)),
        ]

    def _create_difficulty_buttons(self):
        w, h = self.screen.get_size()
        return [
            Button("EASY", pygame.Rect(w // 2 - 100, h // 2 - 100, 200, 60),
                   self.font, (200, 200, 200), (0, 255, 0)),
            Button("MEDIUM", pygame.Rect(w // 2 - 100, h // 2, 200, 60),
                   self.font, (200, 200, 200), (255, 165, 0)),
            Button("HARD", pygame.Rect(w // 2 - 100, h // 2 + 100, 200, 60),
                   self.font, (200, 200, 200), (255, 0, 0)),
        ]

    def draw_buttons(self, buttons):
        for btn in buttons:
            btn.draw(self.screen)

    # -------------------- gameplay rendering -------------------- #
    def draw_maze(self, dungeon, hero_x, hero_y):
        """Render the dungeon overview while the hero is in the maze."""
        view_rows, view_cols = self.view_rows, self.view_cols

        start_r = max(0, min(dungeon.rows - view_rows, hero_x - view_rows // 2))
        start_c = max(0, min(dungeon.cols - view_cols, hero_y - view_cols // 2))
        end_r = min(start_r + view_rows, dungeon.rows)
        end_c = min(start_c + view_cols, dungeon.cols)

        base_colors = {
            "wall": (30, 30, 30),
            "hallway": (220, 220, 220),
            "door": (0, 128, 255),
            "exit": (0, 255, 128),
        }

        for r in range(start_r, end_r):
            for c in range(start_c, end_c):
                cell = dungeon.maze[r][c]
                screen_x = (c - start_c) * self.cell_size
                screen_y = (r - start_r) * self.cell_size
                rect = pygame.Rect(screen_x, screen_y, self.cell_size, self.cell_size)

                if not cell.explored:
                    color = (0, 0, 0)  # unexplored
                elif not cell.visible:
                    base = base_colors.get(cell.cell_type, (100, 100, 100))
                    color = tuple(int(x * 0.35) for x in base)  # dim explored
                else:
                    color = base_colors.get(cell.cell_type, (255, 0, 255))

                pygame.draw.rect(self.screen, color, rect)

                if r == hero_x and c == hero_y:
                    pygame.draw.circle(
                        self.screen, (255, 0, 0),
                        rect.center, self.cell_size // 3
                    )

    def draw_room(self, room, width, height, ogre, skeleton, gremlin):
        """Render the current room when the hero has entered it."""
        hero_r, hero_c = room.get_hero_position()
        monsters = room.get_monsters()

        start_r = max(0, min(max(0, room.height - self.view_rows),
                             hero_r - self.view_rows // 2))
        start_c = max(0, min(max(0, room.width - self.view_cols),
                             hero_c - self.view_cols // 2))
        end_r = min(start_r + self.view_rows, room.height)
        end_c = min(start_c + self.view_cols, room.width)

        base_colors = {
            "wall": (40, 40, 40),
            "floor": (230, 230, 230),
            "door": (0, 128, 255),
            "Encapsulation": (255, 215, 0),
            "Polymorphism": (255, 215, 0),
            "Abstraction": (255, 215, 0),
            "Inheritance": (255, 215, 0),
            "Health Potion": (255, 192, 203),
            "Vision Potion": (255, 192, 203),
        }

        for r in range(start_r, end_r):
            for c in range(start_c, end_c):
                tile = room.get_tile(r, c)

                room_tile_width = end_c - start_c
                room_tile_height = end_r - start_r
                cell_w = width // room_tile_width
                cell_h = height // room_tile_height
                cell_size = min(cell_w, cell_h)

                screen_x = (c - start_c) * cell_size
                screen_y = (r - start_r) * cell_size
                rect = pygame.Rect(screen_x, screen_y, cell_size, cell_size)

                color = base_colors.get(tile, (255, 0, 255))
                pygame.draw.rect(self.screen, color, rect)

        hero_center = (
            (hero_c - start_c) * self.cell_size + self.cell_size // 2,
            (hero_r - start_r) * self.cell_size + self.cell_size // 2,
        )
        pygame.draw.circle(
            self.screen, (250, 0, 0), hero_center, self.cell_size // 3
        )

        for monster, (mr, mc) in monsters.items():
            screen_x = (mc - start_c) * self.cell_size
            screen_y = (mr - start_r) * self.cell_size

            if isinstance(monster, ogre):
                color = (0, 250, 0)
            elif isinstance(monster, skeleton):
                color = (0, 0, 0)
            elif isinstance(monster, gremlin):
                color = (0, 0, 250)
            else:
                color = (255, 0, 0)

            pygame.draw.circle(
                self.screen, color,
                (screen_x + self.cell_size // 2,
                 screen_y + self.cell_size // 2),
                self.cell_size // 3
            )