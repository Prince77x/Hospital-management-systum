from flask import Flask, jsonify, request , redirect, render_template, url_for,flash,abort
from models import db, Admin, Doctor, Patient, Department, Appointment, Treatment  # Importing the model after db is initialized
from flask_migrate import Migrate
from forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
app = Flask(__name__)

# flask_login configuration 
loginmanager = LoginManager()
loginmanager.init_app(app)
loginmanager.login_view = "patient_login"

# App configuration 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///HospitalData.db' #Tells Flask where DB is stored
app.config['SECRET_KEY'] = 'ABCD123'


# Initializing the database with the Flask app
db.init_app(app)
migrate = Migrate(app, db)
with app.app_context(): #Temporarily activate Flask’s application environment so SQLAlchemy can access the app configuration (like the database URI).”
    db.create_all() # it will create database for each model or classes in sqlite/mysql/postgresql

# user loader 
@loginmanager.user_loader
def load_user(user_id):
     return (
         Admin.query.get(int(user_id)) or
         Doctor.query.get(int(user_id)) or 
         Patient.query.get(int(user_id))
         
     )

# Define routes here 
@app.route('/') 
def home():
    return render_template('./index.html')

#registering route 
@app.route('/register', methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
         
        password_hased = generate_password_hash(form.pat_password.data)

        if Patient.query.filter_by(pat_email=form.pat_email.data).first():
            return "User already exist"
        patient = Patient(pat_name=form.pat_name.data, pat_age=form.pat_age.data, pat_email=form.pat_email.data, pat_phone=form.pat_phone.data, pat_password=password_hased)
        db.session.add(patient)
        db.session.commit()
        login_user(patient)
        flash("You have registered and logged in successfully")
        return redirect(url_for('patient_dashboard'))
    
    return render_template("register.html", form=form)

@app.route('/patient/login',methods=["GET","POST"])
def patient_login():
    form = LoginForm()
    if form.validate_on_submit():

        patient = Patient.query.filter_by(pat_email= form.username.data).first()
        if patient and check_password_hash(patient.pat_password, form.password.data):
            login_user(patient)
            flash("You have logged in successfully")
            return redirect(url_for('patient_dashboard'))
        else:
            flash("Invalid credential")
            return redirect(url_for('patient_login'))
        
    return render_template('login.html', form=form)

@app.route('/admin/login', methods=["GET","POST"])
def admin_login():
    form= LoginForm()
    if form.validate_on_submit():

        admin = Admin.query.filter_by(email = form.username.data).first()
        if admin and check_password_hash(admin.password, form.password.data):
            login_user(admin)
            flash("you have logged in as admin")
            return redirect(url_for('admin_dashboard'))
        else:
            flash('invalid credential')
            return redirect(url_for('admin_login'))
    return render_template('./admin/admin_login.html', form=form)

@app.route('/doctor/login', methods=["GET","POST"])
def doctor_login():
    form= LoginForm()
    if form.validate_on_submit():

        doctor= Doctor.query.filter_by(doc_email = form.username.data).first()
        if doctor and check_password_hash(doctor.doc_password, form.password.data):
            login_user(doctor)
            flash("welcome Doctor ! you are logedin")
            return redirect(url_for('doctor_dashboard'))
        else:
            flash('Invalid credential')
            return redirect(url_for('doctor_login'))
    return render_template('./doctor/doctor_login.html' , form=form)


@app.route('/patient/dashboard')
@login_required
def patient_dashboard():
    return render_template('./patient/patient_dashboard.html')
        
@app.route('/admin/admin_dashboard')
@login_required
def admin_dashboard():
    if not isinstance(current_user, Admin):
        abort(403)
    doctors = Doctor.query.all()
    return render_template('./admin/admin_dashboard.html', admin_name=current_user.name, doctors=doctors)

@app.route('/doctor/dashboard')
@login_required
def doctor_dashboard():
    return render_template('./doctor/doctor_dashboard.html')

@app.route('/admin/add_doctor', methods=["GET","POST"])
@login_required
def add_doctor():
    if request.method == "POST":
        name = request.form.get('doc_name')
        speciality = request.form.get('speciality')
        email = request.form.get('doc_email')
        phone = request.form.get('doc_phone')
        department_id = request.form.get('department_id')
        password_hash = generate_password_hash(request.form.get('password'))

        doctor = Doctor(doc_name=name,speciality=speciality,doc_phone=phone,doc_email=email,department_id=department_id,doc_password=password_hash)

        db.session.add(doctor)
        db.session.commit()
        flash('Doctor added successfully')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('./admin/add_doctor.html')

@app.route('/admin/logout')
@login_required
def logout_admin():
    logout_user()
    flash("logout succesfully")
    return redirect(url_for("home"))


@app.route('/admin/edit_doctor/<int:doctor_id>', methods=["GET","POST"])
@login_required
def edit_doctor(doctor_id):
    if not isinstance(current_user, Admin):
        abort(403)

    doctor = Doctor.query.get_or_404(doctor_id)

    if request.method == "POST":
        doctor.doc_name = request.form.get('doc_name')
        doctor.speciality = request.form.get('speciality')
        doctor.doc_email = request.form.get('doc_email')
        doctor.doc_phone = request.form.get('doc_phone')
        doctor.department_id = request.form.get('department_id')

        db.session.commit()
        flash('Doctor updated successfully')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('./admin/edit_doctor.html',doctor=doctor)

@app.route('/admin/delete_doctor/<int:doctor_id>')
@login_required
def delete_doctor(doctor_id):
    if not isinstance(current_user, Admin):
        abort(403)
    
    doctor = Doctor.query.get_or_404(doctor_id)
    db.session.delete(doctor)
    db.session.commit()
    flash('Doctor deleted successfully')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/view_doctor/<int:doctor_id>')
@login_required
def view_doctor(doctor_id):
    if not isinstance(current_user, Admin):
        abort(403)
    
    doctor = Doctor.query.get_or_404(doctor_id)
    return render_template('./admin/view_doctor.html', doctor=doctor)







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




