import pygame
from typing import Optional
from src.ui import MainMenu, DungeonView
from src.dungeon import Dungeon
from src.player import get_default_party


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Nineties Crawler")
        self.clock = pygame.time.Clock()
        self.running = True

        # States: "main_menu", "explore"
        self.state: str = "main_menu"
        self.menu = MainMenu(self.screen)
        self.dungeon: Optional[Dungeon] = None
        self.party = get_default_party()
        self.dungeon_view: Optional[DungeonView] = None

    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.state == "main_menu":
                    menu_action = self.menu.handle_event(event)
                    if menu_action == "new_game":
                        self.dungeon = Dungeon()
                        self.player_pos = list(self.dungeon.get_random_walkable())
                        self.dungeon_view = DungeonView(
                            self.screen, self.dungeon, self.player_pos
                        )
                        self.state = "explore"
                elif self.state == "explore" and self.dungeon_view:
                    action = self.dungeon_view.handle_event(event)
                    if action == "main_menu":
                        self.state = "main_menu"
                        self.dungeon = None
                        self.dungeon_view = None

            self.screen.fill((0, 0, 0))
            if self.state == "main_menu":
                self.menu.render()
            elif self.state == "explore" and self.dungeon_view:
                self.dungeon_view.render()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()