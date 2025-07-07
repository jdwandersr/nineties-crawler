import pygame
from typing import Any, Optional, List
from src.dungeon import Dungeon
from src.combat import CombatEncounter


class MainMenu:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font = pygame.font.SysFont("Consolas", 36)
        self.title = self.font.render("Nineties Crawler", True, (255, 255, 255))
        self.subtitle = pygame.font.SysFont("Consolas", 24).render(
            "Press [N] for New Game or [ESC] to quit", True, (200, 200, 200)
        )
        self.instructions = pygame.font.SysFont("Consolas", 16).render(
            "In game: WASD/Arrow keys to move, Enter on stairs, ESC to return", True, (150, 150, 150)
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
        self.screen.blit(
            self.instructions, (w // 2 - self.instructions.get_width() // 2, h // 3 + 100)
        )


class DungeonView:
    TILE_SIZE = 32
    TILE_COLORS = {
        "walkable": (40, 40, 40),
        "wall": (80, 20, 20),
        "clue": (40, 40, 120),
        "player": (60, 220, 60),
        "up_stairs": (220, 220, 60),
        "down_stairs": (220, 120, 60),
        "mob": (220, 60, 60),  # Red color for mobs
    }

    def __init__(self, screen: pygame.Surface, dungeon: Dungeon, player_pos: List[int]) -> None:
        self.screen = screen
        self.dungeon = dungeon
        self.player_pos = player_pos  # [x, y]
        self.font = pygame.font.SysFont("Consolas", 24)
        self.info_text: Optional[pygame.Surface] = None
        self.info_timer: int = 0

    def handle_event(self, event: Any) -> Optional[str]:
        dx, dy = 0, 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "main_menu"
            elif event.key in (pygame.K_UP, pygame.K_w):
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
                
                # Check for mob encounter first
                if tile.mob and tile.mob.is_alive():
                    # When player steps on a tile with a living mob, trigger combat
                    self.info_text = self.font.render(f"You encountered a {tile.mob.name}! Entering combat...", True, (255, 100, 100))
                    self.info_timer = 120
                    return "combat"  # Signal to game state manager to switch to combat mode
                
                # Check for clue
                clue = self.dungeon.get_clue(new_x, new_y)
                if clue:
                    self.info_text = self.font.render(clue, True, (255, 255, 200))
                    self.info_timer = 120  # Show for 2 seconds (60fps*2)
                # Check for stairs
                elif tile.has_up_stairs:
                    self.info_text = self.font.render("You found up stairs! Press Enter to use them.", True, (255, 255, 200))
                    self.info_timer = 120
                elif tile.has_down_stairs:
                    self.info_text = self.font.render("You found down stairs! Press Enter to use them.", True, (255, 255, 200))
                    self.info_timer = 120
        
        # Check if player is on stairs and presses Enter
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            px, py = self.player_pos
            tile = self.dungeon.grid[py][px]
            if tile.has_up_stairs or tile.has_down_stairs:
                return "main_menu"
        
        return None

    def render(self) -> None:
        # Draw dungeon tiles
        for y, row in enumerate(self.dungeon.grid):
            for x, tile in enumerate(row):
                color = (
                    self.TILE_COLORS["walkable"] if tile.walkable else self.TILE_COLORS["wall"]
                )
                if tile.has_clue:
                    color = self.TILE_COLORS["clue"]
                elif tile.has_up_stairs:
                    color = self.TILE_COLORS["up_stairs"]
                elif tile.has_down_stairs:
                    color = self.TILE_COLORS["down_stairs"]
                elif tile.mob and tile.mob.is_alive():
                    color = self.TILE_COLORS["mob"]
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


class CombatView:
    """
    Simple combat UI for mob encounters.
    
    This view provides a turn-based combat interface that displays:
    - Party member status (HP, class, alive/dead)
    - Enemy status (HP, alive/dead)
    - Combat log with recent actions
    - Turn-based combat controls
    
    Controls:
    - SPACE: Execute combat action (attack)
    - ESC: Return to main menu
    """
    
    def __init__(self, screen: pygame.Surface, combat: CombatEncounter) -> None:
        self.screen = screen
        self.combat = combat
        self.font = pygame.font.SysFont("Consolas", 20)
        self.title_font = pygame.font.SysFont("Consolas", 28)
        self.info_messages: List[str] = []
    
    def handle_event(self, event: Any) -> Optional[str]:
        """Handle combat input. Returns state change or None."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "main_menu"
            elif event.key == pygame.K_SPACE:
                if self.combat.is_over():
                    return "explore"  # Return to exploration
                else:
                    # Execute combat turn
                    if self.combat.turn == 0:  # Party turn
                        self.combat.party_action("attack", 0)
                        self.info_messages.append("Party attacks!")
                        if not self.combat.is_over():
                            self.combat.next_turn()
                    else:  # Enemy turn
                        self.combat.enemy_action()
                        self.info_messages.append("Enemies attack!")
                        if not self.combat.is_over():
                            self.combat.next_turn()
                    
                    # Keep only last 5 messages
                    self.info_messages = self.info_messages[-5:]
        
        return None
    
    def render(self) -> None:
        """Render the combat screen."""
        self.screen.fill((20, 20, 20))
        
        # Title
        title = self.title_font.render("COMBAT", True, (255, 255, 255))
        self.screen.blit(title, (40, 40))
        
        # Party status
        y_offset = 100
        party_title = self.font.render("PARTY:", True, (100, 255, 100))
        self.screen.blit(party_title, (40, y_offset))
        y_offset += 30
        
        for i, member in enumerate(self.combat.party):
            status = "ALIVE" if member.is_alive() else "DEAD"
            color = (255, 255, 255) if member.is_alive() else (100, 100, 100)
            text = self.font.render(f"{member.name} ({member.char_class}): {member.hp}/{member.max_hp} HP - {status}", True, color)
            self.screen.blit(text, (60, y_offset))
            y_offset += 25
        
        # Enemy status
        y_offset += 20
        enemy_title = self.font.render("ENEMIES:", True, (255, 100, 100))
        self.screen.blit(enemy_title, (40, y_offset))
        y_offset += 30
        
        for i, enemy in enumerate(self.combat.enemies):
            status = "ALIVE" if enemy.is_alive() else "DEAD"
            color = (255, 255, 255) if enemy.is_alive() else (100, 100, 100)
            text = self.font.render(f"{enemy.name}: {enemy.hp}/{enemy.max_hp} HP - {status}", True, color)
            self.screen.blit(text, (60, y_offset))
            y_offset += 25
        
        # Combat messages
        y_offset += 20
        messages_title = self.font.render("COMBAT LOG:", True, (255, 255, 100))
        self.screen.blit(messages_title, (40, y_offset))
        y_offset += 30
        
        for message in self.info_messages:
            text = self.font.render(message, True, (200, 200, 200))
            self.screen.blit(text, (60, y_offset))
            y_offset += 25
        
        # Instructions
        if self.combat.is_over():
            if all(not e.is_alive() for e in self.combat.enemies):
                result = self.font.render("VICTORY! Press SPACE to continue", True, (100, 255, 100))
            else:
                result = self.font.render("DEFEAT! Press SPACE to continue", True, (255, 100, 100))
            self.screen.blit(result, (40, self.screen.get_height() - 80))
        else:
            whose_turn = "Party" if self.combat.turn == 0 else "Enemy"
            turn_text = self.font.render(f"{whose_turn} turn - Press SPACE to attack", True, (255, 255, 255))
            self.screen.blit(turn_text, (40, self.screen.get_height() - 80))
        
        escape_text = self.font.render("Press ESC to return to main menu", True, (150, 150, 150))
        self.screen.blit(escape_text, (40, self.screen.get_height() - 50))