from __future__ import annotations

import math
import random
from typing import Tuple

Toss = Tuple[Tuple[int, int], Tuple[int, int]]


class State:
    def __init__(self, w: int, h: int, r: int):
        self.w = w
        self.h = h

        self.r = r
        self.tosses = []

    def toss(self) -> Toss:
        x1, y1, x2, y2 = -1, -1, -1, -1
        while x1 <= 0 or y1 <= 0 or x2 <= 0 or y2 <= 0:
            x1 = random.randint(0, self.w)
            y1 = random.randint(0, self.h)
            angle = random.uniform(0, 2 * math.pi)

            x2 = x1 + int(self.r * math.cos(angle))
            y2 = y1 + int(self.r * math.sin(angle))

        toss = ((x1, y1), (x2, y2))
        print(toss)

        self.tosses.append(toss)
        return toss

    def clear(self) -> None:
        self.tosses.clear()
