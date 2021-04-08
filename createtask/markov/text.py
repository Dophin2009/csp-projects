from io import TextIO
from typing import Iterator

from .chain import Text


class FileText(Text):
    """
    Text implementation for a file handle. The constructor can be considered a
    non-moving pass of the file object; this class does not resource manage the
    file.
    """

    def __init__(self, f: TextIO) -> None:
        self.__inner = f

    def lines(self) -> Iterator[str]:
        return self.__inner
