from .utils import load_contacts, save_contacts


def add_contact(name, phone, email, city, age):
    contact_book = load_contacts()
    contact_book[name] = {
        "phone": phone,
        "email": email,
        "city": city,
        "age": age,
    }
    save_contacts(contact_book)
    return contact_book[name]


def get_by_name(name):
    contact_book = load_contacts()
    info = contact_book.get(name)
    if info is None:
        print("Not found")
        return None
    else:
        print(info)
        return info


def search_by_phone(phone):
    contact_book = load_contacts()
    for name, info in contact_book.items():
        if info.get("phone") == phone:
            print(name + ":", info)
            return info
    print("Not found")
    return None


def list_all():
    contact_book = load_contacts()
    if not contact_book:
        print("No contacts")
        return {}
    for name, info in contact_book.items():
        print(
            f'{name}: phone={info.get("phone")}, email={info.get("email")}, '
            f'city={info.get("city")}, age={info.get("age")}'
        )
    return contact_book
