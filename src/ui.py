import pygame
from typing import Any


class MainMenu:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font = pygame.font.SysFont("Consolas", 36)
        self.title = self.font.render("Nineties Crawler", True, (255, 255, 255))
        self.subtitle = pygame.font.SysFont("Consolas", 24).render(
            "Press [ESC] to quit", True, (200, 200, 200)
        )

    def handle_event(self, event: Any) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    def render(self) -> None:
        w, h = self.screen.get_size()
        self.screen.blit(
            self.title, (w // 2 - self.title.get_width() // 2, h // 3)
        )
        self.screen.blit(
            self.subtitle, (w // 2 - self.subtitle.get_width() // 2, h // 3 + 60)
        )