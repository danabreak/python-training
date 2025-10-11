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
    
    def __eq__(self,student):
        return self.ID == student.ID
    


    @property
    def gpa(self):
      if not self.grades:
        return 0.0
      avg = self.get_average() 
      return round(avg / 25, 2)  




class GraduateStudent(Student):

    def __init__(self, name, ID,thesis_title):
        super().__init__(name, ID)
        self.thesis_title=thesis_title


    def __str__(self):
        base = super().__str__()
        return f"{base} | Thesis: {self.thesis_title}"

