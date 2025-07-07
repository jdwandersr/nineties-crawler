import pygame
from typing import Optional
from src.ui import MainMenu, DungeonView, CombatView
from src.dungeon import Dungeon
from src.player import get_default_party
from src.combat import CombatEncounter


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Nineties Crawler")
        self.clock = pygame.time.Clock()
        self.running = True

        # States: "main_menu", "explore", "combat"
        self.state: str = "main_menu"
        self.menu = MainMenu(self.screen)
        self.dungeon: Optional[Dungeon] = None
        self.party = get_default_party()
        self.dungeon_view: Optional[DungeonView] = None
        self.combat_view: Optional[CombatView] = None
        self.current_combat: Optional[CombatEncounter] = None

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
                        self.party = get_default_party()  # Reset party health
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
                    elif action == "combat":
                        # Start combat with the mob on current tile
                        px, py = self.player_pos
                        tile = self.dungeon.grid[py][px]
                        if tile.mob and tile.mob.is_alive():
                            self.current_combat = CombatEncounter(self.party, [tile.mob])
                            self.combat_view = CombatView(self.screen, self.current_combat)
                            self.state = "combat"
                elif self.state == "combat" and self.combat_view:
                    action = self.combat_view.handle_event(event)
                    if action == "main_menu":
                        self.state = "main_menu"
                        self.dungeon = None
                        self.dungeon_view = None
                        self.combat_view = None
                        self.current_combat = None
                    elif action == "explore":
                        # Return to exploration after combat
                        if self.current_combat and self.current_combat.is_over():
                            # If party won, remove the mob from the dungeon
                            if all(not e.is_alive() for e in self.current_combat.enemies):
                                px, py = self.player_pos
                                tile = self.dungeon.grid[py][px]
                                tile.mob = None  # Remove defeated mob
                        
                        self.state = "explore"
                        self.combat_view = None
                        self.current_combat = None

            self.screen.fill((0, 0, 0))
            if self.state == "main_menu":
                self.menu.render()
            elif self.state == "explore" and self.dungeon_view:
                self.dungeon_view.render()
            elif self.state == "combat" and self.combat_view:
                self.combat_view.render()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()