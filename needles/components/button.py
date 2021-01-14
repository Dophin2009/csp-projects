from __future__ import annotations

from typing import Callable, Optional

import pygame
from pygame.event import Event

from . import Component, ColorValue, Context


class Button(Component):

    def __init__(self, w: int, h: int,
                 ic: ColorValue, ac: ColorValue,
                 on_click_action: Optional[Callable[[Event], None]],
                 px: int = 0, py: int = 0,
                 child: Optional[Component] = None):
        self.w = w
        self.h = h
        self.px = px
        self.py = py

        self.ic = ic
        self.ac = ac

        if on_click_action is not None:
            self.on_click_action = on_click_action
        else:
            def noop(event: Event) -> None:
                pass
            self.on_click_action = noop

        self.child = child

    def type(self) -> str:
        return 'Button'

    def width(self) -> int:
        return self.w

    def height(self) -> int:
        return self.h

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
        else:
            print("mouse out!")
            # Draw normal color button
            pygame.draw.rect(screen, self.ic, (x, y, self.w, self.h))

        # Compute new ctx and draw children
        if self.child is not None:
            new_ctx = ctx.shifted(self.px, self.py)
            self.child.draw(new_ctx)

    def on_click(self, event: Event) -> None:
        self.on_click_action(event)
