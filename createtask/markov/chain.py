from __future__ import annotations

import pathlib
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Iterator, List, Union


class Chain:
    def __init__(self):
        self.__inner: Dict[str, Dict[str, int]] = Dict()

    def rand_suffix(self, prefix: str) -> str:
        # TODO: unimplemented!
        return ''

    def _insert(self, prefix: str, suffix: str) -> None:
        if prefix in self.__inner:
            suffixes = self.__inner[prefix]
            if suffix in suffixes:
                suffixes[suffix] += 1
            else:
                suffixes[suffix] = 1
        else:
            self.__inner[prefix] = {suffix: 1}


PathLike = Union[str, pathlib.Path]


@dataclass
class SplitConfig:
    punctuation: List[str]
    split: str


class ChainBuilder:
    __default_config = SplitConfig(punctuation=['.', ',', '?', '!', '(',
                                                ')', '[', ']', "'", '"'],
                                   split=' ')

    def __init__(self) -> None:
        self.__config = self.__class__.__default_config
        self.__chain = Chain()

    def add(self, text: Text) -> ChainBuilder:
        return self

    def finish(self) -> Chain:
        return self.__chain


class Text(ABC):
    @abstractmethod
    def lines(self) -> Iterator[str]:
        pass
