def main():
    with open('secret-message.txt', 'r') as f:
        lines = f.read().splitlines()

    with open('exercise-08.txt', 'w') as f:
        lines = [line[0] for line in lines]
        f.writelines(lines)


if __name__ == '__main__':
    main()
