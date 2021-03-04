import os
from typing import Dict, List

import pygame
from pygame import Surface
from pygame.time import Clock

from simulation import (Pig, Player, PlayerState, Simulation, SimulationState,
                        Simulator, TossData, TossResult)
from simulation.ai import RandomPlayer, ThresholdPlayer


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


class Display:
    def __enter__(self):
        class DisplayInner:
            WIDTH = 600
            HEIGHT = 600

            def __init__(self):
                pygame.display.set_caption('Pass the Pigs')
                self._screen = pygame.display.set_mode(
                    [self.WIDTH, self.HEIGHT])
                self._clock = Clock()

                self._sprite_loader = PigSpriteLoader('sprites')

            def update(self, state: SimulationState):
                self._screen.fill('white')
                self.__draw_pigs(state.toss)

                pygame.display.flip()
                self._clock.tick(5)

            def __draw_pigs(self, toss: TossData):
                t1 = toss.t1
                t2 = toss.t2

                s1 = self._sprite_loader.load_sprite(t1)
                s2 = self._sprite_loader.load_sprite(t2)
                self.__blit(s1, 0, 0)
                self.__blit(s2, 200, 200)

            def __blit(self, image: Surface, top: int, left: int):
                rect = image.get_rect()
                rect.top = top
                rect.left = left
                self._screen.blit(image, rect)

        pygame.init()
        return DisplayInner()

    def __exit__(self, exc_type, exc_value, traceback):
        pygame.quit()


class PigSpriteLoader:
    _MAP = {
        TossResult.SIDE_DOT: 'side_dot',
        TossResult.SIDE_NO_DOT: 'side_no_dot',
        TossResult.RAZORBACK: 'razorback',
        TossResult.TROTTER: 'trotter',
        TossResult.SNOUTER: 'snouter',
        TossResult.LEANING_JOWLER: 'leaning_jowler',
    }

    def __init__(self, sprite_dir: str):
        self._sprite_dir = sprite_dir

        self._cache: Dict[TossResult, Surface] = {}

    def load_sprite(self, t: TossResult) -> Surface:
        if t in self._cache.keys():
            return self._cache[t]

        name = self.get_sprite_name(t)
        path = self.resolve_image_path(name)

        sprite = pygame.image.load(path)
        sprite.convert()

        self._cache[t] = sprite
        return sprite

    def get_sprite_name(self, t: TossResult) -> str:
        return self._MAP[t]

    def resolve_image_path(self, name: str) -> str:
        return os.path.join(self._sprite_dir, '{}.png'.format(name))


def main():
    rai = RandomPlayer(0.15)
    thai = ThresholdPlayer(5)

    p1 = Pig.standard()
    p2 = Pig.standard()

    game = PassThePigs([rai, thai], p1, p2)
    game.play()


if __name__ == '__main__':
    main()
