from typing import Tuple

import pygame

from .. import config


class Button:
    def __init__(self, rect, label: str, color: Tuple[int, int, int] = config.TEXT_LIGHT):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.color = color
        self.visible = True

    def handle_click(self, mouse_pos) -> bool:
        return self.visible and self.rect.collidepoint(mouse_pos)

    def draw(self, screen: pygame.Surface, font: pygame.font.Font, mouse_pos) -> None:
        if not self.visible:
            return

        hovered = self.rect.collidepoint(mouse_pos)
        panel = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        bg_alpha = 190 if hovered else 140
        pygame.draw.rect(panel, (10, 10, 10, bg_alpha), panel.get_rect(), border_radius=10)
        pygame.draw.rect(panel, self.color, panel.get_rect(), width=2, border_radius=10)
        screen.blit(panel, self.rect.topleft)

        text = font.render(self.label, True, config.TEXT_LIGHT)
        screen.blit(text, text.get_rect(center=self.rect.center))
