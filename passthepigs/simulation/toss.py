from __future__ import annotations

import enum
import itertools
import random
from typing import Dict, List, Optional, Tuple


class Tosser:
    """Class that tosses pigs."""

    def __init__(self):
        pass

    def toss(self, pig: Pig) -> TossResult:
        """
        Toss the given pig by selecting a random toss result based on the
        pig's weighted rates.
        """
        rates = [(rate, result) for rate, result in pig.rates.items()]
        sample_idx = self.__sample([r for r, _ in rates])
        return [res for _, res in rates][sample_idx]

    def __sample(self, probabilities: List[float]) -> int:
        """
        Given a list of weighted probabilities, randomly select an index based
        on those weights.
        """
        totals = list(itertools.accumulate(probabilities))
        n = random.uniform(0, totals[-1])
        for i, total in enumerate(totals):
            if n <= total:
                return i

        # Unreachable
        return 0


class TossResult(enum.Enum):
    """Enum for possible pig toss results."""
    SIDE_NO_DOT = enum.auto(),
    SIDE_DOT = enum.auto(),
    RAZORBACK = enum.auto(),
    TROTTER = enum.auto(),
    SNOUTER = enum.auto(),
    LEANING_JOWLER = enum.auto(),


class TossPairResultType(enum.Enum):
    """Enum for possible pig pair toss results."""
    SIDER = enum.auto()
    DOUBLE_RAZORBACK = enum.auto(),
    DOUBLE_TROTTER = enum.auto(),
    DOUBLE_SNOUTER = enum.auto(),
    DOUBLE_LEANING_JOWLER = enum.auto(),
    MIXED_COMBO = enum.auto(),
    PIG_OUT = enum.auto()


# I'd have liked to been able to create a proper tagged union.
class TossPairResult:
    """
    Result of tossing a pair of pigs, with information about individual
    tosses saved.
    """

    def __init__(self, ty: TossPairResultType,
                 t1: Optional[TossResult] = None,
                 t2: Optional[TossResult] = None):
        self.ty = ty
        self.t1 = t1
        self.t2 = t2

    def to_pair(self) -> Tuple[TossResult, TossResult]:
        """Convert this pair result back into a pair of tosses."""
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
        """Create a sider pair result."""
        if t1 != TossResult.SIDE_DOT and t1 != TossResult.SIDE_NO_DOT:
            raise ValueError('Sider can only be made from a pair of SIDE_DOT '
                             'or SIDE_NO_DOT')
        return cls(TossPairResultType.SIDER, t1)

    @classmethod
    def DoubleRazorback(cls) -> TossPairResult:
        """Create a double razorback pair result."""
        return cls(TossPairResultType.DOUBLE_RAZORBACK)

    @classmethod
    def DoubleTrotter(cls) -> TossPairResult:
        """Create a double trotter pair result."""
        return cls(TossPairResultType.DOUBLE_TROTTER)

    @classmethod
    def DoubleSnouter(cls) -> TossPairResult:
        """Create a double snouter pair result."""
        return cls(TossPairResultType.DOUBLE_SNOUTER)

    @classmethod
    def DoubleLeaningJowler(cls) -> TossPairResult:
        """Create a double leaning jowler pair result."""
        return cls(TossPairResultType.DOUBLE_LEANING_JOWLER)

    @classmethod
    def MixedCombo(cls, t1: TossResult, t2: TossResult) -> TossPairResult:
        """Create a mixed combo pair result."""
        return cls(TossPairResultType.MIXED_COMBO, t1, t2)

    @classmethod
    def PigOut(cls, t1: TossResult, t2: TossResult) -> TossPairResult:
        """Create a pig-out pair result."""
        if not ((t1 == TossResult.SIDE_DOT and t2 == TossResult.SIDE_NO_DOT)
                or (t1 == TossResult.SIDE_NO_DOT and t2 == TossResult.SIDE_DOT)
                ):
            raise ValueError('Pig out can only be made from pair of SIDE_DOT '
                             'and SIDE_NO_DOT')
        return cls(TossPairResultType.PIG_OUT, t1, t2)

    @classmethod
    def from_pair(cls, t1: TossResult, t2: TossResult) -> TossPairResult:
        """Convert a pair of tosses in a pair toss result."""
        def is_sider(t1: TossResult, t2: TossResult) -> bool:
            return (t1 == TossResult.SIDE_DOT == t2) \
                or (t1 == TossResult.SIDE_NO_DOT == t2)

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
            return TossPairResult.DoubleTrotter()
        elif is_double_snouter(t1, t2):
            return TossPairResult.DoubleSnouter()
        elif is_double_leaning_jowler(t1, t2):
            return TossPairResult.DoubleLeaningJowler()
        elif is_pig_out(t1, t2):
            return TossPairResult.PigOut(t1, t2)
        else:
            return TossPairResult.MixedCombo(t1, t2)


"""Standard Pass the Pigs pig toss rates."""
STANDARD_RATES = {
    0.349: TossResult.SIDE_NO_DOT,
    0.302: TossResult.SIDE_DOT,
    0.224: TossResult.RAZORBACK,
    0.088: TossResult.TROTTER,
    0.030: TossResult.SNOUTER,
    0.007: TossResult.LEANING_JOWLER,
}


class Pig:
    """Model of a pig, with weighted toss probability information."""

    def __init__(self, rates: Dict[float, TossResult]):
        self.rates = rates

        if sum([r for r in self.rates]) != 1:
            raise ValueError("rates must add up to 1")

    @classmethod
    def standard(cls) -> Pig:
        """Return a standard pig."""
        return cls(STANDARD_RATES)


class TossScorer:
    """Class for scoring individual and pairs of tosses."""

    def __init__(self):
        pass

    def score_pair(self, t: TossPairResult) -> Optional[int]:
        """
        Return the score of a pair result; None if the result is a pig-out.
        """
        def mixed_combo(t1: Optional[TossResult],
                        t2: Optional[TossResult]) -> int:
            assert t1 is not None and t2 is not None
            return self.score_one(t1) + self.score_one(t2)

        return {
            TossPairResultType.SIDER: lambda _: 1,
            TossPairResultType.DOUBLE_RAZORBACK: lambda _: 20,
            TossPairResultType.DOUBLE_TROTTER: lambda _: 20,
            TossPairResultType.DOUBLE_SNOUTER: lambda _: 40,
            TossPairResultType.DOUBLE_LEANING_JOWLER: lambda _: 60,
            TossPairResultType.PIG_OUT: lambda _: None,
            TossPairResultType.MIXED_COMBO: lambda t: mixed_combo(t.t1, t.t2),
        }[t.ty](t)

    def score_one(self, t: TossResult) -> int:
        """Return the score of a single pig toss."""
        return {
            TossResult.SIDE_DOT: 0,
            TossResult.SIDE_NO_DOT: 0,
            TossResult.RAZORBACK: 5,
            TossResult.TROTTER: 5,
            TossResult.SNOUTER: 10,
            TossResult.LEANING_JOWLER: 15,
        }[t]
