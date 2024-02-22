from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class AddTransactionForm(FlaskForm):
    transaction_type = SelectField('Transaction Type', choices=[('Credit', 'Credit'), ('Debit', 'Debit')])
    operation = SelectField('Operation', choices=[]) 
    amount = DecimalField('Amount', validators=[DataRequired(), NumberRange(min=0.01)], places=2)
    submit = SubmitField('Submit')

class TransferForm(FlaskForm):
    to_account = SelectField('To Account', coerce=int, validators=[DataRequired()])
    amount = IntegerField('Amount', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Transfer')
