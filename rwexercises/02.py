def main():
    with open('exercise-02.txt', 'w') as f:
        for n in range(2, 101, 2):
            f.write('{}\n'.format(n))
        for n in range(1, 101, 2):
            f.write('{}\n'.format(n))


if __name__ == '__main__':
    main()
