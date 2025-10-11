import pytest
from oop.student import Student


def test_student_creation():
    s1 = Student("Dana", 100)
    assert s1.name == "Dana"
    assert s1.ID == 100
    assert s1.grades == []


def test_student_grade_addition():
    s1 = Student("Dana", 100)
    s1.add_grade(90, 85)
    assert s1.grades == [90, 85]


def test_student_average_calc_empty_grades():
    with pytest.raises(ZeroDivisionError):
        s1 = Student("Dana", 100)
        s1.get_average()


def test_student_average_calc_single_grade():
    s1 = Student("Dana", 100)
    s1.add_grade(
        90,
    )
    assert s1.get_average() == 90.0


def test_student_average_calc_multiple_grades():
    s1 = Student("Dana", 100)
    s1.add_grade(90, 70)
    assert s1.get_average() == 80.0


def test_student_str_representation():
    s1 = Student("Dana", 100)
    s1.add_grade(90)
    result = str(s1)

    assert "Student:" in result
    assert "ID:" in result
    assert "Grades:" in result
    assert "Dana" in result
    assert "90" in result
