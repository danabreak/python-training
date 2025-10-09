class Student:

    def __init__(self, name, ID):
        self.name = name
        self.ID = ID
        self.grades = []

    def add_grade(self, *grade):
        self.grades.extend(grade)

    def get_average(self):
        total = 0
        for x in self.grades:
            total += x
        return total / len(self.grades)

    def __str__(self):
        return f"Student: {self.name}, ID: {self.ID}, Grades: {self.grades}"
