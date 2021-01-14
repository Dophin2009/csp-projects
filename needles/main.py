import pygame
from pygame.time import Clock
from pygame.color import Color


def main():
    screen = pygame.display.set_mode([600, 600])
    clock = Clock()

    done = False
    while not done:
        screen.fill(Color('lightskyblue'))
        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
