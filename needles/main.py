from pygame.color import Color

from components import Window
from components.button import Button
from components.list import List
from components.list import Orientation as ListOrientation
from components.properties import (Dimensions, FillMode, Margins, OverflowMode,
                                   Padding)
from components.rect import Rect

WIDTH = 600
HEIGHT = 600


def window() -> Window:
    start = Button("start-button",
                   FillMode.Fill(),
                   "green", "green",
                   margins=Margins(0.02 * WIDTH, 0.02 * WIDTH,
                                   0.04 * WIDTH, 0.02 * WIDTH))
    pause = Button("pause-button",
                   FillMode.Fill(),
                   "yellow", "yellow",
                   margins=Margins.uniform(0.02 * WIDTH))
    clear = Button("clear-button",
                   FillMode.Fill(),
                   "red", "red",
                   margins=Margins.uniform(0.02 * WIDTH))
    buttons = List("buttons", ListOrientation.HORIZONTAL,
                   FillMode.Fill(), padding=Padding.uniform(10),
                   overflow=OverflowMode.Ignore(),
                   children=[(start, 0.22 * WIDTH),
                             (pause, 0.19 * WIDTH),
                             (clear, 0.2 * WIDTH)])

    floorboard = Rect("floorboard", FillMode.Fill(),
                      "brown", padding=Padding.uniform(10))

    left_panel = List("left", ListOrientation.VERTICAL,
                      FillMode.Fill(),
                      children=[(floorboard, 0.7 * HEIGHT),
                                (buttons, 0.2 * HEIGHT)])

    info_panel = Rect("info", FillMode.Fill(), "lightgrey",
                      padding=Padding.uniform(0.05 * WIDTH),
                      margins=Margins(0.075 * WIDTH, 0, 0, 0),
                      overflow=OverflowMode.Restrict())

    wrapper = List("wrapper", ListOrientation.HORIZONTAL,
                   FillMode.Fill(),
                   padding=Padding.uniform(0.05 * WIDTH),
                   overflow=OverflowMode.Restrict(),
                   children=[(left_panel, 0.65 * WIDTH),
                             (info_panel, 0.35 * WIDTH)])

    w = Window('Needle Simulation', Dimensions(WIDTH, HEIGHT), child=wrapper)
    return w


def main():
    w = window()
    w.render()


if __name__ == '__main__':
    main()
