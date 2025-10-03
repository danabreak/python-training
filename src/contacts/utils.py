import json


def load_contacts(filename="contacts.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_contacts(contacts, filename="contacts.json"):
    with open(filename, "w") as f:
        json.dump(contacts, f, indent=4)
