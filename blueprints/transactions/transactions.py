from flask import Blueprint, request, render_template, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from models import db, Transaction, Account
from collections import defaultdict
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from forms.transaction_form import AddTransactionForm, TransferForm

transactions_bp = Blueprint('transaction', __name__)

@transactions_bp.route('/add_transaction/<int:account_id>', methods=['GET', 'POST'])
@login_required
def add_transaction(account_id):
    account = Account.query.get_or_404(account_id)
    form = AddTransactionForm()

    set_operation_choices(form, form.transaction_type.data)

    if form.validate_on_submit():
        # Validate the transaction
        is_valid, error_message = validate_transaction(account_id, transaction_amount=form.amount.data, transaction_type=form.transaction_type.data)
        if not is_valid:
            flash(error_message, 'danger')
            return render_template('transactions/add_transaction.html', form=form, account_id=account_id)
        
        # Process the transaction
        process_transaction(account_id, form.transaction_type.data, form.amount.data, form.operation.data)
        flash('Transaction made successfully!', 'success')
        return redirect(url_for('customer.customer_detail', user_id=account.CustomerId))
    
    return render_template('transactions/add_transaction.html', form=form, account_id=account_id)

def process_transaction(account_id, transaction_type, amount, operation):
    account = Account.query.get_or_404(account_id)
    new_balance = account.Balance + amount if transaction_type == 'Credit' else account.Balance - amount
    
    transaction = Transaction(
        AccountId=account_id,
        Type=transaction_type,
        Operation=operation,
        Amount=amount,
        NewBalance=new_balance,
        Date=datetime.utcnow()
    )
    
    account.Balance = new_balance
    db.session.add(transaction)
    db.session.commit()

def set_operation_choices(form, transaction_type):
    if transaction_type == 'Credit':
        form.operation.choices = [
            ('Deposit cash', 'Deposit cash'),
            ('Salary', 'Salary'),
            ('Transfer', 'Transfer')
        ]
    else:
        form.operation.choices = [
            ('ATM withdrawal', 'ATM withdrawal'),
            ('Payment', 'Payment'),
            ('Bank withdrawal', 'Bank withdrawal'),
            ('Transfer', 'Transfer')
        ]


@transactions_bp.route('/transfer_transaction/<int:from_account_id>', methods=['GET', 'POST'])
@login_required
def transfer_transaction(from_account_id):
    form = TransferForm()
    from_account = Account.query.get_or_404(from_account_id)  # Fetch the from account to get the CustomerId
    customer_id = from_account.CustomerId  # Retrieve CustomerId from the from account

    # Filter accounts belonging to the same customer excluding the from_account
    form.to_account.choices = [
        (account.Id, f'{account.AccountType} - {account.Id}') 
        for account in Account.query.filter(Account.CustomerId == customer_id, Account.Id != from_account_id).all()
    ]
    if form.validate_on_submit():
        amount = form.amount.data
        to_account_id = form.to_account.data
        transfer_funds(from_account_id, to_account_id, amount)
        flash('Transfer completed successfully.', 'success')
        return redirect(url_for('account.manage_accounts', customer_id=customer_id))
    print(form.errors)
    return render_template('transactions/transfer_transaction.html', form=form, from_account_id=from_account_id)

def transfer_funds(from_account_id, to_account_id, amount):
    from_account = Account.query.get_or_404(from_account_id)
    to_account = Account.query.get_or_404(to_account_id)
    
    if from_account.Balance < amount:
        flash('Insufficient funds.', 'error')
        return False
    
    from_account.Balance -= amount
    to_account.Balance += amount
    
    db.session.add(Transaction(Type='Debit', Operation=f'Transfer from {from_account.Id} to {to_account.Id}', Date=datetime.utcnow(), Amount=-amount, NewBalance=from_account.Balance, AccountId=from_account_id))
    db.session.add(Transaction(Type='Credit', Operation=f'Transfer to {to_account.Id} from {from_account.Id}', Date=datetime.utcnow(), Amount=amount, NewBalance=to_account.Balance, AccountId=to_account_id))
    
    db.session.commit()
    return True


def validate_transaction(from_account_id, to_account_id=None, transaction_amount=None, transaction_type=None):
    from_account = Account.query.get(from_account_id)
    if not from_account:
        return False, "Source account not found."
    
    if to_account_id:
        to_account = Account.query.get(to_account_id)
        if not to_account:
            return False, "Destination account not found."
    
    if transaction_amount <= 0:
        return False, "Transaction amount must be positive."
    
    if transaction_type in ['Debit', 'TransferFrom'] and transaction_amount > from_account.Balance:
        return False, "Insufficient balance in source account."

    return True, ""


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

def get_total_balance(customer_id):
    accounts = Account.query.filter_by(CustomerId=customer_id).all()
    total_balance = sum(account.Balance for account in accounts)
    return total_balance







