from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, List, Optional, Tuple, Union

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


class Button(Component):

    def __init__(self, w: int, h: int,
                 ic: ColorValue, ac: ColorValue,
                 on_click: Optional[Callable[[MousePos, MouseButtons], None]],
                 px: int = 0, py: int = 0,
                 child: Optional[Component] = None):
        self.w = w
        self.h = h
        self.px = px
        self.py = py

        self.ic = ic
        self.ac = ac

        if on_click is not None:
            self.on_click = on_click
        else:
            def noop(pos: MousePos, buttons: MouseButtons) -> None:
                pass
            self.on_click = noop

        self.child = child

    def draw(self, ctx: Context):
        screen = ctx.screen
        x = ctx.x
        y = ctx.y

        # Check if mouse position is within absolute position of button
        mouse_pos = pygame.mouse.get_pos()
        print(mouse_pos)
        if x + self.w > mouse_pos[0] > x and y + self.h > mouse_pos[1] > y:
            print("mouse in!")
            # Draw accented color button
            pygame.draw.rect(screen, self.ac, (x, y, self.w, self.h))

            # Check for left mouse click
            mouse_buttons = pygame.mouse.get_pressed(3)
            if mouse_buttons[0] == 1:
                self.on_click(mouse_pos, mouse_buttons)
        else:
            print("mouse out!")
            # Draw normal color button
            pygame.draw.rect(screen, self.ic, (x, y, self.w, self.h))

        # Compute new ctx and draw children
        if self.child is not None:
            new_ctx = ctx.shifted(self.px, self.py)
            self.child.draw(new_ctx)
