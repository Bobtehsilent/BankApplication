from flask import Blueprint, request, render_template, jsonify
from models import db, Transaction, Account
from datetime import datetime, timedelta

transactions_bp = Blueprint('transaction', __name__)

@transactions_bp.route('/add_transaction', methods=['POST'])
def add_transaction():
    try:
        Type = request.form['tran_type']
        Operation = request.form['tran_operation']
        Date = request.form['tran_date']
        Amount = request.form['tran_amount']
        NewBalance = request.form['new_balance']
        #maybe add a account id must be sent with the by other means.
        AccountId = request.form['account_id']

        new_transaction = Transaction(
            Type=Type, Operation=Operation, Date=Date, Amount=Amount, NewBalance=NewBalance, AccountId=AccountId
        )
        
        db.session.add(new_transaction)
        db.session.commit()
        return 'Transaction added successfully', 200
    except Exception as e:
        return str(e), 400

@transactions_bp.route('/transactions/<int:id>', methods=['GET'])
def get_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    return render_template('transaction_detail.html', transaction=transaction)

@transactions_bp.route('/update_transaction/<int:id>', methods=['POST'])
def update_transaction(id):
    transaction = Transaction.query.get_or_404(id)

    transaction.Type = request.form['tran_type']
    transaction.Operation = request.form['tran_operation']
    transaction.Date = request.form['tran_date']
    transaction.Amount = request.form['tran_amount']
    transaction.NewBalance = request.form['new_balance']
    # Update AccountId if necessary

    db.session.commit()
    return "Transaction updated successfully", 200

@transactions_bp.route('/delete_transaction/<int:id>', methods=['DELETE'])
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()
    return "Transaction deleted successfully", 200

@transactions_bp.route('/graph_transactions/<int:customer_id>', methods=['GET'])
def transactions_graph(customer_id):
    account_types = request.args.getlist('account_types')
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    transactions = Transaction.query.join(Account).filter(
        Account.CustomerId == customer_id,
        Account.AccountType.in_(account_types),
        Transaction.Date.between(start_date, end_date)
    ).order_by(Transaction.Date.asc()).all()

    graph_data = [{"date": trans.Date.strftime("%Y-%m-%d"), "balance": trans.NewBalance, 'account_type': trans.Account.Type} for trans in transactions]
    return jsonify(graph_data)






