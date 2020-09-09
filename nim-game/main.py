from game import Game, GameState, Interface, Pile


def prompt_with(prompt: str) -> str:
    return input(prompt + " ")


def prompt_user_int(prompt: str) -> int:
    num_str = prompt_with(prompt)
    try:
        return int(num_str)
    except ValueError:
        return prompt_user_int(prompt)


class CommandLineInterface(Interface):
    def update(self, state: GameState):
        print("Player {}'s turn:".format(state.current_player))
        for i, p in enumerate(state.piles):
            print("Pile {}: {}".format(i, p.sticks))

    def prompt_pile(self, state: GameState) -> int:
        prompt_msg = "Select pile ({} - {}):".format(
            0, state.player_count - 1)
        return prompt_user_int(prompt_msg)

    def prompt_take(self, pile: Pile) -> int:
        return prompt_user_int(
            "Select sticks (max {}):".format(pile.sticks))

    def game_over(self, state: GameState):
        print("Game over: player {} lost".format(state.current_player))


if __name__ == "__main__":
    interface = CommandLineInterface()
    players = prompt_user_int("Number of players?")
    piles = prompt_user_int("Number of piles?")
    game = Game(interface, piles, players)
    game.loop()
