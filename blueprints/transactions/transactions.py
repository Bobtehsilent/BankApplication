from flask import Blueprint, request, render_template, jsonify
from models import db, Transaction, Account
from collections import defaultdict
from datetime import datetime

transactions_bp = Blueprint('transaction', __name__)

def add_transaction(account_id, transaction_type, amount):
    try:
        # Fetch the account
        account = Account.query.get(account_id)
        if not account:
            raise ValueError("Account not found")

        # Prepare to calculate the new balance
        new_balance = account.Balance + amount if transaction_type == "Credit" else account.Balance - amount

        # Check for overdraft scenario and handle accordingly
        if transaction_type == "Debit" and new_balance < 0:
            # Calculate overdraft amount
            overdraft_amount = abs(new_balance)
            
            # Find or create a debt account for the customer
            debt_account = Account.query.filter_by(CustomerId=account.CustomerId, AccountType="Debt").first()
            if not debt_account:
                debt_account = Account(
                    AccountType="Debt",
                    Balance=0,
                    Created=datetime.now(),
                    CustomerId=account.CustomerId
                )
                db.session.add(debt_account)
            
            # Add the overdraft amount to the debt account
            debt_account.Balance += overdraft_amount
            new_balance = 0  # Optionally reset the original account's balance to 0 if overdraft is fully transferred

        # Update the account's balance
        account.Balance = new_balance

        # Create the transaction
        transaction = Transaction(
            AccountId=account_id,
            Type=transaction_type,
            Amount=amount,
            NewBalance=account.Balance,  # Use the updated account balance
            Date=datetime.now()
        )

        # Save the transaction and account updates
        db.session.add(transaction)
        db.session.commit()

    except Exception as e:
        db.session.rollback()  # Ensure to roll back on error
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

def get_total_balance(customer_id):
    accounts = Account.query.filter_by(CustomerId=customer_id).all()
    total_balance = sum(account.Balance for account in accounts)
    return total_balance

@transactions_bp.route('/graph_transactions/<int:customer_id>', methods=['GET'])
def transactions_graph(customer_id):
    transactions = Transaction.query.join(Account).filter(
        Account.CustomerId == customer_id
    ).order_by(Transaction.Date.asc()).all()  # Note: Removed limit here to process all transactions
    
    # Prepare data structure to hold cumulative balance by account type
    balances_by_type = defaultdict(list)
    
    # Track running balances for each account type
    running_balances = defaultdict(int)

    for transaction in transactions:
        # Assuming each transaction affects the balance according to its type
        if transaction.Type == "Debit":
            running_balances[transaction.Account.AccountType] += transaction.Amount
        else:  # Debit
            running_balances[transaction.Account.AccountType] -= transaction.Amount
        
        # Append the current running balance for this account type
        balances_by_type[transaction.Account.AccountType].append({
            "date": transaction.Date.strftime("%Y-%m-%d"),
            "cumulative_balance": running_balances[transaction.Account.AccountType]
        })

    return jsonify(balances_by_type)






