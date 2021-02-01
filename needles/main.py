import math
import typing

import pygame
from pygame.font import Font

from components import Component, ComponentBoxes, Container, Window
from components.button import Button
from components.list import List
from components.list import Orientation as ListOrientation
from components.properties import (ColorValue, Dimensions, FillMode, Margins,
                                   OverflowMode, Padding)
from components.rect import Rect
from components.text import Text
from state import State, Toss

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

        def draw_toss(toss: Toss, color: ColorValue):
            pygame.draw.line(ctx.screen, color,
                             (toss[0][0] + dx, toss[0][1] + dy),
                             (toss[1][0] + dx, toss[1][1] + dy))

        for x in self.lines:
            pygame.draw.line(ctx.screen, 'black',
                             (x + dx, dy), (x + dx, y_bottom))

        for toss in self.cross:
            draw_toss(toss, 'blue')

        for toss in self.no_cross:
            draw_toss(toss, 'black')

        return boxes


class InfoPanel(Component):
    def __init__(self, id: str, state: State, font: Font):
        self._id = id
        self.state = state
        self.font = font

        self.rect = Rect("info", FillMode.Fill(), "lightgrey",
                         overflow=OverflowMode.Restrict())

    def id(self) -> str:
        return self._id

    def type(self) -> str:
        return 'InfoPanel'

    def draw(self, ctx: Container) -> ComponentBoxes:
        boxes = self.rect.draw(ctx)

        num_toss = self.state.num_tosses()
        num_cross = self.state.num_cross()

        if num_toss != 0:
            percent_cross = '{:.4f}'.format(num_cross / num_toss * 100)
        else:
            percent_cross = '--'
        theoretical_percent_cross = 2 * self.state.r / \
            (self.state.g * math.pi) * 100

        pi_estimate = self.state.pi_estimate()
        if pi_estimate is None:
            pi_estimate = '--'
        else:
            pi_estimate = '{:.4f}'.format(pi_estimate)

        new_ctx = Container(ctx.screen, ctx.rg, boxes.active,
                            padding=Padding.uniform(10))

        num_toss_text = Text("num-toss-text",
                             "Tosses: {}".format(num_toss), self.font,
                             fill_mode=FillMode.Fill(), color='black')
        num_cross_text = Text("num-cross-text",
                              "Crosses: {}".format(num_cross), self.font,
                              fill_mode=FillMode.Fill(),
                              margins=Margins(0, 0, 0, 10),
                              color='black')
        percent_cross_text = Text("percent-cross-text",
                                  "% Crosses: {}".format(percent_cross),
                                  self.font,
                                  fill_mode=FillMode.Fill(), color='black')
        theoretical_cross_text = Text("theoretical-cross-text",
                                      "Theoretical %: {:.4f}".format(
                                          theoretical_percent_cross),
                                      self.font,
                                      margins=Margins(0, 0, 0, 10),
                                      fill_mode=FillMode.Fill(), color='black')

        pi_estimate_text = Text("pi-estimate-text",
                                "π estimation: {}".format(pi_estimate),
                                self.font,
                                fill_mode=FillMode.Fill(), color='black')
        pi_actual_text = Text("pi-actual-text",
                              "π: {:.4f}".format(math.pi),
                              self.font,
                              fill_mode=FillMode.Fill(),
                              color='black')

        description_text = Text("description-text",
                                "Press START to start drop",
                                self.font,
                                fill_mode=FillMode.Fill(),
                                margins=Margins(0, 0, 0, 20),
                                color='black')

        stats_list = List("stat-text-list", ListOrientation.VERTICAL,
                          FillMode.Fill(),
                          children=[
                              (description_text, 40),
                              (num_toss_text, 20),
                              (num_cross_text, 30),
                              (percent_cross_text, 20),
                              (theoretical_cross_text, 30),
                              (pi_estimate_text, 20),
                              (pi_actual_text, 20)
                          ])

        ctx.rg.register_child(self, stats_list, True)
        list_boxes = stats_list.draw(new_ctx)
        ctx.rg.set_box(stats_list.id(), list_boxes, False)

        return boxes


def window() -> Window:
    pygame.font.init()
    font = pygame.font.SysFont(None, 24)

    r = int(BOARD_WIDTH / 6)
    control = Control(BOARD_WIDTH, BOARD_HEIGHT, 6, r)

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

    info_panel = InfoPanel("info", control.state, font)

    wrapper = List("wrapper", ListOrientation.HORIZONTAL,
                   FillMode.Fill(),
                   overflow=OverflowMode.Restrict(),
                   children=[(left_panel, BOARD_WIDTH),
                             (info_panel, WIDTH - BOARD_WIDTH)])

    w = Window('Needle Simulation', Dimensions(WIDTH, HEIGHT),
               tick_speed=100000,
               child=wrapper,
               before_draw=lambda w: control.before_draw(w))
    return w


def main():
    w = window()
    w.render()


if __name__ == '__main__':
    main()
