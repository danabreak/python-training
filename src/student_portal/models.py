
students={}
index=1


def next_id():
    global index
    sid=index
    index+=1
    return sid


def add_student(name,email,location,birthdate):
    name = (name or "").strip()
    email = (email or "").strip()
    if not name:
        raise ValueError("name is required")
    if not email or "@" not in email:
        raise ValueError("valid email is required")
    


    sid=next_id()

    student = {
        "id": sid,                 
        "name": name,
        "email": email,
        "grades": [], 
        "location": location,
        "birthdate": birthdate,
    }

    students[sid]=student
    return student



def get_all_students():
    return list(students.values())


def get_student_by_id(sid):
    try:
        key = int(sid)  
    except (TypeError, ValueError):
        return None
    return students.get(key)


def add_grade(sid,grade):
    student=get_student_by_id(sid)
    if student is None:
        raise KeyError(f"student {sid} not found")
    student["grades"].append(float(grade))
    return student


    


def average_grade(sid):
    student = get_student_by_id(sid)
    if student is None:
        raise KeyError(f"student {sid} not found")

    grades = student.get("grades", [])
    if not grades:  
        return 0.0

    return sum(grades) / len(grades)


