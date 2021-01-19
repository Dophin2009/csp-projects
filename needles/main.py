from pygame.color import Color

from components import Window
from components.button import Button
from components.properties import Dimensions, FillMode, Margins, OverflowMode


def window() -> Window:
    button = Button(
        FillMode.Dimensions(Dimensions(100, 40)),
        "red", "blue",
        margins=Margins.uniform(10),
        on_click_action=lambda _: print("clicked!")
    )

    w = Window('Needle Simulation', Dimensions(600, 600), child=button)
    return w


def main():
    w = window()
    w.render()


if __name__ == '__main__':
    main()
    main()
