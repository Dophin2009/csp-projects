from __future__ import annotations

from typing import List, Optional, Tuple, Union

from pygame.color import Color

ColorValue = Union[
    Color, str, Tuple[int, int, int], List[int], int, Tuple[int, int, int, int]
]
MousePos = Tuple[int, int]
MouseButtons = Union[Tuple[bool, bool, bool],
                     Tuple[bool, bool, bool, bool, bool]]


Point = Tuple[int, int]


class Dimensions:
    def __init__(self, w: int, h: int):
        self.w = w
        self.h = h


class Box:
    def __init__(self, x: int, y: int, w: int, h: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def right_x(self) -> int:
        return self.x + self.w

    def bottom_y(self) -> int:
        return self.y + self.h

    def points(self) -> Tuple[Point, Point, Point, Point]:
        """
        Returns the four verticies of the box in the following order: Top left,
        top right, bottom left, bottom right.
        """
        fx = self.right_x()
        fy = self.bottom_y()
        return ((self.x, self.y), (fx, self.y), (fx, fy), (self.x, fy))

    def contains(self, p: Point) -> bool:
        return self.right_x() > p[0] > self.x \
            and self.bottom_y() > p[1] > self.y

    def encapsulates(self, other: Box) -> bool:
        return self.x < other.x and self.right_x() > other.right_x() \
            and self.y < other.y and self.bottom_y() > other.bottom_y()

    def as_tuple(self) -> Tuple[int, int, int, int]:
        return (self.x, self.y, self.w, self.h)

    def shrink(self, s: Sides) -> Box:
        w = self.w - s.left - s.right
        h = self.h - s.top - s.bottom
        return Box(self.x + s.left, self.y + s.top, w, h)

    def grow(self, s: Sides) -> Box:
        w = self.w + s.left + s.right
        h = self.h + s.top + s.bottom
        return Box(self.x - s.left, self.y - s.top, w, h)

    def __repr__(self) -> str:
        return f'Box({self.x}, {self.y}, {self.w}, {self.h})'


class Sides:
    def __init__(self, left: int = 0, top: int = 0,
                 right: int = 0, bottom: int = 0):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    @classmethod
    def uniform(cls, v: int) -> Sides:
        return cls(v, v, v, v)

    @classmethod
    def symmetric(cls, h: int, v: int) -> Sides:
        return cls(h, v, h, v)

    @staticmethod
    def zero() -> Sides:
        return Sides(0, 0, 0, 0)


class Padding(Sides):
    @staticmethod
    def zero() -> Padding:
        return Padding(0, 0, 0, 0)


class Margins(Sides):
    @staticmethod
    def zero() -> Margins:
        return Margins(0, 0, 0, 0)


class FillMode:
    # Hacky algebraic sum type
    __create_key = object()

    __Fill = 0
    __Dimensions = 1

    def __init__(self, create_key, ty: int,
                 dimensions: Optional[Dimensions] = None):
        assert(create_key == FillMode.__create_key), \
            "FillMode objects cannot be created directly"
        self._ty = ty
        self._dims = dimensions

    def inner(self) -> Optional[Dimensions]:
        if self._ty == FillMode.__Fill:
            return None
        else:
            assert self._dims is not None
            return self._dims

    def is_fill(self) -> bool:
        return self._ty == FillMode.__Fill

    def is_dimensions(self) -> bool:
        return self._ty == FillMode.__Dimensions

    @classmethod
    def Fill(cls) -> FillMode:
        return FillMode(FillMode.__create_key, FillMode.__Fill)

    @classmethod
    def Dimensions(cls, dims: Dimensions) -> FillMode:
        return FillMode(FillMode.__create_key, FillMode.__Dimensions, dims)


class OverflowMode:
    # Another hacky sum type
    __create_key = object()

    __Ignore = 0
    __Restrict = 1

    def __init__(self, create_key, ty: int):
        assert(create_key == OverflowMode.__create_key), \
            "OverflowMode objects cannot be created directly"
        self._ty = ty

    def is_ignore(self) -> bool:
        return self._ty == OverflowMode.__Ignore

    def is_restrict(self) -> bool:
        return self._ty == OverflowMode.__Restrict

    @classmethod
    def Ignore(cls) -> OverflowMode:
        return OverflowMode(OverflowMode.__create_key, OverflowMode.__Ignore)

    @classmethod
    def Restrict(cls) -> OverflowMode:
        return OverflowMode(OverflowMode.__create_key, OverflowMode.__Restrict)
