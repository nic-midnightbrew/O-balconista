import random
import sys

import pygame

from . import config
from .npc import NPCS, NPCActor
from .ui.button import Button
from .ui.panels import DocumentPanel, QuestionPanel


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("O Balconistao")

        counter_raw = pygame.image.load(str(config.COUNTER_PATH))
        self.screen = pygame.display.set_mode(counter_raw.get_size())
        self.counter = counter_raw.convert_alpha()

        self.background = pygame.image.load(str(config.BACKGROUND_PATH)).convert_alpha()
        bg_size = (
            int(self.background.get_width() * config.BACKGROUND_SCALE),
            int(self.background.get_height() * config.BACKGROUND_SCALE),
        )
        self.background = pygame.transform.smoothscale(self.background, bg_size)
        self.background_rect = self.background.get_rect(center=config.WINDOW_HOLE.center)

        self.id_card = pygame.image.load(str(config.ID_CARD_PATH)).convert_alpha()

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 19, bold=True)

        self.npcs = list(NPCS)
        random.shuffle(self.npcs)
        self.npc_index = 0
        self.let_shapeshifter_pass = False
        self.shift_over = False

        self.npc = NPCActor(self.npcs[self.npc_index])

        self._build_buttons()
        self._build_panels()

        self.running = True

    def _build_buttons(self) -> None:
        total_w = config.BUTTON_W * 2 + config.BUTTON_GAP
        start_x = config.BUTTON_CENTER_X - total_w // 2

        self.deny_button = Button(
            (start_x, config.BUTTON_Y, config.BUTTON_W, config.BUTTON_H),
            "NAO DEIXAR PASSAR",
            color=config.RED,
        )
        self.allow_button = Button(
            (start_x + config.BUTTON_W + config.BUTTON_GAP, config.BUTTON_Y, config.BUTTON_W, config.BUTTON_H),
            "DEIXAR PASSAR",
            color=config.GREEN,
        )
        self.deny_button.visible = False
        self.allow_button.visible = False

        self.documents_button = Button(
            pygame.Rect(0, 0, config.DOCUMENTS_BUTTON_W, config.DOCUMENTS_BUTTON_H),
            "DOCUMENTOS",
            color=config.TEXT_LIGHT,
        )
        self.documents_button.rect.center = config.DOCUMENTS_BUTTON_CENTER

        self.ask_button = Button(
            pygame.Rect(0, 0, config.ASK_BUTTON_W, config.ASK_BUTTON_H),
            "PERGUNTAR",
            color=config.BLUE,
        )
        self.ask_button.rect.center = config.ASK_BUTTON_CENTER

        self.documents_button.visible = False
        self.ask_button.visible = False

    def _build_panels(self) -> None:
        doc_rect = pygame.Rect(0, 0, 460, 380)
        doc_rect.center = config.WINDOW_HOLE.center
        self.document_panel = DocumentPanel(doc_rect, self.id_card)

        question_rect = pygame.Rect(0, 0, 560, 340)
        question_rect.center = config.WINDOW_HOLE.center
        self.question_panel = QuestionPanel(question_rect, self.npc.profile.questions)

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(config.FPS) / 1000.0
            self._handle_events()
            self._update(dt)
            self._draw()
        pygame.quit()
        sys.exit()

    def _handle_events(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_click(mouse_pos)

    def _handle_click(self, mouse_pos) -> None:
        if self.shift_over:
            return

        if self.document_panel.handle_event(mouse_pos):
            return
        if self.question_panel.handle_event(mouse_pos):
            return

        if self.documents_button.handle_click(mouse_pos):
            self.question_panel.close()
            self.document_panel.toggle()
            return
        if self.ask_button.handle_click(mouse_pos):
            self.document_panel.close()
            self.question_panel.toggle()
            return

        if self.allow_button.handle_click(mouse_pos):
            self._decide(let_pass=True)
        elif self.deny_button.handle_click(mouse_pos):
            self._decide(let_pass=False)

    def _decide(self, let_pass: bool) -> None:
        current_npc = self.npc.profile
        if let_pass and not current_npc.is_human:
            self.let_shapeshifter_pass = True

        self.npc_index += 1
        if self.npc_index >= len(self.npcs):
            self.shift_over = True
            return

        self._next_npc()

    def _next_npc(self) -> None:
        self.npc.reset(self.npcs[self.npc_index])
        self.document_panel.close()
        self.question_panel.close()
        self.documents_button.visible = False
        self.ask_button.visible = False
        self.allow_button.visible = False
        self.deny_button.visible = False

    def _update(self, dt: float) -> None:
        if self.shift_over:
            return

        self.npc.update(dt)

        if self.npc.arrived:
            self.documents_button.visible = True
            self.ask_button.visible = True

        if self.npc.ready_for_decision:
            self.allow_button.visible = True
            self.deny_button.visible = True

    def _draw(self) -> None:
        screen = self.screen
        mouse_pos = pygame.mouse.get_pos()

        screen.fill((0, 0, 0))
        screen.blit(self.background, self.background_rect)

        if self.shift_over:
            screen.blit(self.counter, (0, 0))
            self._draw_end_screen(screen)
            pygame.display.flip()
            return

        self.npc.draw(screen)
        screen.blit(self.counter, (0, 0))

        self.documents_button.draw(screen, self.font, mouse_pos)
        self.ask_button.draw(screen, self.font, mouse_pos)
        self.deny_button.draw(screen, self.font, mouse_pos)
        self.allow_button.draw(screen, self.font, mouse_pos)

        self.document_panel.draw(screen, self.font, mouse_pos)
        self.question_panel.draw(screen, self.font, mouse_pos)

        pygame.display.flip()

    def _draw_end_screen(self, screen: pygame.Surface) -> None:
        if self.let_shapeshifter_pass:
            text = "GAME OVER - Um metamorfo passou pela portaria!"
            color = config.RED
        else:
            text = "FIM DE EXPEDIENTE - Nenhum metamorfo passou!"
            color = config.GREEN

        big_font = pygame.font.SysFont("consolas", 32, bold=True)
        surface = big_font.render(text, True, color)
        rect = surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(surface, rect)
