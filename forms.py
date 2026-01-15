from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, IntegerField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, Email

class RegisterForm(FlaskForm):
    pat_name = StringField("Full Name", validators=[DataRequired(), Length(min=3, max=50)])
    pat_age = IntegerField("Patient Age", validators=[DataRequired()])
    pat_email = EmailField("Email", validators=[DataRequired(),Email()])
    pat_phone = IntegerField("Enter your Phone number:", validators=[DataRequired()])
    pat_password = PasswordField("Password",validators=[DataRequired(),Length(max=16)])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")