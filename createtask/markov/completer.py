from __future__ import annotations

from datetime import datetime
from random import Random
from typing import List, Optional

from .chain import Chain


class Completer:
    ENDINGS = ['.', '?', '!', '…']

    def __init__(self, chain: Chain) -> None:
        self.__chain = chain
        self.__rand = Random(datetime.now())

    def sentence(self, prefix: str = '', min_n: int = 0) -> List[str]:
        def is_ending(s: str) -> bool:
            for ending in self.ENDINGS:
                if s == ending or s[-1] == ending:
                    return True
            return False

        n = 0
        latest = prefix

        sent = []
        while True:
            suffix = self.suffix(latest)
            if suffix is None:
                suffix = self.suffix('')
                assert suffix is not None
            sent.append(suffix)
            latest = suffix

            n += 1
            if n > min_n and is_ending(latest):
                break

        return sent

    def suffix_n(self, prefix: str, n: int) -> Optional[List[str]]:
        latest = prefix

        ret = []
        for _ in range(0, n):
            suffix = self.suffix(latest)
            if suffix is None:
                suffix = self.suffix('')
                assert suffix is not None
            ret.append(suffix)
            latest = suffix

        return ret

    def suffix(self, prefix: str) -> Optional[str]:
        suffixes = self.__chain.suffixes_of(prefix)
        if suffixes is None:
            return None

        suffix_list = list(suffixes)
        weights = list(suffixes.values())

        return self.__rand.choices(population=suffix_list,
                                   weights=weights,
                                   k=1)[0]

    def word(self) -> str:
        return self.__rand.choice(self.__chain.prefixes())

    def set_random(self, rand: Random) -> None:
        self.__rand = rand
