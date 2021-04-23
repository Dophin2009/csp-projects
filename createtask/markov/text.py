import re
from io import TextIOWrapper
from typing import Iterator

from .chain import Text


class FileText(Text):
    """
    Text implementation for a file handle. The constructor can be considered a
    non-moving pass of the file object; this class does not resource manage the
    file.
    """

    CLEANERS = [
        (re.compile(r'“|”|‟'), '"'),
    ]

    def __init__(self, f: TextIOWrapper) -> None:
        self.__inner = f

    def lines(self) -> Iterator[str]:
        return map(lambda line: self.__clean(line), self.__inner)

    def __clean(self, s: str) -> str:
        s = s.rstrip()

        for regexp, substitution in self.CLEANERS:
            s = regexp.sub(substitution, s)

        return s


class LineTexts:
    def __init__(self, text: Text):
        self.__text = text

    def texts(self) -> Iterator[Text]:
        return map(lambda line: StringText(line), self.__text.lines())


class StringText(Text):

    def __init__(self, inner: str):
        self.__inner = inner

    def lines(self) -> Iterator[str]:
        return [self.__inner].__iter__()
