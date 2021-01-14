from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Union

from pygame.color import Color
from pygame.event import Event
from pygame.surface import Surface
from pygame.time import Clock
import pygame

ColorValue = Union[
    Color, str, Tuple[int, int, int], List[int], int, Tuple[int, int, int, int]
]
MousePos = Tuple[int, int]
MouseButtons = Union[Tuple[bool, bool, bool],
                     Tuple[bool, bool, bool, bool, bool]]


class Context:
    def __init__(self, screen: Surface, delta_x: int, delta_y: int):
        self.screen = screen
        self._delta_x = delta_x
        self._delta_y = delta_y

    @property
    def x(self) -> int:
        return self._delta_x

    @property
    def y(self) -> int:
        return self._delta_y

    def shifted(self, x: int, y: int) -> Context:
        return Context(self.screen, self.x + x, self.y + y)


class Component(ABC):
    child: Optional[Component]

    @abstractmethod
    def draw(self, ctx: Context):
        """
        Implementations should draw the component on the given screen and at
        the given delta. The screen and modified delta should be passed to any
        nested components.
        """
        pass


class Window:
    def __init__(self, w: int, h: int, px: int = 0, py: int = 0,
                 child: Optional[Component] = None):
        self.w = w
        self.h = h
        self.px = px
        self.py = py

        self.screen = pygame.display.set_mode([600, 600])
        self.clock = Clock()

        self.child = child

    def render(self):
        ctx = Context(self.screen, self.px, self.py)

        done = False
        while not done:
            self.screen.fill(Color('lightskyblue'))

            for event in pygame.event.get():
                if self._check_quit(event):
                    done = True

            if self.child is not None:
                self.child.draw(ctx)

            pygame.display.update()
            self.clock.tick(30)

    def _check_quit(self, event: Event) -> bool:
        return event.type == pygame.QUIT or \
            (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)
