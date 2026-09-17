from dataclasses import dataclass, field
from typing import List, Optional, Tuple

import pygame

from . import config


def _ease_out_cubic(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


@dataclass
class NPCProfile:

    name: str
    questions: List[str] = field(default_factory=list)
    is_human: bool = True


QUESTIONS = ["Motivo da entrada", "Documentos", "Aparência"]

NPCS = [
    NPCProfile(name="Visitante 1", questions=QUESTIONS, is_human=True),
    NPCProfile(name="Visitante 2", questions=QUESTIONS, is_human=False),
    NPCProfile(name="Visitante 3", questions=QUESTIONS, is_human=True),
    NPCProfile(name="Visitante 4", questions=QUESTIONS, is_human=False),
    NPCProfile(name="Visitante 5", questions=QUESTIONS, is_human=True),
]


class NPCActor:

    START_SCALE = 0.35
    END_SCALE = 1.0
    END_HEIGHT = 560

    def __init__(self, profile: NPCProfile):
        self.profile = profile
        self.sprite = pygame.image.load(str(config.NPC_PATH)).convert_alpha()
        native_w, native_h = self.sprite.get_size()
        self._aspect = native_w / native_h

        hole = config.WINDOW_HOLE
        self._center_x = hole.centerx
        self._start_bottom = hole.top + hole.height * 0.55
        self._end_bottom = float(hole.bottom)

        self._elapsed = 0.0
        self.arrived = False
        self.time_since_arrival = 0.0

        self._cached_size: Optional[Tuple[int, int]] = None
        self._cached_sprite: Optional[pygame.Surface] = None

    def update(self, dt: float) -> None:
        if not self.arrived:
            self._elapsed += dt
            if self._elapsed >= config.NPC_ENTRY_DURATION:
                self._elapsed = config.NPC_ENTRY_DURATION
                self.arrived = True
        else:
            self.time_since_arrival += dt

    @property
    def ready_for_decision(self) -> bool:
        return self.arrived and self.time_since_arrival >= config.DECISION_DELAY

    def reset(self, profile: NPCProfile) -> None:
        self.profile = profile
        self._elapsed = 0.0
        self.arrived = False
        self.time_since_arrival = 0.0

    def _scaled_sprite(self, width: int, height: int) -> pygame.Surface:
        if self._cached_size != (width, height):
            self._cached_sprite = pygame.transform.smoothscale(self.sprite, (width, height))
            self._cached_size = (width, height)
        return self._cached_sprite

    def draw(self, screen: pygame.Surface) -> None:
        t = _ease_out_cubic(self._elapsed / config.NPC_ENTRY_DURATION)

        scale = self.START_SCALE + (self.END_SCALE - self.START_SCALE) * t
        height = max(1, int(self.END_HEIGHT * scale))
        width = max(1, int(height * self._aspect))
        sprite = self._scaled_sprite(width, height)

        bottom_y = self._start_bottom + (self._end_bottom - self._start_bottom) * t
        rect = sprite.get_rect(midbottom=(self._center_x, bottom_y))
        screen.blit(sprite, rect)
