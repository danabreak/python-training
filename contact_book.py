import sys


contact_book = {
    "Dana": {
        "phone": "0595376282",
        "email": "danabreik2424@gmail.com",
        "city": "Nablus",
        "age": 22,
    }
}


def add_contact():
    contact_book[sys.argv[2]] = {
        "phone": sys.argv[3],
        "email": sys.argv[4],
        "city": sys.argv[5],
        "age": sys.argv[6],
    }
    print("Added :" + sys.argv[2])


def get_by_name():
    info = contact_book.get(sys.argv[2])
    if info is None:
        print("Not found")
    else:
        print(info)


def search_by_phone():
    for name, info in contact_book.items():
        if info.get("phone") == sys.argv[2]:
            print(name + ":", contact_book.get(name))
            return
    print("Not found")


def list_all():
    if not contact_book:
        print("No contacts")
        return
    for name, info in contact_book.items():
        print(
            f'{name}: phone={info.get("phone")}, email={info.get("email")}, city={info.get("city")}, age={info.get("age")}'
        )


if sys.argv[1] == "add":
    add_contact()
elif sys.argv[1] == "get":
    get_by_name()

elif sys.argv[1] == "find-phone":
    search_by_phone()

elif sys.argv[1] == "list":
    list_all()
