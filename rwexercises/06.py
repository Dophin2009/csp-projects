def main():
    cities = ['Omaha', 'Garland', 'Baltimore', 'Chicago', 'Durham',
              'Birmingham', 'Colorado Springs', 'Mesa', 'New York', 'Phoenix']

    with open('exercise-06.txt', 'w') as f:
        for city in cities:
            f.write('{}\n'.format(city))


if __name__ == '__main__':
    main()
