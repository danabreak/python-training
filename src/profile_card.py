import sys


def print_profile_card(name: str, age: str, city: str, title: str):
    print("----------------------------------")
    print("|      Name : " + name + " " * (19 - len(name)) + "|")
    print("|      Age  : " + age + " " * (19 - len(age)) + "|")
    print("|      City : " + city + " " * (19 - len(city)) + "|")
    print("|      Title: " + title + " " * (19 - len(title)) + "|")
    print("----------------------------------")


def main():
    if len(sys.argv) != 5:
        print("Usage: python src/profile_card.py <name> <age> <city> <title>")
        return

    name, age, city, title = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    print_profile_card(name, age, city, title)


if __name__ == "__main__":
    main()
