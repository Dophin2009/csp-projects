import random
from typing import Iterator, Tuple

import pygame
from pygame import Surface
from pygame.time import Clock

from game import Game

WIDTH = 600
HEIGHT = 600

ROWS = 30
COLS = 30

RECT_W = int(WIDTH / ROWS)
RECT_H = int(HEIGHT / COLS)


def main():
    game = Game(ROWS, COLS)
    for r, c in generate_random_coords(300):
        game.board[r][c].set_alive()

    pygame.init()

    pygame.display.set_caption("Conway's Game of Life")
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    clock = Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                (event.type == pygame.KEYDOWN
                 and event.key == pygame.K_ESCAPE):
                running = False

        for r, _ in enumerate(game.board):
            for c, _ in enumerate(game.board[r]):
                draw_cell(screen, game, r, c)

        pygame.display.flip()
        clock.tick(10)

        game.update()

    pygame.quit()


def draw_cell(screen: Surface, game: Game, r: int, c: int):
    cell = game.cell_at(r, c)
    if cell.is_alive():
        color = (0, 0, 0)
    else:
        color = (255, 255, 255)

    pygame.draw.rect(screen, color,
                     (r * RECT_W, c * RECT_H, RECT_W, RECT_H))


def generate_random_coords(n: int) -> Iterator[Tuple[int, int]]:
    return ((random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
            for _ in range(n))


if __name__ == '__main__':
    main()
