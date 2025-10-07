import sys


def get_top_three(students):
    top_three = sorted(students, key=lambda x: x[1], reverse=True)[:3]
    names = [name for name, grade in top_three]
    return names


def dict_transform(grades):
    results = {s: "Pass" if g >= 60 else "Fail" for s, g in grades.items()}
    return results


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  python src/grades.py top-three\n"
            "  python src/grades.py transform\n"
        )
        return

    cmd = sys.argv[1]

    # Example student data
    students = [("Dana", 88), ("Lama", 75), ("Khaled", 92), ("Sara", 55), ("Omar", 60)]

    grades_dict = {"Dana": 88, "Lama": 75, "Khaled": 92, "Sara": 55, "Omar": 60}

    if cmd == "top-three":
        names = get_top_three(students)
        print("🏆 Top three students:", ", ".join(names))

    elif cmd == "transform":
        results = dict_transform(grades_dict)
        for student, result in results.items():
            print(f"{student}: {result}")

    else:
        print("Invalid command. Use 'top-three' or 'transform'.")


if __name__ == "__main__":
    main()
