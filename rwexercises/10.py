def main():
    with open('exercise-03.txt', 'r') as f:
        lines = f.read().splitlines()
    nums = [int(line) for line in lines]
    print(sum(nums) / len(nums))


if __name__ == '__main__':
    main()
