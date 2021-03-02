from __future__ import annotations

import enum
import itertools
import random
from typing import Dict, Generator, List, Optional


class Player:


class Simulation:
    def __init__(self, players: List[Player], p1: Pig, p2: Pig):
        self._tosser = Tosser()
        self._scorer = TossScorer()
        self._scores = [0] * players
        self._current_player = 0
        self._p1 = p1
        self._p2 = p2

    def simulate(self) -> Generator[None, None, None]:
        while True:

        yield None

    def toss(self):
        toss1 = self._tosser.toss(self._p1)
        toss2 = self._tosser.toss(self._p2)

        toss_score = self._scorer.get_toss_score(toss1, toss2)
        if toss_score is None:
            new_score = 0
        else:
            new_score = self._scores[self._current_player] + toss_score
        self._scores[self._current_player] = new_score

    def next_player(self) -> int:
        self._current_player += 1
        if self._current_player >= len(self._scores):
            self._current_player = 0
        return self._current_player

    def scores(self) -> List[int]:
        return self._scores

    def current_player(self) -> int:
        return self._current_player


class TossScorer:
    def __init__(self):
        self.checker = TossChecker()
        pass

    def get_toss_score(self, t1: TossResult, t2: TossResult) -> Optional[int]:
        if self.checker.is_sider(t1, t2):
            return 1
        elif self.checker.is_double_razorback(t1, t2):
            return 20
        elif self.checker.is_double_trotter(t1, t2):
            return 20
        elif self.checker.is_double_snouter(t1, t2):
            return 40
        elif self.checker.is_double_leaning_jowler(t1, t2):
            return 60
        elif self.checker.is_pig_out(t1, t2):
            return None


class Tosser:
    def __init__(self):
        pass

    def toss(self, pig: Pig) -> TossResult:
        sample_idx = self.__sample([r for r in pig.rates])
        return pig.rates[sample_idx]

    def __sample(self, probabilities: List[float]) -> int:
        totals = list(itertools.accumulate(probabilities))
        n = random.uniform(0, totals[-1])
        for i, total in enumerate(totals):
            if n <= total:
                return i

        # Unreachable
        return 0


class TossChecker:
    def __init__(self):
        pass

    def is_sider(self, t1: TossResult, t2: TossResult) -> bool:
        return t1 == TossResult.SIDE_DOT == t2 \
            or t1 == TossResult.SIDE_NO_DOT == t2

    def is_double_razorback(self, t1: TossResult, t2: TossResult) -> bool:
        return t1 == TossResult.RAZORBACK == t2

    def is_double_trotter(self, t1: TossResult, t2: TossResult) -> bool:
        return t1 == TossResult.TROTTER == t2

    def is_double_snouter(self, t1: TossResult, t2: TossResult) -> bool:
        return t1 == TossResult.SNOUTER == t2

    def is_double_leaning_jowler(self, t1: TossResult, t2: TossResult) -> bool:
        return t1 == TossResult.LEANING_JOWLER == t2

    def is_pig_out(self, t1: TossResult, t2: TossResult) -> bool:
        return (t1 == TossResult.SIDE_DOT and t2 == TossResult.SIDE_NO_DOT) \
            or (t1 == TossResult.SIDE_NO_DOT and t2 == TossResult.SIDE_DOT)


class TossResult(enum.Enum):
    SIDE_NO_DOT = enum.auto(),
    SIDE_DOT = enum.auto(),
    RAZORBACK = enum.auto(),
    TROTTER = enum.auto(),
    SNOUTER = enum.auto(),
    LEANING_JOWLER = enum.auto(),


STANDARD_RATES = {
    0.349: TossResult.SIDE_NO_DOT,
    0.302: TossResult.SIDE_DOT,
    0.224: TossResult.RAZORBACK,
    0.088: TossResult.TROTTER,
    0.030: TossResult.SNOUTER,
    0.007: TossResult.LEANING_JOWLER,
}


class Pig:
    def __init__(self, rates: Dict[float, TossResult]):
        self.rates = rates

        if sum([r for r in self.rates]) != 1:
            raise ValueError("rates must add up to 1")

    @classmethod
    def standard(cls) -> Pig:
        return cls(STANDARD_RATES)
