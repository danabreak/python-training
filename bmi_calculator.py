def bmi_calculator(height: float, weight: float) -> float:
    if height <= 0 or weight <= 0:
        raise ValueError("height and weight must be positive")
    else:
        bmi = round(weight / height**2, 2)
        return bmi
