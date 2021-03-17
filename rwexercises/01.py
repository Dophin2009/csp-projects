def main():
    with open('exercise-01.txt', 'w') as f:
        for n in range(1, 101):
            f.write('{}\n'.format(n))


if __name__ == '__main__':
    main()
