from __future__ import annotations

from datetime import datetime
from random import Random
from typing import List, Optional

from .chain import Chain, Prefix, Suffix


class Completer:
    ENDINGS = ['.', '?', '!', '…']

    def __init__(self, chain: Chain, max_state_size: Optional[int] = None,
                 rand: Optional[Random] = None) -> None:
        self.__chain = chain
        self.__max_state_size = max_state_size

        if rand is None:
            self.__rand = Random(datetime.now())
        else:
            self.__rand = rand

    def sentences(self, prefix: Prefix = (),
                  min_n: int = 3, min_c: int = 0) -> List[str]:
        """
        Given a prefix, complete multiple sentences.
        """
        max_state_size = self.max_state_size()
        if max_state_size is None:
            return []

        n = 0
        c = 0
        sent = []
        while True:
            suffix = self.suffix_any(prefix)
            if suffix is not None:
                sent.append(suffix)
            else:
                break

            c += 1
            if self.__is_ending(suffix):
                n += 1
                if n > min_n and c > min_c:
                    break

            if len(prefix) >= max_state_size:
                start = len(prefix) - max_state_size + 1
                prefix = (*prefix[start:], suffix)
            else:
                prefix = (*prefix, suffix)

        return sent

    def sentence(self, prefix: Prefix = (), min_c: int = 0) -> List[str]:
        """
        Given a prefix, complete the sentence.
        """
        return self.sentences(prefix, 1, min_c)

    def suffix_n(self, prefix: Prefix, n: int) -> Optional[List[str]]:
        """
        Given a prefix, produce a list of n suffixes, using the latest suffixes
        as prefixes for the next.
        """
        max_state_size = self.max_state_size()

        ret = []
        for _ in range(0, n):
            suffix = self.suffix_any(prefix)
            if suffix is not None:
                ret.append(suffix)
            else:
                break

            if len(prefix) == max_state_size:
                prefix = (*prefix[1:], suffix)
            else:
                prefix = (*prefix, suffix)

        return ret

    def suffix_any(self, prefix: Prefix) -> Optional[Suffix]:
        """
        Return a random suffix for the given prefix, searching the chain for
        any suffix for an ending sub-prefix.
        """
        if len(prefix) == 0:
            return self.suffix(())

        suffix = None
        while len(prefix) != 0:
            suffix = self.suffix(prefix)
            if suffix is not None:
                break
            else:
                prefix = prefix[1:]
        return suffix

    def suffix(self, prefix: Prefix) -> Optional[Suffix]:
        """
        Return a random suffix for the given prefix.
        """
        suffixes = self.__chain.suffixes_of(prefix)
        if suffixes is not None:
            suffix_list = list(suffixes)
            weights = list(suffixes.values())

            return self.__rand.choices(population=suffix_list,
                                       weights=weights,
                                       k=1)[0]
        else:
            return None

    def word(self) -> Optional[Prefix]:
        """
        Return a random prefix from the chain. The prefix is selected from
        state size = 1 group.
        """
        prefixes = self.__chain.prefixes(1)
        if prefixes is not None:
            return self.__rand.choice(prefixes)
        else:
            return None

    def start_word(self) -> Optional[Suffix]:
        """
        Return a random start word from the chain. The prefix is selected from
        state size = 0 group.
        """
        suffixes = self.__chain.suffixes_of(())
        if suffixes is not None:
            suffix = self.__rand.choices(list(suffixes.keys()),
                                         weights=list(suffixes.values()))
            if len(suffix) != 0:
                return suffix[0]
        else:
            return None

    def __is_ending(self, s: Suffix) -> bool:
        for ending in self.ENDINGS:
            if s == ending:
                return True
        return False

    def max_state_size(self) -> Optional[int]:
        if self.__max_state_size is not None:
            return self.__max_state_size

        max_state_size = self.__chain.state_sizes()
        if len(max_state_size) == 0:
            return None

        return max(max_state_size)
