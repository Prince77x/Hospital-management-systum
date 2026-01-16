from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()

from datetime import datetime

 # Doctor model
class Doctor(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key = True, unique=True)
    doc_name = db.Column(db.String(100), nullable=False)
    speciality = db.Column(db.String(100),nullable=False)
    doc_email = db.Column(db.String(100), unique=True, nullable=False)
    doc_phone = db.Column(db.String(10), unique=True, nullable=False)
    doc_password = db.Column(db.String(16), nullable = False)

    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

# Patient model
class Patient(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key = True, unique=True)
    pat_name = db.Column(db.String(100), nullable=False)
    pat_age = db.Column(db.Integer,nullable=False)
    pat_email = db.Column(db.String(100), unique=True, nullable=False)
    pat_phone = db.Column(db.String(10), unique=True, nullable=False)
    pat_password = db.Column(db.String(16), nullable=False)

    appointments = db.relationship('Appointment', backref='patient', lazy=True)

# Department model
class Department(db.Model):
    id = db.Column(db.Integer,primary_key = True, unique=True)
    dept_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100),nullable=False)
    
    doctors = db.relationship('Doctor', backref='department', lazy=True)
    
# Appointment model
class Appointment(db.Model):
    id = db.Column(db.Integer,primary_key = True, unique=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)  

    treatments = db.relationship('Treatment', backref='appointment', lazy=True)

# Treatment model
class Treatment(db.Model):
    id = db.Column(db.Integer,primary_key = True, unique=True)
    treatment_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200),nullable=False)

    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)


# Admin model
class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
