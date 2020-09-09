from argparse import ArgumentParser
import sys

import cli


def flag_parser() -> ArgumentParser:
    parser = ArgumentParser(prog="nim", description="Play the game nim.")
    parser.add_argument('-g', '--gui', action='store_true',
                        help='use the QT GUI instead of cli')
    return parser


def main():
    parser = flag_parser()
    args = parser.parse_args()

    if args.gui:
        exit(1)
    else:
        players = cli.prompt_user_int("Number of players?")
        piles = cli.prompt_user_int("Number of piles?")
        game = cli.Game(piles, players)

    game.loop()


if __name__ == "__main__":
    main()
