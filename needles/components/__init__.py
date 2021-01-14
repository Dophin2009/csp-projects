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
    def type(self) -> str:
        pass

    @abstractmethod
    def draw(self, ctx: Context):
        """
        Implementations should draw the component on the given screen and at
        the given delta. The screen and modified delta should be passed to any
        nested components.
        """
        pass

    @abstractmethod
    def width(self) -> int:
        pass

    @abstractmethod
    def height(self) -> int:
        pass

    def on_click(self, event: Event) -> None:
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

        if child is not None:
            if child.width() > w - px or child.height() > h - py:
                msg = 'Window child {} is too large'.format(child.type())
                raise Exception(msg)
        self.child = child

    def render(self):
        pygame.init()
        ctx = Context(self.screen, self.px, self.py)

        exit = False
        while not exit:
            # Draw the child if it is given
            if self.child is not None:
                self.child.draw(ctx)

            # Handle events
            for event in pygame.event.get():
                if self._check_quit(event):
                    exit = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.on_click(event)

            pygame.display.update()
            self.clock.tick(30)

        pygame.quit()

    def on_click(self, event: Event) -> None:
        "Pass click event to descendants if within the active box."
        if self.child is None:
            return

        x, y = event.pos
        if self.child.width() + self.px > x > self.px \
                and self.child.height() + self.py > y > self.py:
            self.child.on_click(event)

    def in_active_box(self, x: int, y: int) -> bool:
        """
        Check that the given coordinates are within the active box, not
        including the padding.
        """
        return self.w - self.px > x > self.px \
            and self.h - self.py > y > self.py

    def _check_quit(self, event: Event) -> bool:
        """
        Check if window should stop rendering; returns true if X button clicked
        or <esc> key is pressed.
        """
        return event.type == pygame.QUIT or \
            (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)
