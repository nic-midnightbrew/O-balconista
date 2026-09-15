import sys
from pathlib import Path

import pygame

BASE_DIR = Path(__file__).resolve().parent
COUNTER_PATH = BASE_DIR / "Counter.png"
BACKGROUND_PATH = BASE_DIR / "Hospital_Background.png"

FPS = 60

WINDOW_HOLE = pygame.Rect(321, 0, 928, 594)
BACKGROUND_SCALE = 1 # tamanho da imagem de fundo

BUTTON_W, BUTTON_H = 220, 44
BUTTON_GAP = 450 #espaco entre bootes
BUTTON_CENTER_X = 785 # eixo dos boteoes juntos em x
BUTTON_Y = 540 # eixo dos boteoes juntos em y

TEXT_LIGHT = (222, 228, 228)
GREEN = (86, 232, 168)
RED = (255, 90, 90)


def draw_button(screen, font, rect, label, color, hovered):
    panel = pygame.Surface(rect.size, pygame.SRCALPHA)
    bg_alpha = 190 if hovered else 140
    pygame.draw.rect(panel, (10, 10, 10, bg_alpha), panel.get_rect(), border_radius=10)
    pygame.draw.rect(panel, color, panel.get_rect(), width=2, border_radius=10)
    screen.blit(panel, rect.topleft)
    text = font.render(label, True, TEXT_LIGHT)
    screen.blit(text, text.get_rect(center=rect.center))


def main():
    pygame.init()
    pygame.display.set_caption("O Balconistao")

    counter = pygame.image.load(str(COUNTER_PATH))
    background = pygame.image.load(str(BACKGROUND_PATH))
    screen = pygame.display.set_mode(counter.get_size())
    counter = counter.convert_alpha()
    background = background.convert_alpha()

    bg_size = (int(background.get_width() * BACKGROUND_SCALE),
               int(background.get_height() * BACKGROUND_SCALE))
    background = pygame.transform.smoothscale(background, bg_size)
    background_rect = background.get_rect(center=WINDOW_HOLE.center)

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 19, bold=True)

    total_w = BUTTON_W * 2 + BUTTON_GAP
    start_x = BUTTON_CENTER_X - total_w // 2

    deny_rect = pygame.Rect(start_x, BUTTON_Y, BUTTON_W, BUTTON_H)
    allow_rect = pygame.Rect(start_x + BUTTON_W + BUTTON_GAP, BUTTON_Y, BUTTON_W, BUTTON_H)

    running = True
    while running:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if allow_rect.collidepoint(mouse_pos):
                    pass
                elif deny_rect.collidepoint(mouse_pos):
                    pass

        screen.fill((0, 0, 0))
        screen.blit(background, background_rect)
        screen.blit(counter, (0, 0))

        draw_button(screen, font, deny_rect, "NÃO DEIXAR PASSAR", RED, deny_rect.collidepoint(mouse_pos))
        draw_button(screen, font, allow_rect, "DEIXAR PASSAR", GREEN, allow_rect.collidepoint(mouse_pos))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
