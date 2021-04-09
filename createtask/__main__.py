from pathlib import Path
from typing import List

from .markov import Chain, ChainBuilder, Completer
from .markov.text import FileText
from .markov.tokenize import Tokenizer


def main():
    chain = build_chain()

    completer = Completer(chain)

    prefix = ('After',)
    sent_tokens = [*prefix, *completer.sentences(prefix)]

    tokenizer = Tokenizer()
    sent = tokenizer.detokenize(sent_tokens)
    print(sent)


def build_chain() -> Chain:
    builder = ChainBuilder(max_state_size=5)
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
