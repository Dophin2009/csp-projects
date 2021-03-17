def main():
    with open('exercise-06.txt', 'r') as f:
        lines = f.read().splitlines()

    lengths = [len(s) for s in lines]
    with open('exercise-07.txt', 'w') as f:
        for n in lengths:
            f.write('{}\n'.format(n))


if __name__ == '__main__':
    main()
