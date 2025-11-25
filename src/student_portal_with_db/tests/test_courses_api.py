import unittest
from student_portal import create_app, db
from student_portal.models import Course

class CoursesAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # 1) GET empty
    def test_list_courses_empty(self):
        resp = self.client.get("/api/courses")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json(), [])

    # 2) POST success
    def test_create_course_success(self):
        resp = self.client.post("/api/courses", json={"name": "Math"})
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertEqual(data["name"], "Math")

    # 3) POST validation (missing name)
    def test_create_course_missing_name(self):
        resp = self.client.post("/api/courses", json={})
        self.assertEqual(resp.status_code, 400)
        self.assertIn("Missing 'name'", resp.get_json()["error"])

    # 4) PUT success (update)
    def test_update_course_success(self):
        with self.app.app_context():
            c = Course(name="Old")
            db.session.add(c); db.session.commit()
            cid = c.id

        resp = self.client.put(f"/api/courses/{cid}", json={"name": "New"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["name"], "New")

    # 5) DELETE success
    def test_delete_course_success(self):
        with self.app.app_context():
            c = Course(name="ToDelete")
            db.session.add(c); db.session.commit()
            cid = c.id

        resp = self.client.delete(f"/api/courses/{cid}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json(), {"message": "Deleted"})

if __name__ == "__main__":
    unittest.main()
