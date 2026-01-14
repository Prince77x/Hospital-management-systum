from app import app
from models import db, Admin, Doctor

with app.app_context():

    # seed Admin
    if not Admin.query.first(): #  it will check if there is already data in admin table or not and return none if there is no data
        admin1 = Admin(name="admin1", email="admin1@gmail.com", password="admin123")
        admin2 = Admin(name="admin2", email="admin2@gmail.com", password="admin231")

        db.session.add(admin1)
        db.session.add(admin2)

        print("Admin data seeded.")

    # seed Doctor
    if not Doctor.query.first():
        doctor1 = Doctor(doc_name="Dr. John Doe", speciality="Cardiology", doc_email="john.doe@example.com", doc_phone="1234567890", department_id=1)
        doctor2 = Doctor(doc_name="Dr. Jane Smith", speciality="Neurology", doc_email="jane.smith@example.com", doc_phone="0987654321", department_id=2)

        db.session.add(doctor1)
        db.session.add(doctor2)

        print("Doctor data seeded.")

     
     # commit the changes to the database
    db.session.commit()
    print("Database seeding completed.")