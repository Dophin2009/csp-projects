from __future__ import annotations

import random

from . import Player, PlayerChoiceInput, TurnChoice


class RandomPlayer(Player):
    def __init__(self, stop_rate: float):
        self._stop_rate = stop_rate

    def turn_choice(self, _: PlayerChoiceInput):
        if random.random() > self._stop_rate:
            return TurnChoice.CONTINUE
        else:
            return TurnChoice.STOP


class ThresholdPlayer(Player):
    def __init__(self, score_threshold: int):
        self._score_threshold = score_threshold

    def turn_choice(self, data: PlayerChoiceInput):
        if data.turn_state.score() < self._score_threshold:
            return TurnChoice.CONTINUE
        else:
            return TurnChoice.STOP
