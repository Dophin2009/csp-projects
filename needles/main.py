import typing

import pygame
from state import State, Toss

from components import Component, ComponentBoxes, Container, Window
from components.button import Button
from components.list import List
from components.list import Orientation as ListOrientation
from components.properties import (Dimensions, FillMode, Margins, OverflowMode,
                                   Padding)
from components.rect import Rect
from components.text import Text

WIDTH = 800
HEIGHT = 600

BOARD_WIDTH = int(0.7 * WIDTH)
BOARD_HEIGHT = int(0.8 * HEIGHT)


class Control:
    def __init__(self, w: int, h: int, g: int, r: int):
        self.tossing = False
        self.state = State(w, h, g, r)

    def before_draw(self, _: Window) -> None:
        if self.tossing:
            self.state.toss()

    def start(self) -> None:
        self.tossing = True

    def pause(self) -> None:
        self.tossing = False

    def clear(self) -> None:
        self.tossing = False
        self.state.clear()


class Floorboards(Component):
    def __init__(self, id: str, lines: typing.List[int],
                 cross: typing.List[Toss], no_cross: typing.List[Toss]):
        self._id = id
        self.lines = lines
        self.cross = cross
        self.no_cross = no_cross

        self.rect = Rect("floorboard", FillMode.Fill(),
                         "brown", padding=Padding.uniform(10))

    def id(self) -> str:
        return self._id

    def type(self) -> str:
        return 'Floorboards'

    def draw(self, ctx: Container) -> ComponentBoxes:
        boxes = self.rect.draw(ctx)

        dx, dy = boxes.active.x, boxes.active.y
        y_bottom = boxes.active.bottom_y()
        for x in self.lines:
            pygame.draw.line(ctx.screen, 'black',
                             (x + dx, dy), (x + dx, y_bottom))

        for toss in self.cross:
            pygame.draw.line(ctx.screen, 'blue',
                             (toss[0][0] + dx, toss[0][1] + dy),
                             (toss[1][0] + dx, toss[1][1] + dy))

        for toss in self.no_cross:
            pygame.draw.line(ctx.screen, 'black',
                             (toss[0][0] + dx, toss[0][1] + dy),
                             (toss[1][0] + dx, toss[1][1] + dy))

        return boxes


def window() -> Window:
    pygame.font.init()
    font = pygame.font.SysFont(None, 24)

    r = int(BOARD_WIDTH / 6)
    control = Control(BOARD_WIDTH, BOARD_HEIGHT, r, r)

    start = Button("start-button",
                   FillMode.Fill(),
                   "green", "green",
                   padding=Padding.uniform(15),
                   child=Text('start-button-text', 'START', font,
                              FillMode.Fill(), 'black'),
                   on_click_action=lambda _: control.start())
    pause = Button("pause-button",
                   FillMode.Fill(),
                   "yellow", "yellow",
                   padding=Padding.uniform(15),
                   child=Text('pause-button-text', 'PAUSE', font,
                              FillMode.Fill(), 'black'),
                   on_click_action=lambda _: control.pause())
    clear = Button("clear-button",
                   FillMode.Fill(),
                   "red", "red",
                   padding=Padding.uniform(15),
                   child=Text('clear-button-text', 'CLEAR', font,
                              FillMode.Fill(), 'black'),
                   on_click_action=lambda _: control.clear())

    buttons = List("buttons", ListOrientation.HORIZONTAL,
                   FillMode.Fill(),
                   overflow=OverflowMode.Ignore(),
                   margins=Margins.uniform(0.01),
                   children=[(start, int(BOARD_WIDTH / 3)),
                             (pause, int(BOARD_WIDTH / 3)),
                             (clear, int(BOARD_WIDTH / 3))])

    floorboard = Floorboards('floorboards', control.state.cross_lines(),
                             control.state.cross, control.state.no_cross)

    left_panel = List("left", ListOrientation.VERTICAL,
                      FillMode.Fill(),
                      children=[(floorboard, BOARD_HEIGHT),
                                (buttons, HEIGHT - BOARD_HEIGHT)])

    info_panel = Rect("info", FillMode.Fill(), "lightgrey",
                      overflow=OverflowMode.Restrict())

    wrapper = List("wrapper", ListOrientation.HORIZONTAL,
                   FillMode.Fill(),
                   overflow=OverflowMode.Restrict(),
                   children=[(left_panel, BOARD_WIDTH),
                             (info_panel, WIDTH - BOARD_WIDTH)])

    w = Window('Needle Simulation', Dimensions(WIDTH, HEIGHT),
               tick_speed=20,
               child=wrapper,
               before_draw=lambda w: control.before_draw(w))
    return w


def main():
    w = window()
    w.render()


if __name__ == '__main__':
    main()
