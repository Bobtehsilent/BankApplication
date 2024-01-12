from flask import Blueprint, request, render_template
from datetime import datetime
from models import Account, db

account_bp = Blueprint('account', __name__)

@account_bp.route('/accounts')
def account_dashboard():
    # Logic ro fetch account data
    return render_template('account_dashboard.html')

@account_bp.route('/add_account', methods=['POST'])
def add_account():
    AccounType = request.form['account_type']
    Created = datetime.today()
    Balance = request.form['balance']

@account_bp.route('/accounts/<int:id>', methods=['GET'])
def get_accounts(id):
    account = Account.query.get_or_404(id)
    return render_template('account_detail.html', account=account)

@account_bp.route('/account/update/<int:id>', methods=['POST'])
def update_account(id):
    accounts = Account.query.get_or_404(id)
    accounts.AccountType = request.form['new_type']
    accounts.Created = request.form['new_creation_date']
    accounts.Balance = request.form['new_start_balance']

    db.session.commit()
    return 'Account updated successfully'

@account_bp.route('/accounts/delete/<int:id>', methods=['POST'])
def delete_account(id):
    account = Account.query.get_or_404(id)
    db.session.delete(account)
    db.session.commit()
    return 'ACcount deleted successfully'

@account_bp.route('/account/update_balance/<int:id>', methods=['POST'])
def update_balance(id):
    pass
    