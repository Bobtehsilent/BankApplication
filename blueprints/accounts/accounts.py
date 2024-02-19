from flask import Blueprint, request, render_template, jsonify
from flask_login import login_required
from sqlalchemy import func
from datetime import datetime
from models import Account, db, Customer
from ..customers.customers import database_to_dict

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

    if sort_order == 'asc':
        query = query.order_by(getattr(Customer, sort_column).asc())
    else:
        query = query.order_by(getattr(Customer, sort_column).desc())

    if request.args.get('ajax', '0') == '1':
        paginated_customers = query.paginate(page=page, per_page=per_page, error_out=False)
        customer_account_data = database_to_dict(paginated_customers.items)
        print(customer_account_data)
        return jsonify({
            'customers': customer_account_data,
            'pagination': {
                'total_pages': paginated_customers.pages,
                'current_page': paginated_customers.page,
                'has_prev': paginated_customers.has_prev,
                'has_next': paginated_customers.has_next,
                'prev_num': paginated_customers.prev_num if paginated_customers.has_prev else None,
                'next_num': paginated_customers.next_num if paginated_customers.has_next else None,
            }
        })
    else:    
        paginated_customers = query.paginate(page=page, per_page=per_page, error_out=False)
        customer_account_data = database_to_dict(paginated_customers.items)
        return render_template('accounts/accounts.html', customer_account_data=customer_account_data,
                            paginated=paginated_customers, search_query=search_query,
                            sort_column=sort_column, sort_order=sort_order)


# @account_bp.route('/accounts')
# def account_dashboard():
#     # Logic ro fetch account data
#     return render_template('account_dashboard.html')

@account_bp.route('/manage_accounts/<int:customer_id>')
@login_required
def manage_accounts(customer_id):
    # Fetch the customer and their accounts, display management options
    customer = Customer.query.get_or_404(customer_id)
    accounts = Account.query.filter_by(CustomerId=customer_id).all()
    return render_template('manage_accounts.html', customer=customer, accounts=accounts)

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
    return 'Account deleted successfully'

@account_bp.route('/account/update_balance/<int:id>', methods=['POST'])
def update_balance(id):
    pass
    