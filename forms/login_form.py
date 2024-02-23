from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models import User  # Adjust the import based on your application structure

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    email = StringField('Company Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, max=35),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    role = SelectField('Role', choices=[('Cashier', 'Cashier'), ('Admin', 'Admin')], validators=[DataRequired()])
    information_permission = BooleanField('Information Permission')
    management_permission = BooleanField('Management Permission')
    admin_permission = BooleanField('Admin Permission')
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(Username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(CompanyEmail=email.data).first()
        if user:
            raise ValidationError('That email is already in use. Please choose a different one.')
