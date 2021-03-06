from __future__ import annotations

import random
from typing import Optional

from . import Player, PlayerChoiceInput, TurnChoice


class RandomPlayer(Player):
    def __init__(self, stop_rate: float, name: Optional[str] = None):
        self._name = name or 'Random({:.2f})'.format(stop_rate)
        self._stop_rate = stop_rate

    def name(self) -> str:
        return self._name

    def turn_choice(self, _: PlayerChoiceInput):
        if random.random() > self._stop_rate:
            return TurnChoice.CONTINUE
        else:
            return TurnChoice.STOP


class ThresholdPlayer(Player):
    def __init__(self, score_threshold: int, name: Optional[str] = None):
        self._name = name or 'Threshold({})'.format(score_threshold)
        self._score_threshold = score_threshold

    def name(self) -> str:
        return self._name

    def turn_choice(self, data: PlayerChoiceInput):
        if data.turn_state.score() < self._score_threshold:
            return TurnChoice.CONTINUE
        else:
            return TurnChoice.STOP
