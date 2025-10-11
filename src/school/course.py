
from .student import Student


class Course:
     def __init__(self, name,professor):
        self.name = name
        self.professor=professor
        self.students=[]

     def add_student(self,student):
        if not isinstance(student, Student):
           raise TypeError("student must be a Student")
        if student not in self.students:
           self.students.append(student)


     def __iter__(self):
        return iter(self.students)
     
    
