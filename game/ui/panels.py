from typing import List

import pygame

from .. import config
from .button import Button

CLOSE_BUTTON_SIZE = 28


class Panel:

    def __init__(self, rect, title: str):
        self.rect = pygame.Rect(rect)
        self.title = title
        self.visible = False
        self.close_button = Button(
            (
                self.rect.right - CLOSE_BUTTON_SIZE - 8,
                self.rect.top + 8,
                CLOSE_BUTTON_SIZE,
                CLOSE_BUTTON_SIZE,
            ),
            "X",
            color=config.RED,
        )

    def open(self) -> None:
        self.visible = True

    def close(self) -> None:
        self.visible = False

    def toggle(self) -> None:
        self.visible = not self.visible

    def handle_event(self, mouse_pos) -> bool:
        if not self.visible:
            return False
        if self.close_button.handle_click(mouse_pos):
            self.close()
            return True
        return False

    def contains(self, mouse_pos) -> bool:
        return self.visible and self.rect.collidepoint(mouse_pos)

    def _draw_frame(self, screen: pygame.Surface, font: pygame.font.Font, mouse_pos) -> None:
        backdrop = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.rect(backdrop, (*config.PANEL_BG, 235), backdrop.get_rect(), border_radius=14)
        pygame.draw.rect(backdrop, config.PANEL_BORDER, backdrop.get_rect(), width=2, border_radius=14)
        screen.blit(backdrop, self.rect.topleft)

        title_surf = font.render(self.title, True, config.TEXT_LIGHT)
        screen.blit(title_surf, (self.rect.left + 16, self.rect.top + 12))
        self.close_button.draw(screen, font, mouse_pos)

    def draw(self, screen: pygame.Surface, font: pygame.font.Font, mouse_pos) -> None:
        raise NotImplementedError


class DocumentPanel(Panel):

    def __init__(self, rect, document_image: pygame.Surface):
        super().__init__(rect, "DOCUMENTO DE IDENTIFICACAO")

        padding = 40
        header_h = 56
        max_w = self.rect.width - padding * 2
        max_h = self.rect.height - padding - header_h
        img_w, img_h = document_image.get_size()
        scale = min(max_w / img_w, max_h / img_h)
        size = (int(img_w * scale), int(img_h * scale))

        self.document_surface = pygame.transform.smoothscale(document_image, size)
        self.document_rect = self.document_surface.get_rect(
            center=(self.rect.centerx, self.rect.top + header_h + max_h // 2)
        )

    def handle_event(self, mouse_pos) -> bool:
        if super().handle_event(mouse_pos):
            return True
        return self.contains(mouse_pos)

    def draw(self, screen: pygame.Surface, font: pygame.font.Font, mouse_pos) -> None:
        if not self.visible:
            return
        self._draw_frame(screen, font, mouse_pos)
        screen.blit(self.document_surface, self.document_rect)


GENERIC_ANSWERS = {
    "Motivo da entrada": "Vim a trabalho.",
    "Documentos": "Esta tudo em ordem, pode conferir.",
    "Aparência": "Minha aparência? Está normal",
}


class QuestionPanel(Panel):

    ROW_H = 56
    ROW_GAP = 14

    def __init__(self, rect, questions: List[str]):
        super().__init__(rect, "PERGUNTAR")

        self.questions = questions
        self.question_buttons = []
        self.selected_answer = ""
        top = self.rect.top + 56
        for i, question in enumerate(questions):
            btn_rect = (
                self.rect.left + 20,
                top + i * (self.ROW_H + self.ROW_GAP),
                self.rect.width - 40,
                self.ROW_H,
            )
            self.question_buttons.append(Button(btn_rect, question, color=config.BLUE))

        answer_top = top + len(questions) * (self.ROW_H + self.ROW_GAP)
        self.answer_rect = pygame.Rect(self.rect.left + 20, answer_top, self.rect.width - 40, 40)

    def close(self) -> None:
        super().close()
        self.selected_answer = ""

    def handle_event(self, mouse_pos) -> bool:
        if super().handle_event(mouse_pos):
            return True
        if not self.visible:
            return False
        for button in self.question_buttons:
            if button.handle_click(mouse_pos):
                self.selected_answer = GENERIC_ANSWERS.get(button.label, "")
                return True
        return self.contains(mouse_pos)

    def draw(self, screen: pygame.Surface, font: pygame.font.Font, mouse_pos) -> None:
        if not self.visible:
            return
        self._draw_frame(screen, font, mouse_pos)
        for button in self.question_buttons:
            button.draw(screen, font, mouse_pos)

        if self.selected_answer:
            answer_surf = font.render(self.selected_answer, True, config.TEXT_LIGHT)
            screen.blit(answer_surf, answer_surf.get_rect(midtop=self.answer_rect.midtop))
