from password import strong_password, WeakPasswordError
import pytest


def test_strong_password_length_less_than_eight():
    with pytest.raises(WeakPasswordError, match="Password is too short"):
        strong_password("Dana2$")


def test_strong_password_no_uppercase():
    with pytest.raises(
        WeakPasswordError, match="Password doesn't contain an uppercase"
    ):
        strong_password("dana24#$")


def test_strong_password_no_digit():
    with pytest.raises(WeakPasswordError, match="Password doesn't contain any digit"):
        strong_password("Dana%##$")


def test_strong_password_no_special_char():
    with pytest.raises(
        WeakPasswordError, match="Password doesn't contain any special characters"
    ):
        strong_password("DanaDa22")


def test_strong_password_returns_true():
    strong = strong_password("Dana24#$")
    assert strong == True
