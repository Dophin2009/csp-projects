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


class Control:
    def __init__(self, w: int, h: int, r: int):
        self.tossing = False
        self.state = State(w, h, r)

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
    def __init__(self, id: str, tosses: typing.List[Toss]):
        self._id = id
        self.tosses = tosses

        self.rect = Rect("floorboard", FillMode.Fill(),
                         "brown", padding=Padding.uniform(10))

    def id(self) -> str:
        return self._id

    def type(self) -> str:
        return 'Floorboards'

    def draw(self, ctx: Container) -> ComponentBoxes:
        boxes = self.rect.draw(ctx)

        for toss in self.tosses:
            dx, dy = boxes.active.x, boxes.active.y
            pygame.draw.line(ctx.screen, 'black',
                             (toss[0][0] + dx, toss[0][1] + dy),
                             (toss[1][0] + dx, toss[1][1] + dy))

        return boxes


def window() -> Window:
    pygame.font.init()
    font = pygame.font.SysFont(None, 24)

    control = Control(300, 400, 50)

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
                   children=[(start, 0.235 * WIDTH),
                             (pause, 0.235 * WIDTH),
                             (clear, 0.235 * WIDTH)])

    floorboard = Floorboards('floorboards', control.state.tosses)

    left_panel = List("left", ListOrientation.VERTICAL,
                      FillMode.Fill(),
                      children=[(floorboard, 0.8 * HEIGHT),
                                (buttons, 0.2 * HEIGHT)])

    info_panel = Rect("info", FillMode.Fill(), "lightgrey",
                      overflow=OverflowMode.Restrict())

    wrapper = List("wrapper", ListOrientation.HORIZONTAL,
                   FillMode.Fill(),
                   overflow=OverflowMode.Restrict(),
                   children=[(left_panel, 0.7 * WIDTH),
                             (info_panel, 0.3 * WIDTH)])

    w = Window('Needle Simulation', Dimensions(WIDTH, HEIGHT),
               tick_speed=5,
               child=wrapper, before_draw=lambda w: control.before_draw(w))
    return w


def main():
    w = window()
    w.render()


if __name__ == '__main__':
    main()
