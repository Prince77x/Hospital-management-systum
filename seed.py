from app import app
from models import db, Admin
from werkzeug.security import generate_password_hash

with app.app_context():

    # seed Admin
    if not Admin.query.first():

        admin1 = Admin(name="admin1", email="admin1@gmail.com", password=generate_password_hash("admin123"))
        admin2 = Admin(name="admin2", email="admin2@gmail.com", password=generate_password_hash("admin231"))

        db.session.add_all([admin1, admin2])
        db.session.commit()
        print("Admin data seeded.")

