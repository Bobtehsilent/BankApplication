from flask import Blueprint, request, render_template, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from models import db, Transaction, Account,Customer
from collections import defaultdict
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from forms.transaction_form import AddTransactionForm
from forms.account_forms import TransferForm
from blueprints.breadcrumbs import update_breadcrumb

transactions_bp = Blueprint('transaction', __name__)

@transactions_bp.route('/account/transaction_handling/<int:customer_id>/<int:account_id>')
@login_required
def transaction_handling(account_id, customer_id):
    update_breadcrumb('Transaction Account', url_for('transaction.transaction_handling', account_id=account_id, customer_id=customer_id))
    account = Account.query.get_or_404(account_id)
    transactions = Transaction.query.filter_by(AccountId=account.Id).all()
    add_transaction_form = AddTransactionForm()
    # Set up your forms and pass them to the template
    return render_template('/transactions/transaction_handling.html', account=account, transactions=transactions, add_transaction_form=add_transaction_form)


@transactions_bp.route('/new_transaction/<int:account_id>', methods=['GET', 'POST'])
@login_required
def add_transaction(account_id):
    account = Account.query.get_or_404(account_id)
    add_transaction_form = AddTransactionForm()

    if add_transaction_form.validate_on_submit():
        is_valid, error_message = validate_transaction(account_id, transaction_amount=add_transaction_form.amount.data)
        if not is_valid:
            flash(error_message, 'danger')
            return redirect(url_for('account.manage_accounts', customer_id=account.CustomerId, account_id=account_id))
        process_transaction(account_id, add_transaction_form.amount.data, add_transaction_form.operation.data)
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('account.manage_accounts', customer_id=account.CustomerId, account_id=account_id))

    # If not valid or it's a GET request, show the form
    return render_template('accounts/manage_accounts.html', customer_id=account.CustomerId, add_transaction_form=add_transaction_form, account=account, account_id=account_id)


def process_transaction(account_id, amount, operation):
    account = Account.query.get_or_404(account_id)
    # Determine transaction type based on the sign of the amount
    transaction_type = 'Credit' if amount >= 0 else 'Debit'
    # Directly add the amount to the account's balance (it can be negative for debit transactions)
    new_balance = account.Balance + amount
    
    # Create and save the transaction record
    transaction = Transaction(
        AccountId=account_id,
        Type=transaction_type,
        Operation=operation,
        Amount=amount,  # Keep the signed value of the amount
        NewBalance=new_balance,
        Date=datetime.utcnow()
    )
    
    account.Balance = new_balance
    db.session.add(transaction)
    db.session.commit()

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
        if transfer_funds(from_account_id, to_account_id, amount):
            flash('Transfer completed successfully.', 'success')
            return redirect(url_for('account.account_handling', customer_id=customer_id, account_id=from_account_id))
        else:
            flash('Transfer not successfull.', 'failed')
            return render_template('/accounts/account_handling.html')
    return render_template('/accounts/account_handling.html', customer_id=customer_id, form=form, from_account_id=from_account_id)
    

def transfer_funds(from_account_id, to_account_id, amount):
    from_account = Account.query.get_or_404(from_account_id)
    to_account = Account.query.get_or_404(to_account_id)
    
    if from_account.Balance < amount:
        return False, 'Insufficient funds.'
    
    process_transaction(from_account_id, -amount, f'Transfer from {from_account.Id} to {to_account.Id}')
    process_transaction(to_account_id, amount, f'Transfer to {to_account.Id} from {from_account.Id}')
    return True, 'Transfer completed successfully.'



def validate_transaction(account_id, transaction_amount=None, transaction_type=None):
    account = Account.query.get_or_404(account_id)
    if not account:
        return False, "Account not found."
    
    if transaction_amount == 0:
        return False, "Transaction amount cannot be zero."
    
    if transaction_type == 'withdraw' and transaction_amount > 0:
        return False, "Withdrawal amounts must be negative."
    
    if transaction_type == 'deposit' and transaction_amount < 0:
        return False, "Deposit amounts must be positive."
    
    if transaction_type == 'withdraw' and abs(transaction_amount) > account.Balance:
        return False, "Insufficient balance for withdrawal."

    return True, ""


#Unused for now.
@transactions_bp.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
@login_required
def delete_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    account = transaction.account

    if transaction.Type == 'Credit':
        account.Balance -= transaction.Amount
    elif transaction.Type == 'Debit':
        account.Balance += transaction.Amount
    else:
        flash('Invalid transaction type.', 'error')
        return redirect(url_for('transaction.transaction_handling', account_id=account.Id, customer_id=account.CustomerId))

    db.session.delete(transaction)
    db.session.commit()

    flash('Transaction deleted and balance updated successfully.', 'success')
    return redirect(url_for('some_redirect_target'))

def get_total_balance(customer_id):
    accounts = Account.query.filter_by(CustomerId=customer_id).all()
    total_balance = sum(account.Balance for account in accounts)
    return total_balance







