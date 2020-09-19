import random

from graphics import Circle
from graphics import color_rgb
from graphics import GraphWin
from graphics import Point
from graphics import update

disk_size = 50
win_size = 600


def spawn_disk() -> Circle:
    x = random.randint(int(-disk_size / 2),  # nosec
                       int(win_size + disk_size / 2))
    y = random.randint(-win_size, -disk_size)  # nosec
    c = Circle(Point(x, y), disk_size)
    return c


win = GraphWin("Shapes", win_size, win_size)
win.setBackground(color_rgb(255, 255, 255))

disks = [spawn_disk() for _ in range(0, 20)]
for d in disks:
    d.draw(win)
win.redraw()

while True:
    for i, d in enumerate(disks):
        d.move(0, 2)
        if d.getCenter().getY() - d.getRadius() > win_size:
            disks[i] = spawn_disk()
            disks[i].draw(win)
    win.redraw()
    update(30)
