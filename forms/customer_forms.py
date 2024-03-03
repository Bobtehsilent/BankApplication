from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, DateField, SelectField, HiddenField
from wtforms.validators import DataRequired, Email

class AddCustomerForm(FlaskForm):
    givenname = StringField('Given Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    telephone = StringField('Telephone')
    address = StringField('Address')
    city = StringField('City')
    zipcode = StringField('Zipcode')
    country = SelectField('Country', choices=[], validators=[DataRequired()]) 
    birthday = DateField('Birthday', format='%Y-%m-%d', validators=[DataRequired()])
    personalnumber_last4 = StringField('Last 4 digits of Personal Number', validators=[DataRequired()])
    submit = SubmitField('Submit Add')

class EditCustomerForm(FlaskForm):
    id = HiddenField() 
    givenname = StringField('Given Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    telephone = StringField('Telephone')
    address = StringField('Address')
    city = StringField('City')
    zipcode = StringField('Zipcode')
    country = SelectField('Country', choices=[], validators=[DataRequired()])
    birthday = DateField('Birthday', format='%Y-%m-%d', validators=[DataRequired()])
    personalnumber_last4 = StringField('Last 4 digits of Personal Number', validators=[DataRequired()])
    submit = SubmitField('Submit Edit') 
