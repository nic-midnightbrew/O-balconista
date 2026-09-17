from pathlib import Path

import pygame

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"

COUNTER_PATH = ASSETS_DIR / "Counter.png"
BACKGROUND_PATH = ASSETS_DIR / "Hospital_Background.png"
NPC_PATH = ASSETS_DIR / "NPC.png"
ID_CARD_PATH = ASSETS_DIR / "ID.png"

FPS = 60

WINDOW_HOLE = pygame.Rect(321, 0, 928, 594)
BACKGROUND_SCALE = 1  # tamanho da imagem de fundo

BUTTON_W, BUTTON_H = 220, 44
BUTTON_GAP = 450  # espaco entre botoes
BUTTON_CENTER_X = 785  # eixo dos botoes juntos em x
BUTTON_Y = 540  # eixo dos botoes juntos em y

DOCUMENTS_BUTTON_W, DOCUMENTS_BUTTON_H = 240, 46
DOCUMENTS_BUTTON_CENTER = (785, 815)

ASK_BUTTON_W, ASK_BUTTON_H = 200, 44
ASK_BUTTON_CENTER = (1080, 250)

NPC_ENTRY_DURATION = 1.6  # tempo animacao do NPC entrando
DECISION_DELAY = 5.0  # tempo pra liberar os botoes de decisao

TEXT_LIGHT = (222, 228, 228)
GREEN = (86, 232, 168)
RED = (255, 90, 90)
BLUE = (120, 190, 255)
PANEL_BG = (18, 16, 14)
PANEL_BORDER = (150, 140, 120)
