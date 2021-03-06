from typing import List

import pygame

from passthepigs import Display, Pig, Player, Simulator
from passthepigs.simulation.ai import RandomPlayer, ThresholdPlayer


class PassThePigs:
    def __init__(self, players: List[Player], p1: Pig, p2: Pig):
        self._simulator = Simulator(players, p1, p2)

    def play(self):
        simulation = self._simulator.simulate()
        simgen = simulation.run()

        with Display() as display:
            playing = True
            stopped = False
            while not stopped:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        stopped = True
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            stopped = True

                if playing:
                    state = next(simgen)
                    display.update(state)


def main():
    rai = RandomPlayer(0.15)
    thai = ThresholdPlayer(5)

    p1 = Pig.standard()
    p2 = Pig.standard()

    game = PassThePigs([rai, thai], p1, p2)
    game.play()


if __name__ == '__main__':
    main()
