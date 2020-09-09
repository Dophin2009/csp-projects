from __future__ import annotations

import random
from abc import ABC
from abc import abstractmethod
from typing import List


class Pile:
    def __init__(self, sticks: int):
        self.sticks = sticks

    def take(self, count: int) -> int:
        self.sticks -= count
        if self.sticks < 0:
            self.sticks = 0
        return self.sticks

    @staticmethod
    def random() -> Pile:
        sticks = random.randint(2, 10)
        return Pile(sticks)


class Interface(ABC):
    @abstractmethod
    def update(self, state: GameState):
        pass

    @abstractmethod
    def prompt_pile(self, state: GameState) -> int:
        pass

    @abstractmethod
    def prompt_take(self, pile: Pile) -> int:
        pass

    @abstractmethod
    def game_over(self, state: GameState):
        pass


class GameState:
    def __init__(self, piles: List[Pile], player_count: int):
        self.piles = piles
        self.player_count = player_count
        self.current_player = -1

    def next_player(self) -> int:
        self.current_player += 1
        if self.current_player == self.player_count:
            self.current_player = 0
        return self.current_player

    def clear(self) -> bool:
        for p in self.piles:
            if p.sticks != 0:
                return False
        return True


class Game:
    def __init__(self, interface: Interface, pile_count: int,
                 player_count: int):
        self.interface = interface
        piles = [Pile.random() for _ in range(0, pile_count)]
        self.state = GameState(piles, player_count)

    def loop(self):
        while not self.state.clear():
            self.next_turn()

    def next_turn(self):
        self.state.next_player()
        self.interface.update(self.state)

        pile = self.prompt_user_pile()
        take_count = self.prompt_user_take(pile)
        pile.take(take_count)

    def prompt_user_pile(self) -> Pile:
        choice = self.interface.prompt_pile(self.state)

        if choice >= len(self.state.piles) or choice < 0:
            return self.prompt_user_pile()

        pile = self.state.piles[choice]
        if pile.sticks == 0:
            return self.prompt_user_pile()

        return pile

    def prompt_user_take(self, pile: Pile) -> int:
        num = self.interface.prompt_take(pile)
        if num > pile.sticks or num < 1:
            return self.prompt_user_take(pile)
        return num
