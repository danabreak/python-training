from .utils import save_students, load_students, export_to_csv


def register_student(name, ID, email, grades):
    students = load_students()

    if name in students:
        raise ValueError(f"Student '{name}' already exists.")

    if "@" not in email or "." not in email.split("@")[-1]:
        raise ValueError("Invalid email format.")

    try:
        grades = [int(x.strip()) for x in grades.split(",")] if grades.strip() else []
    except ValueError:
        raise ValueError("Grades must be integers separated by commas, e.g. 90,80,100")

    for g in grades:
        if not (0 <= g <= 100):
            raise ValueError("Each grade must be between 0 and 100.")

    students[name] = {
        "ID": ID,
        "email": email,
        "grades": grades,
    }

    save_students(students)
    return students[name]


def update_grades(name: str, grades_new: str):
    students = load_students()

    info = students.get(name)
    if info is None:
        print("Not found")
        return None
    try:
        grades = (
            [int(x.strip()) for x in grades_new.split(",")]
            if grades_new.strip()
            else []
        )
    except ValueError:
        raise ValueError("Grades must be integers separated by commas, e.g. 90,80,100")
    for g in grades:
        if not 0 <= g <= 100:
            raise ValueError("Each grade must be between 0 and 100")
    info["grades"] = grades
    students[name] = info
    save_students(students)
    return info


def list_top_three():
    students = load_students()
    scored = []
    for name, info in students.items():
        grades = info.get("grades", [])
        if grades:
            avg = sum(grades) / len(grades)
        else:
            avg = 0
        scored.append((name, avg))

    sorted_students = sorted(scored, key=lambda x: x[1], reverse=True)
    top_three = sorted_students[:3]
    for name, avg in top_three:
        print(f"{name}: Average = {avg:.2f}")

    return top_three


def export_list():
    students = load_students()
    export_to_csv(students)
    print("✅ Exported to students_export.csv")
