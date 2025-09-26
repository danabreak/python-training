import pytest
from bmi_calculator import bmi_calculator


def test_bmi_valid_case1():
    assert bmi_calculator(1.80, 81) == 25.0


def test_bmi_valid_case2():
    assert bmi_calculator(1.65, 60) == 22.04


def test_bmi_invalid_height():
    with pytest.raises(ValueError):
        bmi_calculator(0, 70)


def test_bmi_invalid_weight():
    with pytest.raises(ValueError):
        bmi_calculator(1.70, -50)
