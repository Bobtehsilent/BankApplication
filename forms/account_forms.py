from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, NumberRange

class AddAccountForm(FlaskForm):
    account_type = SelectField('Account Type', choices=[('Savings', 'Savings'), ('Personal', 'Personal'), ('Checking', 'Checking')], validators=[DataRequired()])
    balance = DecimalField('Initial Balance', validators=[NumberRange(min=0, max=500, message="Balance must be between $0 and $500")], default=0)
    submit = SubmitField('Add Account')

class EditAccountForm(FlaskForm):
    account_type = SelectField('Account Type', choices=[('Savings', 'Savings'), ('Personal', 'Personal'), ('Checking', 'Checking')], validators=[DataRequired()])
    submit = SubmitField('Update Account')

class TransferForm(FlaskForm):
    to_account = SelectField('To Account', coerce=int, validators=[DataRequired()])
    amount = DecimalField('Amount', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Transfer')

class CustomerTransferForm(FlaskForm):
    to_account = SelectField('To Account', coerce=int, validators=[DataRequired()])
    amount = DecimalField('Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    submit = SubmitField('Transfer')