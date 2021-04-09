from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Iterator, List, Optional, Tuple

from .tokenize import Tokenizer

Prefix = Tuple[str, ...]
Suffix = str
SuffixData = Dict[Suffix, int]
SizeGroup = Dict[Prefix, SuffixData]
ChainDict = Dict[int, SizeGroup]


class Chain:
    def __init__(self):
        self.__inner: ChainDict = dict()

    def prefixes(self, state_size: int) -> List[Prefix]:
        return list(self.__inner[state_size])

    def suffixes_of(self, prefix: Prefix) -> Optional[SuffixData]:
        state_size = len(prefix)
        if state_size not in self.__inner:
            return None

        if prefix in self.__inner[state_size]:
            return self.__inner[state_size][prefix]
        else:
            return None

    def inner(self) -> ChainDict:
        return self.__inner

    def state_sizes(self) -> List[int]:
        return list(self.__inner.keys())

    def _insert(self, prefix: Prefix, suffix: Suffix) -> None:
        state_size = len(prefix)

        if state_size not in self.__inner:
            self.__inner[state_size] = {prefix: {suffix: 1}}
        elif prefix not in self.__inner[state_size]:
            self.__inner[state_size][prefix] = {suffix: 1}
        else:
            suffixes = self.__inner[state_size][prefix]
            if suffix in suffixes:
                suffixes[suffix] += 1
            else:
                suffixes[suffix] = 1


class ChainBuilder:
    def __init__(self, max_state_size: int = 3) -> None:
        self.__tokenizer = Tokenizer()
        self.__max_state_size = max_state_size

        self.__chain = Chain()

    def add(self, text: Text) -> ChainBuilder:
        previous = [_ChainState(n)
                    for n in range(0, self.__max_state_size + 1)]

        chain = self.__chain

        for line in text.lines():
            if len(line) == 0:
                continue

            units = self.__tokenizer.tokenize(line)
            if len(units) <= 1:
                continue

            for unit in units:
                if len(unit) == 0:
                    continue

                is_start = True
                for state_size, _ in enumerate(previous):
                    state = previous[state_size]

                    if state.is_filled():
                        chain._insert(state.pieces, unit)
                        is_start = False

                    state.shift_new(unit)

                if is_start:
                    chain._insert(tuple(), unit)

        return self

    def finish(self) -> Chain:
        return self.__chain


class _ChainState:
    def __init__(self, state_size: int) -> None:
        self.state_size = state_size
        self.pieces: Tuple[str, ...] = ('',) * state_size

    def shift_new(self, new: str) -> None:
        self.pieces = (*self.pieces[1:], new)

    def is_filled(self) -> bool:
        return all(piece != '' for piece in self.pieces)


class Text(ABC):
    @abstractmethod
    def lines(self) -> Iterator[str]:
        pass
