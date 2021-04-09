from pathlib import Path
from typing import List

from .markov import Chain, ChainBuilder, Completer
from .markov.text import FileText
from .markov.tokenize import Detokenizer


def main():
    chain = build_chain()

    completer = Completer(chain)

    completed = completer.sentence('After', 5)
    sent_tokens = ['After'] + completed

    detokenizer = Detokenizer()
    sent = detokenizer.detokenize(sent_tokens)
    print(sent)


def build_chain() -> Chain:
    builder = ChainBuilder()
    for p in corpus_filepaths():
        with open(p, 'r') as f:
            builder.add(FileText(f))

    return builder.finish()


def corpus_filepaths() -> List[Path]:
    corpus_dir = __here().joinpath('corpus')
    return [p for p in corpus_dir.iterdir() if p.is_file()]


def __here() -> Path:
    return Path(__file__).parent.absolute()


if __name__ == '__main__':
    main()
