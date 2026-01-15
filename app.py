from flask import Flask, jsonify, request , redirect, render_template 
from models import db, Admin, Doctor, Patient, Department, Appointment, Treatment  # Importing the model after db is initialized
from flask_migrate import Migrate
from forms import RegisterForm
from werkzeug.security import generate_password_hash
app = Flask(__name__)


# App configuration 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///HospitalData.db' #Tells Flask where DB is stored
app.config['SECRET_KEY'] = 'ABCD123'


# Initializing the database with the Flask app
db.init_app(app)
migrate = Migrate(app, db)
with app.app_context(): #Temporarily activate Flask’s application environment so SQLAlchemy can access the app configuration (like the database URI).”
    db.create_all() # it will create database for each model or classes in sqlite/mysql/postgresql


# Define routes here 
@app.route('/') 
def home():
    return render_template('./index.html')

#registering route 
@app.route('/registerP', methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
         
        password_hased = generate_password_hash(form.pat_password.data)

        if Patient.query.filter_by(pat_email=form.pat_email.data).first():
            return "User already exist"
        patient = Patient(pat_name=form.pat_name.data, pat_age=form.pat_age.data, pat_email=form.pat_email.data, pat_phone=form.pat_phone.data, pat_password=password_hased)
        db.session.add(patient)
        db.session.commit()
        return "you have regidte successfully"
    
    return render_template("./auth/register.html", form=form)


'''
@app.route('/datacheckup')
def datacheckup():
    admin = Admin.query.all()
    admin_list = [{"id": a.id, "name": a.name, "email": a.email} for a in admin]
     
    doctor = Doctor.query.all()
    doctor_list=[]
    for d in doctor:
        doctor_list.append({'id':d.id, 'doc_name':d.doc_name, 'speciality':d.speciality,'phone':d.doc_phone,'department_id':d.department_id})
        
    return jsonify({"admins": admin_list ,"doctors": doctor_list})
'''
if __name__ == '__main__':
    app.run(debug=True)




