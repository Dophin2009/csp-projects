from __future__ import annotations

from typing import Callable, Optional

import pygame
from pygame.event import Event

from . import Component, Container
from .properties import ColorValue, FillMode, Margins, OverflowMode, Padding
from .rect import Rect


class Button(Rect):

    def __init__(self,  fill_mode: FillMode,
                 color: ColorValue, accent_color: Optional[ColorValue] = None,
                 padding=Padding.zero(), margins=Margins.zero(),
                 overflow=OverflowMode.Ignore(),
                 child: Optional[Component] = None,
                 on_click_action: Optional[Callable[[Event], None]] = None):
        super(Button, self).__init__(fill_mode, color,
                                     padding, margins, overflow, child)
        if accent_color is not None:
            self.accent_color = accent_color
        else:
            self.accent_color = self.color

        if on_click_action is not None:
            self.on_click_action = on_click_action
        else:
            def noop(event: Event) -> None:
                pass
            self.on_click_action = noop

        self.child = child

    def type(self) -> str:
        return 'Button'

    def draw(self, ctx: Container):
        box = self.determine_box(ctx)
        screen = ctx.screen

        # Check if mouse position is within absolute position of button
        mouse_pos = pygame.mouse.get_pos()

        if box.contains(mouse_pos):
            color = self.accent_color
            # Draw accented color button
        else:
            # Draw normal color button
            color = self.color

        # Draw box
        pygame.draw.rect(screen, color, box.as_tuple())

        # Compute new ctx and draw children
        #  if self.child is not None:
        #  new_ctx = ctx.shifted(self.px, self.py)
        #  self.child.draw(new_ctx)

    def on_click(self, event: Event) -> None:
        self.on_click_action(event)
