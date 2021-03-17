def main():
    with open('exercise-03.txt', 'r') as f:
        for line in f.readlines():
            print(line, end='')


if __name__ == '__main__':
    main()
