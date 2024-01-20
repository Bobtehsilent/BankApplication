from flask import Blueprint, request, render_template
from flask_login import login_required
from sqlalchemy import func
from datetime import datetime
from models import Account, db, Customer
from .customers import database_to_dict

account_bp = Blueprint('account', __name__)


@account_bp.route('/account_list', endpoint='account_list')
@login_required
def account_list():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    search_query = request.args.get('search', '')
    sort_column = request.args.get('sort_column', 'Surname')
    sort_order = request.args.get('sort_order', 'asc')

    query = Customer.query.join(Account)

    if search_query:
        query = query.filter(Customer.Surname.contains(search_query))

    query = query.group_by(Customer.Id)
    
    if 'page' not in request.args and 'search' not in request.args:
        if request.args.get('sort_column') == sort_column:
            sort_order = 'desc' if sort_order == 'asc' else 'asc'
    
    if sort_order == 'asc':
        query = query.order_by(getattr(Customer, sort_column).asc())
    else:
        query = query.order_by(getattr(Customer, sort_column).desc())

    paginated_customers = query.paginate(page=page, per_page=per_page, error_out=False)
    customer_account_data = database_to_dict(paginated_customers.items)
    print(customer_account_data)
    
    return render_template('accounts.html', customer_account_data=customer_account_data,
                           paginated=paginated_customers, search_query=search_query,
                           sort_column=sort_column, sort_order=sort_order)


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
    