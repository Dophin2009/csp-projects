def main():
    with open('exercise-03.txt', 'r') as f:
        lines = f.read().splitlines()

    nums = [int(line) for line in lines]
    nums.sort()

    with open('exercise-12.txt', 'w') as f:
        lines = ['{}\n'.format(n) for n in nums]
        f.writelines(lines)


if __name__ == '__main__':
    main()
