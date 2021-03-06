from __future__ import annotations

import enum
import itertools
import random
from typing import Dict, List, Optional, Tuple


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


class TossResult(enum.Enum):
    SIDE_NO_DOT = enum.auto(),
    SIDE_DOT = enum.auto(),
    RAZORBACK = enum.auto(),
    TROTTER = enum.auto(),
    SNOUTER = enum.auto(),
    LEANING_JOWLER = enum.auto(),


class TossPairResultType(enum.Enum):
    SIDER = enum.auto()
    DOUBLE_RAZORBACK = enum.auto(),
    DOUBLE_TROTTER = enum.auto(),
    DOUBLE_SNOUTER = enum.auto(),
    DOUBLE_LEANING_JOWLER = enum.auto(),
    MIXED_COMBO = enum.auto(),
    PIG_OUT = enum.auto()


class TossPairResult:
    def __init__(self, ty: TossPairResultType,
                 t1: Optional[TossResult] = None,
                 t2: Optional[TossResult] = None):
        self.ty = ty
        self.t1 = t1
        self.t2 = t2

    def to_pair(self) -> Tuple[TossResult, TossResult]:
        return {
            TossPairResultType.SIDER: lambda s: (s.t1, s.t1),
            TossPairResultType.DOUBLE_RAZORBACK: lambda _: (
                TossResult.RAZORBACK, TossResult.RAZORBACK),
            TossPairResultType.DOUBLE_TROTTER: lambda _: (
                TossResult.TROTTER, TossResult.TROTTER),
            TossPairResultType.DOUBLE_SNOUTER: lambda _: (
                TossResult.SNOUTER, TossResult.SNOUTER),
            TossPairResultType.DOUBLE_LEANING_JOWLER: lambda _: (
                TossResult.LEANING_JOWLER, TossResult.LEANING_JOWLER),
            TossPairResultType.PIG_OUT: lambda s: (s.t1, s.t2),
            TossPairResultType.MIXED_COMBO: lambda s: (s.t1, s.t2)
        }[self.ty](self)

    @classmethod
    def Sider(cls, t1: TossResult) -> TossPairResult:
        if t1 != TossResult.SIDE_DOT and t1 != TossResult.SIDE_NO_DOT:
            raise ValueError('Sider can only be made from a pair of SIDE_DOT '
                             'or SIDE_NO_DOT')
        return cls(TossPairResultType.SIDER, t1)

    @classmethod
    def DoubleRazorback(cls) -> TossPairResult:
        return cls(TossPairResultType.DOUBLE_RAZORBACK)

    @classmethod
    def DoubleTrotter(cls) -> TossPairResult:
        return cls(TossPairResultType.DOUBLE_TROTTER)

    @classmethod
    def DoubleSnouter(cls) -> TossPairResult:
        return cls(TossPairResultType.DOUBLE_SNOUTER)

    @classmethod
    def DoubleLeaningJowler(cls) -> TossPairResult:
        return cls(TossPairResultType.DOUBLE_LEANING_JOWLER)

    @classmethod
    def MixedCombo(cls, t1: TossResult, t2: TossResult) -> TossPairResult:
        return cls(TossPairResultType.MIXED_COMBO, t1, t2)

    @classmethod
    def PigOut(cls, t1: TossResult, t2: TossResult) -> TossPairResult:
        if not ((t1 == TossResult.SIDE_DOT and t2 == TossResult.SIDE_NO_DOT)
                or (t1 == TossResult.SIDE_NO_DOT and t2 == TossResult.SIDE_DOT)
                ):
            raise ValueError('Pig out can only be made from pair of SIDE_DOT '
                             'and SIDE_NO_DOT')
        return cls(TossPairResultType.PIG_OUT, t1, t2)

    @classmethod
    def from_pair(cls, t1: TossResult, t2: TossResult) -> TossPairResult:
        def is_sider(t1: TossResult, t2: TossResult) -> bool:
            return t1 == TossResult.SIDE_DOT == t2 \
                or t1 == TossResult.SIDE_NO_DOT == t2

        def is_double_razorback(t1: TossResult, t2: TossResult) -> bool:
            return t1 == TossResult.RAZORBACK == t2

        def is_double_trotter(t1: TossResult, t2: TossResult) -> bool:
            return t1 == TossResult.TROTTER == t2

        def is_double_snouter(t1: TossResult, t2: TossResult) -> bool:
            return t1 == TossResult.SNOUTER == t2

        def is_double_leaning_jowler(t1: TossResult, t2: TossResult) -> bool:
            return t1 == TossResult.LEANING_JOWLER == t2

        def is_pig_out(t1: TossResult, t2: TossResult) -> bool:
            return (t1 == TossResult.SIDE_DOT
                    and t2 == TossResult.SIDE_NO_DOT) \
                or (t1 == TossResult.SIDE_NO_DOT
                    and t2 == TossResult.SIDE_DOT)

        if is_sider(t1, t2):
            return TossPairResult.Sider(t1)
        elif is_double_razorback(t1, t2):
            return TossPairResult.DoubleRazorback()
        elif is_double_trotter(t1, t2):
            return TossPairResult.DoubleRazorback()
        elif is_double_snouter(t1, t2):
            return TossPairResult.DoubleRazorback()
        elif is_double_leaning_jowler(t1, t2):
            return TossPairResult.DoubleRazorback()
        elif is_pig_out(t1, t2):
            return TossPairResult.PigOut(t1, t2)
        else:
            return TossPairResult.MixedCombo(t1, t2)


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


class TossScorer:
    def __init__(self):
        pass

    def score_pair(self, t: TossPairResult) -> Optional[int]:
        if t.ty == TossPairResultType.SIDER:
            return 1
        elif t.ty == TossPairResultType.DOUBLE_RAZORBACK:
            return 20
        elif t.ty == TossPairResultType.DOUBLE_TROTTER:
            return 20
        elif t.ty == TossPairResultType.DOUBLE_SNOUTER:
            return 40
        elif t.ty == TossPairResultType.DOUBLE_LEANING_JOWLER:
            return 60
        elif t.ty == TossPairResultType.PIG_OUT:
            return None
        elif t.ty == TossPairResultType.MIXED_COMBO:
            assert t.t1 is not None and t.t2 is not None
            return self.score_one(t.t1) + self.score_one(t.t2)

    def score_one(self, t: TossResult) -> int:
        return {
            TossResult.SIDE_DOT: 0,
            TossResult.SIDE_NO_DOT: 0,
            TossResult.RAZORBACK: 5,
            TossResult.TROTTER: 5,
            TossResult.SNOUTER: 10,
            TossResult.LEANING_JOWLER: 15,
        }[t]
