from __future__ import annotations

from typing import List, Tuple, Union

from pygame.color import Color
from pygame.font import Font

from . import Component, ComponentBoxes, Container
from .properties import FillMode, Margins, OverflowMode, Padding
from .rect import Rect

ColorValue = Union[
    Color, Tuple[int, int, int], List[int], int, Tuple[int, int, int, int]
]


class Text(Rect):
    def __init__(self, id: str, text: str, font: Font,
                 fill_mode: FillMode,
                 color: ColorValue,
                 padding=Padding.zero(),
                 margins=Margins.zero(),
                 overflow=OverflowMode.Ignore()):
        super(Text, self).__init__(id, fill_mode, color,
                                   padding, margins, overflow, child=None)
        self.text = text
        self.font = font

        self.text_color = color

    def type(self) -> str:
        return 'Text'

    def draw(self, ctx: Container) -> ComponentBoxes:
        box = self.determine_box(ctx)
        screen = ctx.screen

        img = self.font.render(self.text, True, self.text_color)

        screen.blit(img, (box.x, box.y))
        return ComponentBoxes(box, box.grow(self.margins))
