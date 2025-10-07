# 🐍 Python Training Projects

This repository contains multiple mini-projects developed to practice Python programming, data structures, modular design, file I/O, and testing.  
Each project is independent and can be executed directly from the command line.


---


## 📁 Project Structure
src/
contacts/ # Contact management CLI (JSON-based)
student_management_cli/ # Student management CLI with CSV export
bmi_calculator.py # Simple BMI calculator script
grades.py # Functions for handling grades and top students
profile_card.py # Profile card generator script
tests/ # Pytest unit tests for all projects


---


## ⚙️ Setup

### 1️⃣ Create a Virtual Environment

python -m venv .

### 2️⃣ Activate It

Windows PowerShell
.venv\Scripts\Activate.ps1

macOS / Linux
source .venv/bin/

### 3️⃣ Install Dependencies

pip install pytest flake8 black


------
### 📁 Projects:


## 📇 Contacts Project

A small command-line contact book that stores, retrieves, and searches contacts in a JSON file.


🧱 Project Structure
src/
└── contacts/
    ├── contact_book.py   # CLI interface (parses sys.argv)
    ├── manager.py        # Business logic (add, get, search, list)
    └── utils.py          # JSON file load/save helpers


🧠 Features

- Add new contact.

- Search by name or phone number.

- List all contacts.

- Persistent storage in contacts.json .



▶️ Example Usage
# Add a new contact
python -m src.contacts.contact_book add "Dana" "0599" "dana@mail.com" "Nablus" "22"

# Get contact by name
python -m src.contacts.contact_book get "Dana"

# Search contact by phone number
python -m src.contacts.contact_book find-phone "0599"

# List all contacts
python -m src.contacts.contact_book list


🗂️ Data Storage

- **File:** all contacts are stored in `contacts.json`.
- **load_contacts()** → reads `contacts.json` using `json.load` ⇒ **JSON → Python dict**  
  (returns `{}` if the file doesn’t exist).
- **Operations** (add/get/find/list) read or update the in-memory **dict**.
- **save_contacts()** → writes the updated **dict** back to `contacts.json` using `json.dump` ⇒ **Python dict → JSON**.


🧠 Behind the Scenes

In memory, contacts are managed as a Python dictionary:

{
    "Dana": {
        "phone": "0599",
        "email": "dana@mail.com",
        "city": "Nablus",
        "age": "22"
    }
}


When saving, the dictionary is automatically serialized (converted) into JSON text and written to contacts.json:

{
    "Dana": {
        "phone": "0599",
        "email": "dana@mail.com",
        "city": "Nablus",
        "age": "22"
    }
}

----

## 🎓 Student Management CLI

A command-line app for managing student records with validation, averages, and export functionality.


🧩 Main Files

cli.py – handles CLI commands and user input

manager.py – contains all core logic (register, update, list, export)

utils.py – handles JSON read/write and CSV export


🧠 Features

- Register new students (name, ID, email, grades)

- Update existing student grades

- List top students by average grade

- Export student list to CSV

- Input validation and exception handling



▶️ Example Usage

# Register a new student
python -m src.student_management_cli.cli register "Lana" 5001 "lana@mail.com" "80,90,100"

# Update grades
python -m src.student_management_cli.cli update-grades "Lana" "90,95,100"

# List top students (sorted by average)
python -m src.student_management_cli.cli list-top-students

# Export students to CSV
python -m src.student_management_cli.cli export-list


🗂️ Data Storage:

- JSON file: students.json
- Export file: students_export.csv


----


## 🧮 BMI Calculator

src/bmi_calculator.py

A small utility that calculates Body Mass Index based on height and weight.

▶️ Template Usage
python src/bmi_calculator.py <height> <weight>


▶️ Example Usage
python src/bmi_calculator.py 1.70 65

Expected output:
Your BMI is: 22.49


----


## 🏅 Grades Module

src/grades.py

This module provides simple grade-related utilities:

- **get_top_three()** → returns top 3 students by grade  
- **dict_transform()** → converts numeric grades to “Pass” or “Fail”


▶️ Template Usage
# Show top three students
python src/grades.py top-three

# Transform numeric grades to Pass/Fail
python src/grades.py transform


------


## 🪪 Profile Card

src/profile_card.py

Generates a formatted profile card or summary string for a person.
Demonstrates string formatting and user input.


▶️ Template Usage
python src/profile_card.py <name> <age> <city> <title>

-----


## 🧪 Running Tests

All projects include test cases written with pytest.

Run all tests:

pytest -q


Run tests for a specific project:

pytest tests/test_student_management_cli.py -v
pytest tests/test_contacts.py -v


-------


## 🧹 Linting

To maintain clean and consistent code style:

# Check code style with flake8
flake8 src tests

# Format code automatically with black
black src tests

-------


## 🗂️ Data Files

- contacts.json – stores contact data

- students.json – stores student data

- students_export.csv – generated by Student Management CLI

These files are ignored in version control using .gitignore.


------


## 💡 Notes

- All projects are self-contained and can be run independently.

- JSON and CSV files are automatically created if missing.

- The code follows a clean modular structure, separating logic (manager.py) from data handling (utils.py).