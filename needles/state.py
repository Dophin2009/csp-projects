from __future__ import annotations

import math
import random
from typing import Tuple, List

Toss = Tuple[Tuple[int, int], Tuple[int, int]]


class State:
    def __init__(self, w: int, h: int, g: int, r: int):
        self.w = w
        self.h = h
        self.g = g

        self.r = r

        self.cross = []
        self.no_cross = []

    def toss(self) -> Toss:
        x1, y1, x2, y2 = -1, -1, -1, -1
        while x1 <= 0 or y1 <= 0 or x2 <= 0 or y2 <= 0 \
                or x1 >= self.w or y1 >= self.h \
                or x2 >= self.w or y2 >= self.h:
            x1 = random.randint(0, self.w)
            y1 = random.randint(0, self.h)
            angle = random.uniform(0, 2 * math.pi)

            x2 = x1 + int(self.r * math.cos(angle))
            y2 = y1 + int(self.r * math.sin(angle))

        t = ((x1, y1), (x2, y2))
        if any([t[0][0] <= line <= t[1][0] or t[1][0] <= line <= t[0][0]
                for line in self.cross_lines()]):
            self.cross.append(t)
        else:
            self.no_cross.append(t)

        return t

    def pi_estimate(self) -> float:
        return (2 * self.r * self.num_tosses()) / (self.g * self.num_cross())

    def num_tosses(self) -> int:
        return self.num_cross() + len(self.no_cross)

    def num_cross(self) -> int:
        return len(self.cross)

    def cross_lines(self) -> List[int]:
        return [i for i in range(self.g, self.w + 1, self.g)]

    def clear(self) -> None:
        self.cross.clear()
        self.no_cross.clear()
