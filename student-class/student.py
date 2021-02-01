import random


class Student:
    def __init__(self, id: int, grade: int, gpa: float,
                 stress: int = 0, courses: int = 0):
        self.id = id
        self.grade = grade
        self.gpa = gpa
        self.stress = stress
        self.courses = courses

    def attend_class(self) -> None:
        for course in range(0, self.courses):
            self.stress = max(0, self.stress + random.randint(-5, 5))
            self.gpa = max(0, self.gpa + (random.random() - 0.5) * 0.1)

    def slack_off(self) -> None:
        self.stress = max(0, self.stress - 5)
        self.gpa = max(0, self.gpa - 0.01)


def main():
    a = Student(0, 11, 4.8, courses=5)
    b = Student(1, 11, 5.15, courses=5)

    a.attend_class()
    a.slack_off()

    b.attend_class()
    b.slack_off()

    print('{:.2f}'.format(a.gpa))
    print('{:.2f}'.format(b.gpa))


if __name__ == '__main__':
    main()
