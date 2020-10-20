from __future__ import annotations

import math
import random
import time
from typing import Generator
from typing import List
from typing import Optional
from typing import Tuple
from typing import TypeVar

import graphics
from graphics import GraphWin
from graphics import Point
from graphics import Rectangle
from graphics import Text

WIN_SIZE = 600


def main():
    game = Game(2, 9)
    game.loop()


class Game:
    def __init__(self, num_players: int, pairs: int):
        self.__state = State(num_players, pairs)
        self.__color_map = {i: random_color() for i in range(pairs)}
        self.win = GraphWin('Matching Game', WIN_SIZE, WIN_SIZE)

    def loop(self):
        game_over = False
        while not game_over:
            self.draw()
            r, c = self.get_click_pos()
            did_select = self.__state.select_card(r, c)
            if not did_select:
                continue

            if self.__state.selection_full():
                self.draw()
                if self.__state.selected_match():
                    self.__state.match_found()
                else:
                    self.__state.next_player()
                time.sleep(1)
                self.__state.clear_selected()

    def get_click_pos(self) -> Tuple[int, int]:
        point = self.win.getMouse()
        (x_size, y_size) = self.square_dim()
        return (int(point.y / y_size), int(point.x / x_size))

    def draw(self):
        rows = self.__state.board_rows()
        cols = self.__state.board_cols()
        y_size = self.win.height / rows
        x_size = self.win.width / cols

        for r in range(rows):
            for c in range(cols):
                card = self.__state.card_at(r, c)
                rx = c * x_size
                ry = r * y_size

                rect = Rectangle(Point(rx, ry),
                                 Point(rx + x_size, ry + y_size))

                if card is None:
                    color = "black"
                else:
                    color = self.__color_map[card.value()]
                    selected = self.__state.selected()
                    if card.matched():
                        rect.setFill(color)
                        text = Text(Point(rx + (x_size / 2),
                                          ry + (y_size / 2)),
                                    card.value())
                        text.draw(self.win)
                    elif selected[0] == (r, c) or selected[1] == (r, c):
                        rect.setFill(color)
                    else:
                        rect.setFill("white")

                rect.draw(self.win)

    def square_dim(self) -> Tuple[float, float]:
        return (self.win.width / self.__state.board_cols(),
                self.win.height / self.__state.board_rows())


class Card:
    Empty = None

    def __init__(self, v: int, matched: bool):
        self.__v = v
        self.__matched = matched

    def flip(self):
        self.__matched = not self.__matched

    def value(self) -> int:
        return self.__v

    def matched(self) -> bool:
        return self.__matched

    def __eq__(self, o):
        if o is None:
            return False
        try:
            return self.__v == o.value() and self.__matched == o.matched()
        except Exception:
            return False

    def __repr__(self) -> str:
        return 'Card({}, {})'.format(self.__v, self.__matched)


Selection = Tuple[Optional[Tuple[int, int]],
                  Optional[Tuple[int, int]]]


class State:
    def __init__(self, num_players: int, pairs: int):
        self.__num_players = num_players
        self.__player_points = [0 for _ in range(self.__num_players)]
        self.__current_player = 0

        self.__board = State.generate_board(pairs)
        self.__selected: Selection = (None, None)

    def select_card(self, r: int, c: int) -> bool:
        v = self.card_at(r, c)
        if v is Card.Empty or v.matched() is True or v == self.__selected[0]:
            return False
        elif self.__selected[0] is None:
            self.__selected = ((r, c), self.__selected[1])
            return True
        else:
            self.__selected = (self.__selected[0], (r, c))
            return True

    def clear_selected(self):
        self.__selected = (None, None)

    def selection_full(self) -> bool:
        return self.__selected[0] is not None \
            and self.__selected[1] is not None

    def selected_match(self) -> bool:
        if self.__selected[0] is None or self.__selected[1] is None:
            return False
        first = self.card_at(self.__selected[0][0], self.__selected[0][1])
        second = self.card_at(self.__selected[1][0], self.__selected[1][1])
        return first == second

    def selected(self) -> Selection:
        return self.__selected

    def next_player(self):
        if self.__current_player == self.__num_players - 1:
            self.__current_player = 0
        else:
            self.__current_player += 1

    def match_found(self):
        self.card_at_tup(self.__selected[0]).flip()
        self.card_at_tup(self.__selected[1]).flip()
        self.__player_points[self.__current_player] += 1

    def card_at(self, r: int, c: int) -> Optional[Card]:
        return self.__board[r][c]

    def card_at_tup(self, tup: Tuple[int, int]) -> Optional[Card]:
        return self.__board[tup[0]][tup[1]]

    def board_rows(self) -> int:
        return len(self.__board)

    def board_cols(self) -> int:
        return len(self.__board[0])

    @staticmethod
    def generate_board(pairs: int) -> List[List[Optional[Card]]]:
        num = 2 * pairs
        side = math.ceil(math.sqrt(num))

        arr: List[Optional[Card]] = [Card(x, False)
                                     for x in range(pairs) for _ in (0, 0)]
        rem = side - num % side
        for _ in range(rem):
            arr.append(Card.Empty)

        random.shuffle(arr)
        matrix = list(chunk_list(arr, side, Card.Empty))
        return matrix


T = TypeVar('T')


def chunk_list(arr: List[T], n: int, p: T) -> Generator[List[T], None, None]:
    arr_len = len(arr)
    for i in range(0, arr_len, n):
        end = i + n
        if end > arr_len:
            c = arr[i:arr_len]
            for i in range(i, arr_len):
                c.append(p)
            yield c
        else:
            yield arr[i:i + n]


def random_color() -> str:
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return graphics.color_rgb(r, g, b)


if __name__ == '__main__':
    main()
