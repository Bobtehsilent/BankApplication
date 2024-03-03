from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, SubmitField, RadioField
from wtforms.validators import DataRequired, NumberRange


class AddTransactionForm(FlaskForm):
    operation_choices = [
        ('Deposit cash', 'Deposit cash'), ('Salary', 'Salary'), ('Transfer to', 'Transfer to'),
        ('ATM withdrawal', 'ATM withdrawal'), ('Payment', 'Payment'), ('Bank withdrawal', 'Bank withdrawal'), ('Transfer from', 'Transfer from')
    ]
    operation = SelectField('Operation', choices=operation_choices)
    amount = DecimalField('Amount', validators=[DataRequired(), NumberRange(min=-999999, max=999999)], places=2)
    submit = SubmitField('Submit')