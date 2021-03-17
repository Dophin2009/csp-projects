import random


def main():
    with open('exercise-03.txt', 'w') as f:
        for _ in range(0, 100):
            n = random.randint(1, 100)
            f.write('{}\n'.format(n))


if __name__ == '__main__':
    main()
