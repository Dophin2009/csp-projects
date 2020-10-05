import random
from typing import List
from typing import Tuple

import graphics
from graphics import Circle
from graphics import GraphWin
from graphics import Point
from graphics import Polygon
from graphics import Rectangle


def main():
    win = GraphWin("Fall Drawing", 600, 600, autoflush=False)

    draw_background(win)
    sun = draw_sun(win)
    draw_forest(win)

    end = False
    while not end:
        key = win.checkKey()
        if key == "q":
            end = True
            win.close()
        update(win, sun)
        graphics.update(30)


def update(win: GraphWin, sun: Circle):
    if sun.getP1().x - sun.getRadius() > win.width:
        sun.move(-win.width - 2 * sun.getRadius() - 20, 0)
    sun.move(1, 0)


def draw_sun(win: GraphWin) -> Circle:
    sun = Circle(Point(-40, 40), 30)
    fill_outline(sun, color(233, 189, 21))
    sun.draw(win)
    return sun


def draw_tree(win: GraphWin, top_x: float, top_y: float, b_width: float,
              b_height: float, t_width: float, t_height: float, b_color: str,
              t_color: str) -> Tuple[Polygon, Rectangle]:
    body_by = top_y + b_height

    body = triangle(top_x, top_y, top_x - b_width / 2,
                    body_by, top_x + b_width / 2, body_by)
    fill_outline(body, b_color)
    body.draw(win)

    trunk = rectangle(top_x - t_width / 2, body_by, top_x +
                      t_width / 2, body_by + t_height)
    fill_outline(trunk, t_color)
    trunk.draw(win)

    return (body, trunk)


def draw_background(win: GraphWin) -> Tuple[Rectangle, Rectangle]:
    sky_color = color(69, 183, 211)
    sky = rectangle(0, 0, win.width, win.height)
    fill_outline(sky, sky_color)
    sky.draw(win)

    ground_color = color(112, 92, 80)
    ground = rectangle(0, 90, win.width, win.height)
    fill_outline(ground, ground_color)
    ground.draw(win)

    return (sky, ground)


def draw_forest(win: GraphWin):
    for i in range(tree_count):
        top_x = (win.width + 10) * random.random() - 5  # nosec
        top_y = i * (win.height - 40) / tree_count + 40
        body_color = rand_tree_body_color()

        draw_tree(win, top_x, top_y, 30, 50, 10, 25,
                  body_color, rand_tree_trunk_color())

    for j in range(15000):
        draw_fuzz(win, random.random() * win.width,  # nosec
                  random.random() * (top_y - 60) + 60, 0.5,
                  rand_tree_body_color())


def draw_fuzz(win: GraphWin, x: float, y: float, size: float, color: str):
    drop = Circle(Point(x, y), size)
    fill_outline(drop, color)
    drop.draw(win)


def rand_tree_body_color() -> str:
    idx = random.randint(0, len(tree_body_colors) - 1)  # nosec
    return tree_body_colors[idx]


def rand_tree_trunk_color() -> str:
    idx = random.randint(0, len(tree_trunk_colors) - 1)  # nosec
    return tree_trunk_colors[idx]


def rectangle(tx: float, ty: float, bx: float, by: float) -> Rectangle:
    return Rectangle(Point(tx, ty), Point(bx, by))


def triangle(x1: float, y1: float, x2: float,
             y2: float, x3: float, y3: float) -> Polygon:
    return polygon((x1, y1), (x2, y2), (x3, y3))


def polygon(*points: Tuple[float, float]) -> Polygon:
    return Polygon([Point(x, y) for x, y in points])


def color(r: int, g: int, b: int) -> str:
    return graphics.color_rgb(r, g, b)


def fill_outline(w, color: str):
    w.setFill(color)
    w.setOutline(color)


def __tree_body_colors() -> List[str]:
    tuples = [(217, 141, 136),
              (235, 184, 145),
              (238, 215, 168),
              (225, 196, 154),
              (212, 91, 18),
              (243, 188, 46)]
    return [color(r, g, b) for r, g, b in tuples]


def __tree_trunk_colors() -> List[str]:
    tuples = [(96, 60, 20), (95, 84, 38), (98, 79, 44), (141, 104, 21)]
    return [color(r, g, b) for r, g, b in tuples]


tree_count = 1500
tree_body_colors = __tree_body_colors()
tree_trunk_colors = __tree_trunk_colors()

if __name__ == '__main__':
    main()
