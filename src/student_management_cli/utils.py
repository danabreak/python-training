import json
import csv


def load_students(filename="students.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_students(students, filename="students.json"):
    with open(filename, "w") as f:
        json.dump(students, f, indent=4)


def export_to_csv(students, filename="students_export.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "ID", "Email", "Grades"])
        for name, info in students.items():
            writer.writerow([name, info["ID"], info["email"], info["grades"]])
