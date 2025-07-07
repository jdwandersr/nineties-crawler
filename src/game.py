import pygame
from src.ui import MainMenu
from typing import Optional


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Nineties Crawler")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state: Optional[str] = "main_menu"
        self.menu = MainMenu(self.screen)

    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if self.state == "main_menu":
                    self.menu.handle_event(event)

            self.screen.fill((0, 0, 0))
            if self.state == "main_menu":
                self.menu.render()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()