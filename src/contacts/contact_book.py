import sys
from .manager import add_contact, get_by_name, search_by_phone, list_all


def main():
    if len(sys.argv) < 2:
        print("Usage: add/get/find-phone/list ...")
        return

    cmd = sys.argv[1]

    if cmd == "add":
        if len(sys.argv) != 7:
            print("Usage: add <name> <phone> <email> <city> <age>")
            return
        add_contact(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
        print(f"Added: {sys.argv[2]}")

    elif cmd == "get":
        get_by_name(sys.argv[2])

    elif cmd == "find-phone":
        search_by_phone(sys.argv[2])

    elif cmd == "list":
        list_all()

    else:
        print("Unknown command")


if __name__ == "__main__":
    main()
