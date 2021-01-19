from __future__ import annotations

from typing import Optional

import pygame

from . import Component, Container
from .properties import (Box, ColorValue, FillMode, Margins, OverflowMode,
                         Padding)


class Rect(Component):
    def __init__(self, fill_mode: FillMode, color: ColorValue,
                 padding=Padding.zero(), margins=Margins.zero(),
                 overflow=OverflowMode.Ignore(),
                 child: Optional[Component] = None):
        self.fill_mode = fill_mode
        self.color = color
        self.padding = padding
        self.margins = margins
        self.child = child

    def type(self) -> str:
        return 'Rect'

    def draw(self, ctx: Container) -> None:
        rect_dims = self.determine_box(ctx)
        screen = ctx.screen
        pygame.draw.rect(screen, self.color, rect_dims.as_tuple())

        #  if self.child is not None:
        #  new_ctx = ctx.shifted(self.mx + self.px, self.my + self.py)
        #  self.child.draw(new_ctx)

    def determine_box(self, ctx: Container) -> Box:
        """
        Calculate the box for when the rectangle is actually drawn in the given
        container.
        """
        if self.fill_mode.is_fill():
            # Fill mode: rectangle should take up all of container content box
            # minus margins.
            rect_dims = ctx.content_box().shrink(self.margins)
        else:
            #  elif self.fill_mode.is_dimensions():
            # Dimensions mode: rectangle should take up specified width and
            # height
            fill_dims = self.fill_mode.inner()
            assert fill_dims is not None

            x = ctx.box.x + self.margins.left
            y = ctx.box.y + self.margins.top
            w = fill_dims.w
            w_with_margin = w + self.margins.right
            h = fill_dims.h
            h_with_margin = h + self.margins.bottom

            if ctx.overflow.is_restrict():
                # Restrict mode: check if too big for container; reduce width
                # and height if necessary
                fx = x + w_with_margin
                fy = y + h_with_margin
                ctx_box_fx = ctx.box.right_x()
                ctx_box_fy = ctx.box.bottom_y()
                if fx > ctx_box_fx:
                    w -= (ctx_box_fx - (fx))
                if fy > ctx_box_fy:
                    h -= (ctx_box_fy - (fy))
            elif ctx.overflow.is_ignore():
                pass
            else:
                pass

            rect_dims = Box(x, y, w, h)

        return rect_dims
