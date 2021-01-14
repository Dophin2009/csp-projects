from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, List, Optional, Tuple, Union

from pygame.surface import Surface
from pygame.color import Color
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
        self.delta_x = delta_x
        self.delta_y = delta_y

    def x(self, x: int) -> int:
        return self.delta_x + x

    def y(self, y: int) -> int:
        return self.delta_y + y


class Component(ABC):

    @abstractmethod
    def draw(self, ctx: Context):
        """
        Implementations should draw the component on the given screen and at
        the given delta. The screen and delta should be passed to any nested
        components.
        """
        pass


Children = Union[List[Component], Component]


class Button:

    def __init__(self, x: int, y: int, w: int, h: int,
                 ic: ColorValue, ac: ColorValue,
                 on_click: Optional[Callable[[MousePos, MouseButtons], None]],
                 children: List[Component]):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.ic = ic
        self.ac = ac

        if on_click is not None:
            self.on_click = on_click
        else:
            def noop(pos: MousePos, buttons: MouseButtons) -> None:
                pass
            self.on_click = noop

        self.children = children

    def draw(self, ctx: Context):
        screen = ctx.screen
        x = ctx.x(self.x)
        y = ctx.y(self.y)

        mouse_pos = pygame.mouse.get_pos()

        # Check if mouse position is within absolute position of button
        if x + self.w > mouse_pos[0] > x and y + self.h > mouse_pos[1] > y:
            # Draw accented color button
            pygame.draw.rect(screen, self.ac, (x, y, self.w, self.h))

            # Check for left mouse click
            mouse_buttons = pygame.mouse.get_pressed(1)
            if mouse_buttons[0] == 1:
                self.on_click(mouse_pos, mouse_buttons)
        else:
            # Draw normal color button
            pygame.draw.rect(screen, self.ic, (x, y, self.w, self.h))

        for child in self.children:
            child.draw(ctx)
