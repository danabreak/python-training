import sys


def bmi_calculator(height: float, weight: float) -> float:
    if height <= 0 or weight <= 0:
        raise ValueError("height and weight must be positive")
    else:
        bmi = round(weight / height**2, 2)
        return bmi


def main():
    if len(sys.argv) != 3:
        print("Usage: python src/bmi_calculator.py <height_in_meters> <weight_in_kg>")
        return

    try:
        height = float(sys.argv[1])
        weight = float(sys.argv[2])
        bmi = bmi_calculator(height, weight)
        print(f"Your BMI is: {bmi}")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
