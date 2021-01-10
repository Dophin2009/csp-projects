import pygame
import random


def setup():
    global screen, clock
    screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
    clock = pygame.time.Clock()


def main():
    done = False
    snowflakes = []
    for i in range(200):
        x = random.randint(0, screen.get_width())
        y = random.randint(0, screen.get_height())
        snowflakes.append((x, y))

    # Load backgorund image
    img = pygame.image.load('background.png')
    img.convert()
    img_rect = img.get_rect()

    while not done:
        screen.fill(pygame.Color('lightskyblue'))
        screen.blit(img, img_rect)

        # Go through the event queue (mouse moves, key presses, etc.)
        for e in pygame.event.get():
            # X or escape key
            if e.type == pygame.QUIT or \
                    (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                # End the program
                done = True

        for i in range(len(snowflakes)):
            snowflakes[i] = (snowflakes[i][0], snowflakes[i][1] + 4)
            pygame.draw.circle(screen, pygame.Color('snow2'), snowflakes[i], 5)
            if snowflakes[i][1] > screen.get_height():
                snowflakes[i] = (snowflakes[i][0], -10)

        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pygame.init()
    setup()
    main()
    pygame.quit()
