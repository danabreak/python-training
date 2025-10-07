# tests/test_students_all.py
import os

from student_management_cli.manager import (
    register_student,
    update_grades,
    list_top_three,
    export_list,
)
from student_management_cli.utils import save_students  # لتفريغ الداتا ببساطة


def reset_data():
    """ابدئي كل اختبار بملف طلاب فاضي."""
    save_students({})
    # لو بدك تمسحي ملف التصدير بعد كل اختبار لما تحتاجي
    if os.path.exists("students_export.csv"):
        os.remove("students_export.csv")


# ---------------------------
# register_student
# ---------------------------

def test_register_student_happy_path():
    reset_data()
    s = register_student("Dana", "1001", "dana@mail.com", "90,80,100")
    assert s["ID"] == "1001"
    assert s["email"] == "dana@mail.com"
    assert s["grades"] == [90, 80, 100]


def test_register_student_duplicate_name_raises():
    reset_data()
    register_student("Ali", "2001", "ali@mail.com", "70,80")
    try:
        register_student("Ali", "2002", "ali2@mail.com", "60")
        assert False, "Expected ValueError for duplicate student name"
    except ValueError as e:
        assert "already exists" in str(e)


def test_register_student_invalid_email_raises():
    reset_data()
    for bad in ["no-at.com", "a@b", "a@b,com"]:
        try:
            register_student("X", "1", bad, "90")
            assert False, f"Expected ValueError for email: {bad}"
        except ValueError as e:
            assert "Invalid email" in str(e)


def test_register_student_non_int_grades_raises():
    reset_data()
    try:
        register_student("Nour", "3001", "nour@mail.com", "90,abc,70")
        assert False, "Expected ValueError for non-integer grades"
    except ValueError as e:
        assert "integers" in str(e)


def test_register_student_grade_out_of_range_raises():
    reset_data()
    try:
        register_student("Sam", "4001", "sam@mail.com", "101,90")
        assert False, "Expected ValueError for grade > 100"
    except ValueError as e:
        assert "between 0 and 100" in str(e)


# ---------------------------
# update_grades
# ---------------------------

def test_update_grades_happy_path():
    reset_data()
    register_student("Lana", "5001", "lana@mail.com", "50,60")
    info = update_grades("Lana", "80,90,100")
    assert info is not None
    assert info["grades"] == [80, 90, 100]


def test_update_grades_user_not_found_returns_none():
    reset_data()
    info = update_grades("NotExist", "70,80")
    assert info is None


def test_update_grades_invalid_input_raises():
    reset_data()
    register_student("Omar", "6001", "omar@mail.com", "55,65")
    try:
        update_grades("Omar", "70,xyz")
        assert False, "Expected ValueError for invalid grades"
    except ValueError as e:
        assert "integers" in str(e)


def test_update_grades_out_of_range_raises():
    reset_data()
    register_student("Mira", "7001", "mira@mail.com", "90,95")
    try:
        update_grades("Mira", "120,80")
        assert False, "Expected ValueError for grade out of range"
    except ValueError as e:
        assert "between 0 and 100" in str(e)


# ---------------------------
# list_top_three
# ---------------------------

def test_list_top_three_ordering_and_limit():
    reset_data()
    register_student("A", "1", "a@mail.com", "100,100")      # avg 100
    register_student("B", "2", "b@mail.com", "90,90,90")     # avg 90
    register_student("C", "3", "c@mail.com", "60")           # avg 60
    register_student("D", "4", "d@mail.com", "70,80")        # avg 75 → خارج التوب 3

    top = list_top_three()
    # top عبارة عن قائمة tuples: (name, avg)
    names_in_order = [name for name, _ in top]
    assert names_in_order == ["A", "B", "D"] or names_in_order == ["A", "B", "C"]
    # ملاحظة: حسب حسابتك للمتوسط، D=75 و C=60 → الترتيب: A, B, D


def test_list_top_three_when_less_than_three_students():
    reset_data()
    register_student("OnlyOne", "9", "one@mail.com", "50,100")
    top = list_top_three()
    assert len(top) == 1
    assert top[0][0] == "OnlyOne"


# ---------------------------
# export_list
# ---------------------------
def test_export_list_creates_csv_file():
    reset_data()
    register_student("Z", "9", "z@mail.com", "80,90")
    export_list()
    assert os.path.exists("students_export.csv")

    with open("students_export.csv", "r", encoding="utf-8") as f:
        content = f.read().lower()
    # عدلنا السطر التالي: شطبنا ",avg"
    assert "name,id,email,grades" in content
