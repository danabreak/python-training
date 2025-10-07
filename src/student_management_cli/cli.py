import sys

from .manager import register_student, update_grades, list_top_three, export_list

USAGE = (
    "Usage:\n"
    "  register <name> <id> <email> <grades>\n"
    "  update-grades <name> <grades>\n"
    "  list-top-students\n"
    "  export-list csv\n"
)


def main():
    if len(sys.argv) < 2:
        print(USAGE)
        return

    cmd = sys.argv[1]

    if cmd == "register":
        if len(sys.argv) != 6:
            print("Usage: register <name> <id> <email> <grades(comma-separated)>")
            return
        name, student_id, email, grades_str = (
            sys.argv[2],
            sys.argv[3],
            sys.argv[4],
            sys.argv[5],
        )
        try:
            register_student(name, student_id, email, grades_str)
            print(f"Registered: {name}")
        except ValueError as e:
            print(f"Error: {e}")

    elif cmd == "update-grades":
        if len(sys.argv) != 4:
            print("Usage: update-grades <name> <grades>")
            return
        update_grades(sys.argv[2], sys.argv[3])
        print("Grades updated.")

    elif cmd == "list-top-students":
        list_top_three()

    elif cmd == "export-list":
        export_list()

    else:
        print("Unknown command")


if __name__ == "__main__":
    main()
