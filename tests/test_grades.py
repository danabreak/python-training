from grades import get_top_three, dict_transform


def test_get_top_three_returns_correct_students():
    students = [
        ("Ali", 20),
        ("Dana", 80),
        ("Omar", 70),
        ("Ahmad", 90),
        ("Fatima", 60),
        ("Talah", 100),
    ]
    result = get_top_three(students)
    assert result == ["Talah", "Ahmad", "Dana"]


def test_get_top_three_with_less_than_three_students():
    students = [("Ahmad", 90), ("Dana", 80)]
    result = get_top_three(students)
    assert result == ["Ahmad", "Dana"]


def test_dict_transform_pass_fail():
    grades = {"Ahmad": 90, "Dana": 50, "Omar": 60}
    result = dict_transform(grades)
    expected = {"Ahmad": "Pass", "Dana": "Fail", "Omar": "Pass"}
    assert result == expected


def test_dict_transform_empty_input():
    grades = {}
    result = dict_transform(grades)
    assert result == {}
