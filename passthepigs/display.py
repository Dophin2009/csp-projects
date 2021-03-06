import os
from typing import Dict, List, Tuple

import pygame
from pygame import Surface
from pygame.time import Clock

from .simulation import SimulationState, TossData
from .simulation.toss import TossPairResultType, TossResult


class Display:
    def __enter__(self):
        class DisplayInner:
            WIDTH = 600
            HEIGHT = 600

            TOP_MARGIN_TOP = 30
            TOP_MARGIN_LEFT = 30
            TOP_HEIGHT = 100

            BOTTOM_MARGIN_BOTTOM = 30
            BOTTOM_MARGIN_LEFT = 30
            BOTTOM_HEIGHT = 150

            TICK_SPEED = 1000

            def __init__(self):
                pygame.display.set_caption('Pass the Pigs')
                self._screen = pygame.display.set_mode(
                    [self.WIDTH, self.HEIGHT])
                self._clock = Clock()

                sprite_dir = os.path.join(this_dir(), 'sprites')
                self._sprite_loader = _PigSpriteLoader(sprite_dir)

                top_left = self.TOP_MARGIN_LEFT
                top_top = self.TOP_MARGIN_TOP
                top_width = self.WIDTH - 2 * top_left
                top_height = self.TOP_HEIGHT
                self._score_panel = _ScorePanel(self._screen,
                                                top_left, top_top,
                                                top_width, top_height)

                bottom_left = self.BOTTOM_MARGIN_LEFT
                bottom_width = self.WIDTH - 2 * bottom_left
                bottom_height = self.BOTTOM_HEIGHT
                bottom_top = (
                    self.HEIGHT - self.BOTTOM_MARGIN_BOTTOM - bottom_height)
                self._stat_panel = _StatPanel(self._screen,
                                              bottom_left, bottom_top,
                                              bottom_width, bottom_height)

            def update(self, state: SimulationState):
                self.__draw_background()
                self.__draw_top(state)
                self.__draw_pigs(state.toss)
                self.__draw_bottom(state)

                pygame.display.flip()
                self._clock.tick(self.TICK_SPEED)

            def __draw_background(self):
                self._screen.fill('white')

            def __draw_top(self, state: SimulationState):
                self._score_panel.draw(state)

            def __draw_pigs(self, toss: TossData):
                t1, t2 = toss.toss.to_pair()

                s1 = self._sprite_loader.load_sprite(t1)
                s2 = self._sprite_loader.load_sprite(t2)

                third_width = int(self.WIDTH / 3)
                half_height = int(self.HEIGHT / 2.3)
                s1_rect = s1.get_rect()
                s2_rect = s2.get_rect()

                self.__blit(s1, third_width - int(s1_rect.w / 2),
                            half_height - int(s1_rect.h / 2))
                self.__blit(s2, 2 * third_width - int(s2.get_rect().w / 2),
                            half_height - int(s2_rect.h / 2))

            def __draw_bottom(self, state: SimulationState):
                self._stat_panel.draw(state)

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

        self._name_font = pygame.font.SysFont(None, 24)
        self._score_font = pygame.font.SysFont(None, 48)
        self._turn_font = self._name_font

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
                box_color = 'grey'
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

            if i == current_player:
                turn_text = self._turn_font.render(str(state.turn.score()),
                                                   True, 'black')
                turn_left = score_text_left + 2
                turn_top = score_text_top + score_text_height + 4
                self.__blit(turn_text, turn_left, turn_top)

    def __blit(self, image: Surface, left: int, top: int):
        rect = image.get_rect()
        rect.top = top
        rect.left = left
        self._screen.blit(image, rect)


class _StatPanel:
    def __init__(self, screen: Surface,
                 left: int, top: int,
                 width: int, height: int):
        self._screen = screen
        self._left = left
        self._top = top
        self._width = width
        self._height = height

        self._toss_font = pygame.font.SysFont(None, 20)
        self._pairs_font = pygame.font.SysFont(None, 20)

        self._accumulator = _StatAccumulator()

    def rect(self) -> Tuple[int, int, int, int]:
        return (self._left, self._top, self._width, self._height)

    def draw(self, state: SimulationState):
        self._accumulator.fold_in(state)

        pygame.draw.rect(self._screen, 'lightgrey', self.rect())

        toss_num = len(self._accumulator.states()) * 2
        text_img = self._toss_font.render(
            'Total: {}'.format(toss_num), 'black', True)
        left = self._left + 10
        top = self._top + 15
        self.__blit(text_img, left, top)

        toss_counts = self._accumulator.toss_counts()
        toss_rates = self._accumulator.toss_rates()
        for i, (ty, c) in enumerate(toss_counts.items()):
            name = {
                TossResult.SIDE_DOT: 'Side (Dot)',
                TossResult.SIDE_NO_DOT: 'Side (No Dot)',
                TossResult.RAZORBACK: 'Razorback',
                TossResult.TROTTER: 'Trotter',
                TossResult.SNOUTER: 'Snouter',
                TossResult.LEANING_JOWLER: 'Leaning Jowler',
            }[ty]
            rate = toss_rates[ty]

            text_img = self._toss_font.render(
                '{}: {} / {:.4f}'.format(name, c, rate), 'black', True)

            top = self._top + 18 * (i + 1) + 15
            self.__blit(text_img, left, top)

        pair_counts = self._accumulator.pair_counts()
        pair_rates = self._accumulator.pair_rates()
        for i, (ty, c) in enumerate(pair_counts.items()):
            name = {
                TossPairResultType.SIDER: 'Sider',
                TossPairResultType.DOUBLE_RAZORBACK: 'Double Razorback',
                TossPairResultType.DOUBLE_TROTTER: 'Double Trotter',
                TossPairResultType.DOUBLE_SNOUTER: 'Double Snouter',
                TossPairResultType.DOUBLE_LEANING_JOWLER:
                'Double Leaning Jowler',
                TossPairResultType.MIXED_COMBO: 'Mixed Combo',
                TossPairResultType.PIG_OUT: 'Pig Out',
            }[ty]
            rate = pair_rates[ty]

            text_img = self._pairs_font.render(
                '{}: {} / {:.4f}'.format(name, c, rate), 'black', True)

            left = self._left + int(self._width / 2) + 10
            top = self._top + 18 * i + 15
            self.__blit(text_img, left, top)

    def __blit(self, image: Surface, left: int, top: int):
        rect = image.get_rect()
        rect.top = top
        rect.left = left
        self._screen.blit(image, rect)


class _PigSpriteLoader:
    _NAME_MAP = {
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
        return self._NAME_MAP[t]

    def resolve_image_path(self, name: str) -> str:
        return os.path.join(self._sprite_dir, '{}.png'.format(name))


class _StatAccumulator:
    def __init__(self):
        self._states = []

        self._toss_counts = {variant: 0 for variant in TossResult}
        self._toss_total = 0
        self._pair_counts = {variant: 0 for variant in TossPairResultType}
        self._pair_total = 0

    def fold_in(self, state: SimulationState):
        self._states.append(state)

        toss = state.toss.toss
        t1, t2 = toss.to_pair()

        self._toss_counts[t1] += 1
        self._toss_counts[t2] += 1
        self._toss_total += 2

        self._pair_counts[toss.ty] += 1
        self._pair_total += 1

    def states(self) -> List[SimulationState]:
        return self._states

    def toss_rates(self) -> Dict[TossResult, float]:
        total = self._toss_total
        return {k: c / total for k, c in self._toss_counts.items()}

    def pair_rates(self) -> Dict[TossPairResultType, float]:
        total = self._pair_total
        return {k: c / total for k, c in self._pair_counts.items()}

    def toss_counts(self) -> Dict[TossResult, int]:
        return self._toss_counts

    def pair_counts(self) -> Dict[TossPairResultType, int]:
        return self._pair_counts


def this_dir() -> str:
    return os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(os.path.abspath(__file__))
