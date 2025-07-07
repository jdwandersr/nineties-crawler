import pygame
from typing import Any, Optional, List
from src.dungeon import Dungeon


class MainMenu:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font = pygame.font.SysFont("Consolas", 36)
        self.title = self.font.render("Nineties Crawler", True, (255, 255, 255))
        self.subtitle = pygame.font.SysFont("Consolas", 24).render(
            "Press [N] for New Game or [ESC] to quit", True, (200, 200, 200)
        )

    def handle_event(self, event: Any) -> Optional[str]:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            if event.key == pygame.K_n:
                return "new_game"
        return None

    def render(self) -> None:
        w, h = self.screen.get_size()
        self.screen.blit(
            self.title, (w // 2 - self.title.get_width() // 2, h // 3)
        )
        self.screen.blit(
            self.subtitle, (w // 2 - self.subtitle.get_width() // 2, h // 3 + 60)
        )


class DungeonView:
    TILE_SIZE = 32
    TILE_COLORS = {
        "walkable": (40, 40, 40),
        "wall": (80, 20, 20),
        "clue": (40, 40, 120),
        "player": (60, 220, 60),
    }

    def __init__(self, screen: pygame.Surface, dungeon: Dungeon, player_pos: List[int]) -> None:
        self.screen = screen
        self.dungeon = dungeon
        self.player_pos = player_pos  # [x, y]
        self.font = pygame.font.SysFont("Consolas", 24)
        self.info_text: Optional[pygame.Surface] = None
        self.info_timer: int = 0

    def handle_event(self, event: Any) -> None:
        dx, dy = 0, 0
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                dy = -1
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                dy = 1
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                dx = -1
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                dx = 1
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy
        if (dx != 0 or dy != 0) and 0 <= new_x < self.dungeon.width and 0 <= new_y < self.dungeon.height:
            tile = self.dungeon.grid[new_y][new_x]
            if tile.walkable:
                self.player_pos[0] = new_x
                self.player_pos[1] = new_y
                # Check for clue
                clue = self.dungeon.get_clue(new_x, new_y)
                if clue:
                    self.info_text = self.font.render(clue, True, (255, 255, 200))
                    self.info_timer = 120  # Show for 2 seconds (60fps*2)

    def render(self) -> None:
        # Draw dungeon tiles
        for y, row in enumerate(self.dungeon.grid):
            for x, tile in enumerate(row):
                color = (
                    self.TILE_COLORS["walkable"] if tile.walkable else self.TILE_COLORS["wall"]
                )
                if tile.has_clue:
                    color = self.TILE_COLORS["clue"]
                pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect(
                        40 + x * self.TILE_SIZE,
                        40 + y * self.TILE_SIZE,
                        self.TILE_SIZE,
                        self.TILE_SIZE,
                    ),
                )
        # Draw player
        px, py = self.player_pos
        pygame.draw.rect(
            self.screen,
            self.TILE_COLORS["player"],
            pygame.Rect(
                40 + px * self.TILE_SIZE,
                40 + py * self.TILE_SIZE,
                self.TILE_SIZE,
                self.TILE_SIZE,
            ),
        )

        # Draw info if any
        if self.info_text:
            self.screen.blit(self.info_text, (40, 40 + self.dungeon.height * self.TILE_SIZE + 10))
            self.info_timer -= 1
            if self.info_timer <= 0:
                self.info_text = None