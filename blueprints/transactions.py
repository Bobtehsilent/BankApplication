from flask import Blueprint, request, render_template
from models import db, Transaction

transactions_bp = Blueprint('transaction', __name__)

@transactions_bp.route('/add_transaction', methods=['POST'])
def add_transaction():
    Type = request.form['tran_type']
    Operation = request.form['tran_operation']
    Date = request.form['tran_date']
    Amount = request.form['tran_amount']
    NewBalance = request.form['new_balance']

    new_transaction = Transaction(
        Type=Type, Operation=Operation, Date=Date, Amount=Amount, NewBalance=NewBalance
    )
    
    db.session.add(new_transaction)
    db.session.commit()

@transactions_bp.route('/transactions/<int:id>', methods=['GET'])
def get_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    return render_template('transaction_detail.html', transaction=transaction)

