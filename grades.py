def get_top_three(students):
    top_three = sorted(students, key=lambda x: x[1], reverse=True)[:3]
    names = [name for name, grade in top_three]
    return names


def dict_transform(grades):
    results = {s: "Pass" if g >= 60 else "Fail" for s, g in grades.items()}
    return results
