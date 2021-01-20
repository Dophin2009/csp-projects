from __future__ import annotations

import typing
from enum import Enum, auto
from typing import Tuple

from pygame.event import Event

from . import Component, ComponentBoxes, Container
from .properties import Box, FillMode, Margins, OverflowMode, Padding
from .rect import Rect


class Orientation(Enum):
    HORIZONTAL = auto()
    VERTICAL = auto()


class List(Rect):
    def __init__(self, id: str,
                 orientation: Orientation,
                 fill_mode: FillMode,
                 # List of components and the widths/heights of containers to
                 # use
                 children: typing.List[Tuple[Component, int]],
                 padding=Padding.zero(),
                 margins=Margins.zero(),
                 overflow=OverflowMode.Ignore()):
        self._id = id
        self.orientation = orientation
        self.fill_mode = fill_mode
        self.children = children
        self.padding = padding
        self.margins = margins
        self.overflow = overflow

    def id(self) -> str:
        return self._id

    def type(self) -> str:
        return 'List'

    def draw(self, ctx: Container) -> ComponentBoxes:
        bounds = self.determine_box(ctx)

        break_on_overflow = False
        if self.overflow.is_restrict():
            # Restrict overflow: when later drawing children, break on
            # overflow.
            break_on_overflow = True
        elif self.overflow.is_ignore():
            # Ignore overflow: when later drawing children, continue on
            # overflow.
            pass
        else:
            pass

        # Monkey code
        new_ctx = ctx
        new_padding = self.padding
        child_full_box = Box(0, 0, 0, 0)
        acc = 0
        box = bounds
        children_count = len(self.children)
        for i, (child, size) in enumerate(self.children):
            # Reduce container size
            new_box = None
            if self.orientation == Orientation.HORIZONTAL:
                # Check overflow and shrink or break
                offset_x = child_full_box.w
                if break_on_overflow:
                    acc += size
                    if acc > bounds.w:
                        size -= bounds.w - acc
                        if size <= 0:
                            break

                # Shift left position
                new_box = Box(box.x + offset_x, box.y, size, box.h)

                if i == 0:
                    # No right padding on first item
                    new_padding = Padding(self.padding.left, self.padding.top,
                                          0, self.padding.bottom)
                elif i == 1:
                    # No right or left padding on middle items
                    new_padding = Padding(0, self.padding.top,
                                          0, self.padding.bottom)
                elif i == children_count - 1:
                    # No left padding for last item
                    new_padding = Padding(0, self.padding.top,
                                          self.padding.right,
                                          self.padding.bottom)
            elif self.orientation == Orientation.VERTICAL:
                # Check overflow and shrink or break
                offset_y = child_full_box.h
                if break_on_overflow:
                    acc += size
                    if acc > bounds.h:
                        size -= bounds.h - acc
                        if size <= 0:
                            break

                # Shift top position
                new_box = Box(box.x, box.y + offset_y, box.w, size)

                if i == 0:
                    # No bottom padding on first item
                    new_padding = Padding(self.padding.left, self.padding.top,
                                          self.padding.right, 0)
                elif i == 1:
                    # No top or bottom padding on middle items
                    new_padding = Padding(self.padding.left, 0,
                                          self.padding.right, 0)
                elif i == children_count - 1:
                    # No top padding for last item
                    new_padding = Padding(self.padding.left, 0,
                                          self.padding.right,
                                          self.padding.bottom)
            else:
                pass

            assert new_box is not None

            ctx.rg.register_child(self, child, True)

            box = new_box
            new_ctx = Container(ctx.screen, ctx.rg, new_box,
                                padding=new_padding,
                                overflow=self.overflow)

            child_boxes = child.draw(new_ctx)
            child_full_box = child_boxes.full

            ctx.rg.set_box(child.id(), child_boxes,
                           not bounds.encapsulates(child_boxes.active))

        return ComponentBoxes(bounds, bounds.grow(self.margins))
