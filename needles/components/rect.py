from __future__ import annotations

from typing import Optional

import pygame

from . import Component, ComponentBoxes, Container
from .properties import (Box, ColorValue, FillMode, Margins, OverflowMode,
                         Padding)


class Rect(Component):
    def __init__(self, id: str, fill_mode: FillMode, color: ColorValue,
                 padding=Padding.zero(), margins=Margins.zero(),
                 overflow=OverflowMode.Ignore(),
                 child: Optional[Component] = None):
        self._id = id
        self.fill_mode = fill_mode
        self.color = color
        self.padding = padding
        self.margins = margins
        self.overflow = overflow
        self.child = child

    def id(self) -> str:
        return self._id

    def type(self) -> str:
        return 'Rect'

    def draw(self, ctx: Container) -> ComponentBoxes:
        box = self.determine_box(ctx)
        screen = ctx.screen
        pygame.draw.rect(screen, self.color, box.as_tuple())

        if self.child is not None:
            # Register child component
            ctx.rg.register_child(self, self.child, True)

            new_ctx = Container(ctx.screen,
                                ctx.rg,
                                box,
                                padding=self.padding,
                                overflow=self.overflow)
            child_boxes = self.child.draw(new_ctx)

            # Save bounding boxes
            ctx.rg.set_box(self.child.id(), child_boxes,
                           not box.encapsulates(child_boxes.active))

        return ComponentBoxes(box, box.grow(self.margins))

    def determine_box(self, ctx: Container) -> Box:
        """
        Calculate the box for when the rectangle is actually drawn in the given
        container.
        """
        rect_dims = None
        if self.fill_mode.is_fill():
            # Fill mode: rectangle should take up all of container content box
            # minus margins.
            rect_dims = ctx.content_box().shrink(self.margins)
        elif self.fill_mode.is_dimensions():
            # Dimensions mode: rectangle should take up specified width and
            # height
            fill_dims = self.fill_mode.inner()
            assert fill_dims is not None

            ctx_box = ctx.content_box()
            x = ctx_box.x + self.margins.left
            y = ctx_box.y + self.margins.top
            w = fill_dims.w
            w_with_margin = w + self.margins.right
            h = fill_dims.h
            h_with_margin = h + self.margins.bottom

            if ctx.overflow.is_restrict():
                # Restrict mode: check if too big for container; reduce width
                # and height if necessary
                fx = x + w_with_margin
                fy = y + h_with_margin

                ctx_box_fx = ctx_box.right_x()
                ctx_box_fy = ctx_box.bottom_y()

                if fx > ctx_box_fx:
                    w -= (ctx_box_fx - (fx))
                if fy > ctx_box_fy:
                    h -= (ctx_box_fy - (fy))
            elif ctx.overflow.is_ignore():
                pass
            else:
                pass

            rect_dims = Box(x, y, w, h)

        assert rect_dims is not None
        return rect_dims
