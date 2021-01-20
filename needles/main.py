from components import Window
from components.button import Button
from components.list import List
from components.list import Orientation as ListOrientation
from components.properties import (Dimensions, FillMode, Margins, OverflowMode,
                                   Padding)
from components.rect import Rect


def window() -> Window:
    button1 = Button("button1",
                     #  FillMode.Dimensions(Dimensions(100, 40)),
                     FillMode.Fill(),
                     "red", "blue",
                     margins=Margins.uniform(10),
                     on_click_action=lambda _: print("button1"))
    button2 = Button("button2",
                     FillMode.Dimensions(Dimensions(100, 40)),
                     "green", "yellow",
                     margins=Margins.uniform(10),
                     on_click_action=lambda _: print("button2"))
    button3 = Button("button3",
                     FillMode.Dimensions(Dimensions(100, 80)),
                     "white", "brown",
                     margins=Margins.uniform(10),
                     on_click_action=lambda _: print("button3"))
    button4 = Button("button4",
                     FillMode.Dimensions(Dimensions(50, 40)),
                     "white", "brown",
                     margins=Margins.uniform(10),
                     on_click_action=lambda _: print("button4"))
    wrapper = List("list", ListOrientation.VERTICAL,
                   FillMode.Fill(),
                   children=[(button1, 200), (button2, 100),
                             (button3, 50), (button4, 500)],
                   padding=Padding.uniform(10),
                   margins=Margins.uniform(50))

    w = Window('Needle Simulation', Dimensions(600, 600), child=wrapper)
    return w


def main():
    w = window()
    w.render()


if __name__ == '__main__':
    main()
