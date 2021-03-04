from __future__ import annotations

import enum
import itertools
import random
from typing import Dict, List, Optional


class TossScorer:
    def __init__(self):
        self.checker = TossChecker()
        pass

    def score_pair(self, t1: TossResult, t2: TossResult) -> Optional[int]:
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
        else:
            return self.score_one(t1) + self.score_one(t2)

    def score_one(self, t: TossResult) -> int:
        return {
            TossResult.SIDE_DOT: 0,
            TossResult.SIDE_NO_DOT: 0,
            TossResult.RAZORBACK: 5,
            TossResult.TROTTER: 5,
            TossResult.SNOUTER: 10,
            TossResult.LEANING_JOWLER: 15,
        }[t]


class Tosser:
    def __init__(self):
        pass

    def toss(self, pig: Pig) -> TossResult:
        rates = [(rate, result) for rate, result in pig.rates.items()]
        sample_idx = self.__sample([r for r, _ in rates])
        return [res for _, res in rates][sample_idx]

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
