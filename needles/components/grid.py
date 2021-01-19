from __future__ import annotations

from typing import List, Optional

from . import Component, Context


class Grid(Component):
    def __init__(self, w: int, h: int, c: int, r: int,
                 children: List[GridChild]):
        self.w = w
        self.h = h

        self.c = c
        self.r = r

        for child in children:
            if child.left >= c:
                msg = 'GridChild left pos {} is out of bounds'.format(
                    child.left)
                raise Exception(msg)
            elif child.top >= r:
                msg = 'GridChild top pos {} is out of bounds'.format(
                    child.top)
                raise Exception(msg)
            elif child.left + child.cols > self.c:
                msg = 'GridChild width {} is too large'.format(
                    child.cols)
                raise Exception(msg)
            elif child.top + child.rows > self.r:
                msg = 'GridChild height {} is too large'.format(
                    child.cols)
                raise Exception(msg)

    def type(self) -> str:
        return 'Grid'

    def draw(self, ctx: Context) -> None:
        for child in self.children:
            new_ctx = ctx.shifted()


class GridChild:
    def __init__(self, left: int, top: int, cols: int, rows: int,
                 px: int = 0, py: int = 0,
                 child: Optional[Component] = None):
        if left < 0:
            msg = 'GridChild left pos {} is out of bounds'.format(left)
            raise Exception(msg)
        elif top < 0:
            msg = 'GridChild top pos {} is out of bounds'.format(top)
            raise Exception(msg)

        self.left = left
        self.top = top

        self.cols = cols
        self.rows = rows

        self.child = child
