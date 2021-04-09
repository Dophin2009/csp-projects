from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Iterator, List, Optional

from .tokenize import Tokenizer

ChainDict = Dict[str, Dict[str, int]]


class Chain:
    def __init__(self):
        self.__inner: ChainDict = dict()

    def prefixes(self) -> List[str]:
        return list(self.__inner)

    def suffixes_of(self, prefix: str) -> Optional[Dict[str, int]]:
        if prefix in self.__inner:
            return self.__inner[prefix]
        else:
            return None

    def inner(self) -> ChainDict:
        return self.__inner

    def _insert(self, prefix: str, suffix: str) -> None:
        if prefix in self.__inner:
            suffixes = self.__inner[prefix]
            if suffix in suffixes:
                suffixes[suffix] += 1
            else:
                suffixes[suffix] = 1
        else:
            self.__inner[prefix] = {suffix: 1}


class ChainBuilder:
    def __init__(self) -> None:
        self.__tokenizer = Tokenizer()
        self.__chain = Chain()

    def add(self, text: Text) -> ChainBuilder:
        chain = self.__chain
        for line in text.lines():
            if len(line) == 0:
                continue

            units = self.__tokenizer.tokenize(line)
            if len(units) <= 1:
                prefix = ''
                continue

            prefix = ''
            for unit in units:
                if len(unit) == 0:
                    continue

                chain._insert(prefix, unit)
                prefix = unit

        return self

    def finish(self) -> Chain:
        return self.__chain


class Text(ABC):
    @abstractmethod
    def lines(self) -> Iterator[str]:
        pass
