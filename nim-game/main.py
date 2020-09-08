from __future__ import annotations

import random


def prompt_with(prompt: str) -> str:
    return input(prompt + " ")


def prompt_user_int(prompt: str) -> int:
    num_str = prompt_with(prompt)
    try:
        return int(num_str)
    except ValueError:
        return prompt_user_int(prompt)


class Pile:
    def __init__(self, sticks: int):
        self.sticks = sticks

    def take(self):
        self.sticks -= 1

    @staticmethod
    def random() -> Pile:
        sticks = random.randint(2, 10)
        return Pile(sticks)


class Game:
    def __init__(self, piles: int, player_count: int):
        self.piles = [Pile.random() for _ in range(0, piles)]
        self.player_count = player_count
        self.current_player = -1

    def loop(self):
        while not self.piles_clear():
            self.print_status()
            self.next_turn()
        print("Game over: player {} lost".format(self.current_player))

    def piles_clear(self) -> bool:
        for p in self.piles:
            if p.sticks != 0:
                return False
        return True

    def next_turn(self):
        self.current_player += 1
        if self.current_player == self.player_count:
            self.current_player = 0

        print("Player {}'s turn:".format(self.current_player))

        pile = self.prompt_user_pile()
        take_count = self.prompt_user_take(pile)

        pile.sticks -= take_count

    def prompt_user_pile(self) -> Pile:
        prompt_msg = "Select pile ({} - {}):".format(
            0, self.player_count - 1)
        choice = prompt_user_int(prompt_msg)

        if choice >= len(self.piles) or choice < 0:
            return self.prompt_user_pile()

        pile = self.piles[choice]
        if pile.sticks == 0:
            return self.prompt_user_pile()

        return pile

    def prompt_user_take(self, pile: Pile) -> int:
        num = prompt_user_int(
            "Select sticks (max {}):".format(pile.sticks))
        if num > pile.sticks or num < 1:
            return self.prompt_user_take(pile)
        return num

    def print_status(self):
        for i, p in enumerate(self.piles):
            print("Pile {}: {}".format(i, p.sticks))


if __name__ == "__main__":
    players = prompt_user_int("Number of players?")
    piles = prompt_user_int("Number of piles?")
    game = Game(piles, players)
    game.loop()
