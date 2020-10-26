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
    game = Game(2, 11)
    game.loop()


class Game:
    __y_offset = 30

    def __init__(self, num_players: int, pairs: int):
        self.win = GraphWin('Matching Game', WIN_SIZE, WIN_SIZE)

        self.__reset_num_players = num_players
        self.__reset_pairs = pairs

        self.reset()

    def reset(self):
        self.__state = State(self.__reset_num_players, self.__reset_pairs)

        colors = set()
        for _ in range(self.__reset_pairs):
            c = random_color()
            while c in colors:
                c = random_color()
            colors.add(c)

        self.__color_map = {n: c for n, c in enumerate(colors)}

        rect = Rectangle(Point(0, 0), Point(self.win.width, self.win.height))
        rect.draw(self.win)

    def loop(self):
        while True:
            self.draw()
            if self.__state.all_matched():
                break

            pos = self.wait_click_pos()
            if pos is None:
                continue

            r, c = pos
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
        self.draw_game_over()

    def draw(self):
        y_offset = 30

        rows = self.__state.board_rows()
        cols = self.__state.board_cols()
        y_size = (self.win.height - y_offset) / rows
        x_size = self.win.width / cols

        header = Rectangle(Point(0, 0), Point(self.win.width, y_offset))
        header.setFill("grey")
        header.draw(self.win)

        score_spacing = self.win.width / (self.__state.num_players() + 1)
        for i, score in enumerate(self.__state.player_points()):
            score_text = Text(
                Point((i + 1) * score_spacing, y_offset / 2), score)
            if i == self.__state.current_player():
                score_text.setStyle('bold')
                score_text.setSize(18)
            score_text.setTextColor("black")
            score_text.draw(self.win)

        for r in range(rows):
            for c in range(cols):
                card = self.__state.card_at(r, c)
                rx = c * x_size
                ry = r * y_size + y_offset

                rect = Rectangle(Point(rx, ry),
                                 Point(rx + x_size, ry + y_size))

                if card is None:
                    color = "black"
                else:
                    selected = self.__state.selected()
                    if card.matched() \
                            or selected[0] == (r, c) \
                            or selected[1] == (r, c):
                        (color, fg) = self.__color_map[card.value()]
                    else:
                        color = "white"

                rect.setFill(color)
                rect.draw(self.win)

    def draw_game_over(self):
        width = 300
        height = 50

        winners = self.__state.highest_score_players()

        tx = self.win.width / 2 - width / 2
        ty = self.win.height / 2 - height / 2
        rect = Rectangle(Point(tx, ty), Point(tx + width, ty + height))
        rect.setFill("grey")
        rect.draw(self.win)

        if len(winners) == 1:
            text_str = 'Player {} wins, press q to exit'.format(winners[0])
        else:
            text_str = 'Players {} win, press q to exit'.format(
                ', '.join(str(w) for w in winners))
        text = Text(Point(tx + width / 2, ty + 20), text_str)
        text.setTextColor("black")
        text.draw(self.win)

        key = self.wait_key()
        if key == 'q':
            text.setText('exiting...')
            time.sleep(1)
            self.win.close()
        else:
            self.reset()
            self.loop()

    def wait_click_pos(self) -> Optional[Tuple[int, int]]:
        point = self.wait_click()
        if point.y < self.__y_offset:
            return None

        (x_size, y_size) = self.square_dim()
        return (int((point.y - self.__y_offset) / y_size),
                int(point.x / x_size))

    def wait_click(self) -> Point:
        return self.win.getMouse()

    def wait_key(self) -> str:
        return self.win.getKey()

    def close(self):
        self.win.close()

    def square_dim(self) -> Tuple[float, float]:
        y = (self.win.height - self.__y_offset) / self.__state.board_rows()
        return (self.win.width / self.__state.board_cols(), y)


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

    def all_matched(self) -> bool:
        return all(c is None or c.matched()
                   for row in self.__board for c in row)

    def select_card(self, r: int, c: int) -> bool:
        v = self.card_at(r, c)
        if v is Card.Empty \
                or v.matched() is True \
                or (r, c) == self.__selected[0]:
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

    def match_found(self):
        self.card_at_tup(self.__selected[0]).flip()
        self.card_at_tup(self.__selected[1]).flip()
        self.__player_points[self.__current_player] += 1

    def next_player(self):
        if self.__current_player == self.__num_players - 1:
            self.__current_player = 0
        else:
            self.__current_player += 1

    def current_player(self):
        return self.__current_player

    def highest_score_players(self) -> List[int]:
        m = max(self.__player_points)
        return [i for i, x in enumerate(self.__player_points) if x == m]

    def player_points(self):
        return self.__player_points

    def num_players(self) -> int:
        return self.__num_players

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


def random_color() -> Tuple[str, str]:
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    if (r * 0.299 + g * 0.587 + b * 0.114) > 186:
        fg = "white"
    else:
        fg = "black"

    return (graphics.color_rgb(r, g, b), fg)


if __name__ == '__main__':
    main()
