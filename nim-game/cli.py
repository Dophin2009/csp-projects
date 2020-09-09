from game import GameState, Pile
import game


def prompt_with(prompt: str) -> str:
    return input(prompt + " ")


def prompt_user_int(prompt: str) -> int:
    num_str = prompt_with(prompt)
    try:
        return int(num_str)
    except ValueError:
        return prompt_user_int(prompt)


class Interface(game.Interface):
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


class Game(game.Game):
    def __init__(self, pile_count: int, player_count: int):
        interface = Interface()
        game.Game.__init__(self, interface, pile_count, player_count)
