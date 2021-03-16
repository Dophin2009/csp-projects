from __future__ import annotations

import enum
from abc import ABC, abstractmethod
from typing import Generator, List, Optional

from .toss import Pig, Tosser, TossPairResult, TossScorer


class Player(ABC):
    """Game player interface."""

    def name(self) -> str:
        return 'Unnamed'

    @abstractmethod
    def turn_choice(self, pci: PlayerChoiceInput) -> TurnChoice:
        """Return whether player wants to continue or end their turn."""
        raise NotImplementedError(
            'Player implementation must implement turn_choice')


class PlayerChoiceInput:
    """
    Input data to be used by players to determine whether they want to continue
    or end their turns.
    """

    def __init__(self, toss: TossData,
                 turn_state: TurnState,
                 own_state: PlayerState,
                 player_states: List[PlayerState]):
        self.toss = toss
        self.turn_state = turn_state
        self.own_state = own_state
        self.player_states = player_states


class TossData:
    """
    Data about a given pig toss.
    """

    def __init__(self, toss: TossPairResult, score: Optional[int]):
        self.toss = toss
        self.score = score

    def is_pig_out(self) -> bool:
        """Returns true if the toss was a pig-out."""
        return self.score is None


class TurnChoice(enum.Enum):
    """
    Enum for a player's choice at the end of each toss.
    """
    CONTINUE = enum.auto(),
    STOP = enum.auto(),


class PlayerState:
    """
    Information about a given player's game state.
    """

    def __init__(self, player: Player):
        self.player = player
        self.score = 0

    def add_score(self, n: int):
        self.score += n

    def reset(self):
        self.score = 0

    def clone(self) -> PlayerState:
        new = PlayerState(self.player)
        new.score = self.score
        return new


class TurnState:
    """
    The state of a player's turn.
    """

    def __init__(self):
        self._score = 0

    def score(self) -> int:
        return self._score

    def add_score(self, n: int):
        self._score += 1

    def clear(self):
        self._score = 0

    def clone(self) -> TurnState:
        new = TurnState()
        new._score = self.score()
        return new


class Simulator:
    """Simulation builder class."""

    def __init__(self, players: List[Player], p1: Pig, p2: Pig):
        self._players = players
        self._p1 = p1
        self._p2 = p2

    def simulate(self) -> Simulation:
        """Return a Simulation based on this builder."""
        return Simulation(self._players, self._p1, self._p2)


class SimulationState:
    """Data about the state of the simulation at a given point."""

    def __init__(self, toss: TossData, turn: TurnState, current_player: int,
                 player_states: List[PlayerState]):
        self.toss = toss
        self.turn = turn
        self.current_player = current_player
        self.player_states = player_states


class Simulation:
    """A simulation object that can be run and reset."""

    def __init__(self, players: List[Player], p1: Pig, p2: Pig):
        self._tosser = Tosser()
        self._scorer = TossScorer()

        self._p1 = p1
        self._p2 = p2

        self._players = [PlayerState(p) for p in players]
        self._current_player = 0

    def reset(self):
        """Reset the state of the simulation."""
        self._current_player = 0
        for ps in self.player_states():
            ps.reset()

    def run(self) -> Generator[SimulationState, None, None]:
        """Return a generator that ticks and outputs simulation states."""
        turn_state = TurnState()
        while True:
            toss_data = self.toss(turn_state)

            if toss_data.score is None:
                turn_choice = TurnChoice.STOP
            else:
                pci = PlayerChoiceInput(toss_data,
                                        turn_state,
                                        self.current_player_state(),
                                        self.player_states())
                turn_choice = self.current_player().turn_choice(pci)

            if turn_choice == TurnChoice.CONTINUE:
                pass
            elif turn_choice == TurnChoice.STOP:
                self.current_player_state().add_score(turn_state.score())
                self.next_player()
                turn_state.clear()

            yield SimulationState(toss_data, turn_state.clone(),
                                  self._current_player,
                                  self.cloned_player_states())

    def toss(self, turn_state: TurnState) -> TossData:
        """Make a toss and return the data."""
        toss1 = self._tosser.toss(self._p1)
        toss2 = self._tosser.toss(self._p2)

        toss_result = TossPairResult.from_pair(toss1, toss2)
        toss_score = self._scorer.score_pair(toss_result)
        if toss_score is None:
            # Pig out: reset turn score to 0 and end turn
            turn_state.clear()
        else:
            turn_state.add_score(toss_score)

        return TossData(toss_result, toss_score)

    def next_player(self) -> int:
        """Shift to the next player's turn."""
        self._current_player += 1
        if self._current_player >= len(self._players):
            self._current_player = 0
        return self._current_player

    def player_states(self) -> List[PlayerState]:
        return self._players

    def current_player(self) -> Player:
        return self.current_player_state().player

    def current_player_score(self) -> int:
        return self.current_player_state().score

    def current_player_state(self) -> PlayerState:
        return self._players[self._current_player]

    def cloned_player_states(self) -> List[PlayerState]:
        return [ps.clone() for ps in self._players]
