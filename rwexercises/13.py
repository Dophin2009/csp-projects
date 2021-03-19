def main():
    with open('exercise-03.txt', 'r') as f:
        lines = f.read().splitlines()

    for i, line in enumerate(lines):
        if line == '50':
            print(i)
            return

    print('not found')


if __name__ == '__main__':
    main()
