from pathlib import Path
from typing import List

from .markov import ChainBuilder
from .markov.text import FileText


def main():
    builder = ChainBuilder()
    for p in __corpus_filepaths():
        with open(p, 'r') as f:
            builder.add(FileText(f))

    _ = builder.finish()


def __corpus_filepaths() -> List[Path]:
    corpus_dir = __here().joinpath('corpus')
    return [p for p in corpus_dir.iterdir() if p.is_file()]


def __here() -> Path:
    return Path(__file__).parent.absolute()


if __name__ == '__main__':
    main()
