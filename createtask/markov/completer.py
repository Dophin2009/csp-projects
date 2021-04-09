from __future__ import annotations

from datetime import datetime
from random import Random
from typing import List, Optional

from .chain import Chain, Prefix, Suffix


class Completer:
    ENDINGS = ['.', '?', '!', '…']

    def __init__(self, chain: Chain, rand: Optional[Random] = None) -> None:
        self.__chain = chain

        if rand is None:
            self.__rand = Random(datetime.now())
        else:
            self.__rand = rand

    def sentence(self, prefix: Prefix = (), min_n: int = 0) -> List[str]:
        """
        Given a prefix, complete the sentence.
        """
        def is_ending(s: Suffix) -> bool:
            for ending in self.ENDINGS:
                if s == ending or s[-1] == ending:
                    return True
            return False

        max_state_size = self.__max_state_size()

        n = 0
        sent = []
        while True:
            suffix = self.suffix_any(prefix)
            if suffix is not None:
                sent.append(suffix)
            else:
                break

            n += 1
            if n > min_n and is_ending(suffix):
                break

            if len(prefix) == max_state_size:
                prefix = (*prefix[1:], suffix)
            else:
                prefix = (*prefix, suffix)

        return sent

    def suffix_n(self, prefix: Prefix, n: int) -> Optional[List[str]]:
        """
        Given a prefix, produce a list of n suffixes, using the latest suffixes
        as prefixes for the next.
        """
        max_state_size = self.__max_state_size()

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

    def __max_state_size(self) -> int:
        max_state_size = self.__chain.state_sizes()
        if len(max_state_size) == 0:
            return None
        return sorted(max_state_size, reverse=True)[0]
