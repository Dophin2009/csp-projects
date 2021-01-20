from components import Window
from components.button import Button
from components.list import List
from components.list import Orientation as ListOrientation
from components.properties import (Dimensions, FillMode, Margins, OverflowMode,
                                   Padding)
from components.rect import Rect


def window() -> Window:
    button1 = Button("button",
                     #  FillMode.Dimensions(Dimensions(100, 40)),
                     FillMode.Fill(),
                     "red", "blue",
                     margins=Margins.uniform(10),
                     on_click_action=lambda _: print("clicked!"))
    button2 = Button("button",
                     FillMode.Dimensions(Dimensions(100, 40)),
                     "green", "yellow",
                     margins=Margins.uniform(10),
                     on_click_action=lambda _: print("clicked!"))
    button3 = Button("button",
                     FillMode.Dimensions(Dimensions(100, 80)),
                     "white", "brown",
                     margins=Margins.uniform(10),
                     on_click_action=lambda _: print("clicked!"))
    button4 = Button("button",
                     FillMode.Dimensions(Dimensions(50, 40)),
                     "white", "brown",
                     margins=Margins.uniform(10),
                     on_click_action=lambda _: print("clicked!"))
    wrapper = List("list", ListOrientation.VERTICAL,
                   FillMode.Fill(),
                   children=[(button1, 200), (button2, 100),
                             (button3, 50), (button4, 500), (button1, 50)],
                   padding=Padding.uniform(10),
                   margins=Margins.uniform(50))

    w = Window('Needle Simulation', Dimensions(600, 600), child=wrapper)
    return w


def main():
    w = window()
    w.render()


if __name__ == '__main__':
    main()
