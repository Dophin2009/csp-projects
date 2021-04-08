from __future__ import annotations

from typing import List, Optional

from .chain import Chain


class Completer:
    def __init__(self, chain: Chain) -> None:
        self.__chain = chain

    def sentence(self, suffix: Optional[str] = None,
                 min_n: Optional[int] = None) -> List[str]:
        # TODO: unimplemented!
        return []

    def suffix_n(self, prefix: str, n: int) -> List[str]:
        # TODO: unimplemented!
        return []

    def suffix(self, prefix: str) -> str:
        return ''

    def word(self) -> str:
        return ''
