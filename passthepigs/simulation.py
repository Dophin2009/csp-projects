from __future__ import annotations

import enum
from abc import ABC, abstractmethod
from typing import Generator, List

from .toss import Pig, Tosser, TossScorer


class Player(ABC):
    @abstractmethod
    def turn_choice(self, data: TossData):
        raise NotImplementedError(
            'Player implementation must implement turn_choice')


class TossData:
    def __init__(self, total_score: int):
        self.total_score = total_score


class TurnChoice(enum.Enum):
    CONTINUE = enum.auto(),
    STOP = enum.auto(),


class PlayerState:
    def __init__(self, player: Player):
        self.player = player
        self.score = 0

    def add_score(self, n: int):
        self.score += n


class TurnState:
    def __init__(self):
        self._score = 0

    def score(self) -> int:
        return self._score

    def add_score(self, n: int):
        self._score += 1

    def clear(self):
        self._score = 0


class Simulation:
    def __init__(self, players: List[Player], p1: Pig, p2: Pig):
        self._tosser = Tosser()
        self._scorer = TossScorer()
        self._players = [PlayerState(p) for p in players]
        self._current_player = 0
        self._p1 = p1
        self._p2 = p2

    def simulate(self) -> Generator[None, None, None]:
        turn_state = TurnState()
        while True:
            current_player_state = self.current_player_state()
            turn_choice = self.toss(turn_state, current_player_state.player)
            if turn_choice == TurnChoice.CONTINUE:
                pass
            elif turn_choice == TurnChoice.STOP:
                current_player_state.add_score(turn_state.score())
                self.next_player()
                turn_state.clear()
            yield None

    def toss(self, turn_state: TurnState, player: Player) -> TurnChoice:
        toss1 = self._tosser.toss(self._p1)
        toss2 = self._tosser.toss(self._p2)

        toss_score = self._scorer.get_toss_score(toss1, toss2)
        if toss_score is None:
            # Pig out: reset turn score to 0 and end turn
            turn_state.clear()
            return TurnChoice.STOP
        else:
            turn_state.add_score(toss_score)
            return player.turn_choice(TossData(turn_state._score))

    def next_player(self) -> int:
        self._current_player += 1
        if self._current_player >= len(self._players):
            self._current_player = 0
        return self._current_player

    def player_states(self) -> List[PlayerState]:
        return self._players

    def current_player(self) -> Player:
        return self.current_player_state().player

    def current_player_state(self) -> PlayerState:
        return self._players[self._current_player]
