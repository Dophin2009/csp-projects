import os
from typing import Dict, Tuple

import pygame
from pygame import Surface
from pygame.time import Clock

from .simulation import SimulationState, TossData
from .simulation.toss import TossResult


class Display:
    def __enter__(self):
        class DisplayInner:
            WIDTH = 600
            HEIGHT = 600

            TOP_MARGIN_TOP = 30
            TOP_MARGIN_LEFT = 30
            TOP_HEIGHT = 80

            def __init__(self):
                pygame.display.set_caption('Pass the Pigs')
                self._screen = pygame.display.set_mode(
                    [self.WIDTH, self.HEIGHT])
                self._clock = Clock()

                sprite_dir = os.path.join(this_dir(), 'sprites')
                self._sprite_loader = _PigSpriteLoader(sprite_dir)

                top_width = self.WIDTH - 2 * self.TOP_MARGIN_LEFT
                top_height = 100

                self._score_panel = _ScorePanel(self._screen,
                                                self.TOP_MARGIN_LEFT,
                                                self.TOP_MARGIN_TOP,
                                                top_width, top_height)

            def update(self, state: SimulationState):
                self.__draw_background()
                self.__draw_top(state)
                self.__draw_pigs(state.toss)
                self.__draw_bottom()

                pygame.display.flip()
                self._clock.tick(30)

            def __draw_background(self):
                self._screen.fill('white')

            def __draw_top(self, state: SimulationState):
                self._score_panel.draw(state)

            def __draw_pigs(self, toss: TossData):
                t1, t2 = toss.toss.to_pair()

                s1 = self._sprite_loader.load_sprite(t1)
                s2 = self._sprite_loader.load_sprite(t2)

                third_width = int(self.WIDTH / 3)
                half_height = int(self.HEIGHT / 2)
                s1_rect = s1.get_rect()
                s2_rect = s2.get_rect()

                self.__blit(s1, third_width - int(s1_rect.w / 2),
                            half_height - int(s1_rect.h / 2))
                self.__blit(s2, 2 * third_width - int(s2.get_rect().w / 2),
                            half_height - int(s2_rect.h / 2))

            def __draw_bottom(self):
                pass

            def __blit(self, image: Surface, left: int, top: int):
                rect = image.get_rect()
                rect.top = top
                rect.left = left
                self._screen.blit(image, rect)

        pygame.init()
        return DisplayInner()

    def __exit__(self, exc_type, exc_value, traceback):
        pygame.quit()


class _ScorePanel:
    def __init__(self, screen: Surface,
                 left: int, top: int,
                 width: int, height: int):
        self._screen = screen
        self._left = left
        self._top = top
        self._width = width
        self._height = height

        self._score_font = pygame.font.SysFont(None, 48)
        self._name_font = pygame.font.SysFont(None, 24)

    def rect(self) -> Tuple[int, int, int, int]:
        return (self._left, self._top, self._width, self._height)

    def draw(self, state: SimulationState):
        players = state.player_states
        current_player = state.current_player

        pygame.draw.rect(self._screen, 'gray', self.rect())

        box_width = self._width / len(players)
        box_height = self._height - 10
        for i, ps in enumerate(players):
            box_left = int(self._left + i * box_width)
            box_top = self._top + 5
            rect = (box_left, box_top,
                    box_width, box_height)

            if i == current_player:
                box_color = 'lightblue'
            else:
                box_color = 'lightgrey'
            pygame.draw.rect(self._screen, box_color, rect)

            score_text = self._score_font.render(
                str(ps.score), True, 'black')
            score_text_rect = score_text.get_rect()
            score_text_height = score_text_rect.h
            score_text_left = box_left + 10
            score_text_top = int(
                box_top + box_height / 2 - score_text_height / 2)
            self.__blit(score_text, score_text_left, score_text_top)

            name_text = self._name_font.render(
                ps.player.name(), True, 'black')
            self.__blit(name_text, score_text_left, box_top + 8)

    def __blit(self, image: Surface, left: int, top: int):
        rect = image.get_rect()
        rect.top = top
        rect.left = left
        self._screen.blit(image, rect)


class _PigSpriteLoader:
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


def this_dir() -> str:
    return os.path.dirname(os.path.abspath(__file__))
