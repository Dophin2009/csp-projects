def main():
    with open('exercise-03.txt', 'r') as f:
        nums = f.read().splitlines()

    with open('exercise-05.txt', 'w') as f:
        for n in nums:
            if int(n) < 50:
                f.write('{}\n'.format(n))


if __name__ == '__main__':
    main()
