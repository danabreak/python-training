import unittest
from student_portal import create_app, db
from student_portal.models import Student, Course, User

class StudentsAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            # Add some courses
            db.session.add_all([Course(name="Math"), Course(name="Physics")])
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # -------------------
    # HELPER: create student + user
    # -------------------
    def create_student_with_user(self, name, age):
        user = User(username=f"{name.lower()}_user", role="student")
        user.set_password("123")
        db.session.add(user)
        db.session.commit()

        student = Student(name=name, age=age, user_id=user.id)
        db.session.add(student)
        db.session.commit()
        return student

    # -------------------
    # TESTS
    # -------------------

    def test_get_students_empty(self):
        response = self.client.get('/api/students')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_add_student_success(self):
        data = {
            "name": "Razan",
            "age": 20,
            "courses": ["Math", "Physics"]
        }
        response = self.client.post('/api/students', json=data)
        self.assertEqual(response.status_code, 201)

        json_data = response.get_json()
        self.assertEqual(json_data['name'], "Razan")
        self.assertEqual(json_data['age'], 20)
        self.assertListEqual(json_data['courses'], ["Math", "Physics"])

    def test_update_student(self):
        with self.app.app_context():
            student = self.create_student_with_user("Old Name", 18)
            student_id = student.id

        update_data = {"name": "Razan Updated", "age": 21, "courses": ["Physics"]}

        response = self.client.put(f'/api/students/{student_id}', json=update_data)
        self.assertEqual(response.status_code, 200)

        json_data = response.get_json()
        self.assertEqual(json_data['name'], "Razan Updated")
        self.assertEqual(json_data['age'], 21)
        self.assertListEqual(json_data['courses'], ["Physics"])

    def test_delete_student(self):
        with self.app.app_context():
            student = self.create_student_with_user("To Delete", 19)
            student_id = student.id

        response = self.client.delete(f'/api/students/{student_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Deleted"})

    def test_add_student_missing_name(self):
        response = self.client.post('/api/students', json={"age": 20})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing 'name'", response.get_json()['error'])

    def test_update_student_not_found(self):
        response = self.client.put('/api/students/999', json={"name": "X"})
        self.assertEqual(response.status_code, 404)
