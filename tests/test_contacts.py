# tests/test_contacts.py
from contacts.manager import add_contact, get_by_name, search_by_phone, list_all
import os


def setup_module(module):
    if os.path.exists("contacts_test.json"):
        os.remove("contacts_test.json")


def test_add_and_get():
    add_contact("Dana", "0599", "dana@mail.com", "Nablus", "22")
    result = get_by_name("Dana")
    assert result["city"] == "Nablus"
    assert result["age"] == "22"


def test_search_by_phone():
    add_contact("Ali", "1234", "ali@mail.com", "Ramallah", "30")
    result = search_by_phone("1234")
    assert result["email"] == "ali@mail.com"
    not_found = search_by_phone("9999")
    assert not_found is None


def test_list_all():
    add_contact("B", "2222", "b@mail.com", "Hebron", "25")
    all_contacts = list_all()
    assert "B" in all_contacts
    assert isinstance(all_contacts, dict)
