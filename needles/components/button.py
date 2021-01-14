from __future__ import annotations

from typing import Callable, Optional

import pygame

from . import Component, ColorValue, MousePos, MouseButtons, Context


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
