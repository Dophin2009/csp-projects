from __future__ import annotations

import random
from typing import Iterator, Tuple


class Game:

    def __init__(self, rows: int, cols: int, n: int):
        self.board = [[Cell(False) for _ in range(cols)] for _ in range(rows)]
        self._starting = [(random.randint(0, rows - 1),
                           random.randint(0, cols - 1))
                          for _ in range(n)]
        for r, c in self._starting:
            self.board[r][c].set_alive()

    def reset(self):
        for r, _ in enumerate(self.board):
            for c, _ in enumerate(self.board[r]):
                self.board[r][c].set_dead()

        for r, c in self._starting:
            self.board[r][c].set_alive()

    def update(self):
        for r, _ in enumerate(self.board):
            for c, _ in enumerate(self.board[r]):
                self.__update_cell_next(r, c)

        for r, _ in enumerate(self.board):
            for c, _ in enumerate(self.board[r]):
                self.cell_at(r, c).tick()

    def __update_cell_next(self, r: int, c: int):
        alive_neighbors = sum(1 for _ in self.alive_neighbors_of(r, c))

        cell = self.board[r][c]
        if cell.is_alive():
            if alive_neighbors < 2:
                cell.set_next_dead()
            elif alive_neighbors > 3:
                cell.set_next_dead()
        elif alive_neighbors == 3:
            cell.set_next_alive()

    def alive_neighbors_of(self, r: int, c: int) -> Iterator[Cell]:
        return filter(lambda cell: cell.is_alive(), self.neighbors_of(r, c))

    def neighbors_of(self, r: int, c: int) -> Iterator[Cell]:
        """
        Returns references to the neighboring cells for the cell at the
        given position.
        """
        offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                   (0, 1), (1, -1), (1, 0), (1, 1)]
        unchecked = map(lambda cc: (r + cc[0], c + cc[1]), offsets)

        min_r = 0
        max_r = len(self.board)
        min_c = 0
        max_c = len(self.board[0])

        checked = filter(lambda cc: min_r <=
                         cc[0] < max_r and min_c <= cc[1] < max_c, unchecked)
        return map(lambda cc: self.cell_at(cc[0], cc[1]), checked)

    def cell_at(self, r: int, c: int) -> Cell:
        return self.board[r][c]

    def __str__(self) -> str:
        return str(self.board)


class Cell:

    def __init__(self, alive: bool):
        self._alive = alive
        self._next_alive = alive

    def tick(self):
        self._alive = self._next_alive

    def is_alive(self) -> bool:
        return self._alive

    def set_alive(self):
        self._alive = True

    def set_dead(self):
        self._alive = False

    def set_next(self, alive: bool):
        self._next_alive = alive

    def set_next_alive(self):
        self._next_alive = True

    def set_next_dead(self):
        self._next_alive = False

    def __str__(self) -> str:
        return 'Cell(alive = {}, next = {})'.format(self._alive,
                                                    self._next_alive)
