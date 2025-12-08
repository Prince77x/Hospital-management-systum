from flask import Flask, jsonify, request , redirect, render_template 
from circular import db  # Importing the db instance from circular.py
from models import Admin, Doctor, Patient, Department, Appointment, Treatment  # Importing the model after db is initialized

app = Flask(__name__)
# Configure the database URI (example uses SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///HospitalData.db' #Tells Flask where DB is stored

# Initializing the database with the Flask app
db.init_app(app)

 
@app.route('/') 
def home():
    return render_template('./index.html')

@app.route('/datacheckup')
def datacheckup():
    admin = Admin.query.all()
    admin_list = [{"id": a.id, "name": a.name, "email": a.email} for a in admin]
     
    doctor = Doctor.query.all()
    doctor_list=[]
    for d in doctor:
        doctor_list.append({'id':d.id, 'doc_name':d.doc_name, 'speciality':d.speciality,'phone':d.doc_phone,'department_id':d.department_id})
        
    return jsonify({"admins": admin_list ,"doctors": doctor_list})

if __name__ == '__main__':
    with app.app_context(): #Temporarily activate Flask’s application environment so SQLAlchemy can access the app configuration (like the database URI).”
        db.create_all() # it will create database for each model or classes in sqlite/mysql/postgresql
    app.run(debug=True)




