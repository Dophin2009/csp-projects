from pygame.color import Color

from components import Window
from components.button import Button


def main():
    button = Button(50, 50, Color('gray'), Color('black'),
                    px=0, py=0,
                    on_click_action=lambda event: print("ajwlfj"))
    window = Window(600, 600, child=button)
    window.render()


if __name__ == '__main__':
    main()
