from pathlib import Path
from typing import List

from .markov import Chain, ChainBuilder, Completer
from .markov.text import FileText, LineTexts
from .markov.tokenize import Tokenizer


def main():
    chain = build_chain()
    print()

    completer = Completer(chain)
    tokenizer = Tokenizer()

    while True:
        print('> ', end='')
        try:
            prefix_input = input().strip()
        except KeyboardInterrupt:
            break

        prefix = tuple(t for t in tokenizer.tokenize(prefix_input) if t != '')

        try:
            sent_tokens = [*prefix, *completer.sentence(prefix)]
        except KeyboardInterrupt:
            print()
            continue
        sent = tokenizer.detokenize(sent_tokens)
        print(sent)


def build_chain() -> Chain:
    builder = ChainBuilder(max_state_size=3)
    for p in corpus_filepaths():
        print('Loading {}...'.format(p.name))
        with open(p, 'r') as f:
            for text in LineTexts(FileText(f)).texts():
                builder.add(text)

    return builder.finish()


def corpus_filepaths() -> List[Path]:
    corpus_dir = __here().joinpath('corpus')
    return [p for p in corpus_dir.iterdir() if p.is_file()]


def __here() -> Path:
    return Path(__file__).parent.absolute()


if __name__ == '__main__':
    main()
