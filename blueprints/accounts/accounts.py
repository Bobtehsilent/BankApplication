from flask import Blueprint, request, render_template, jsonify,flash,redirect,url_for
from flask_login import login_required, current_user
from datetime import datetime
from models import Account, db, Customer, Transaction
from forms.account_forms import AddAccountForm, EditAccountForm, TransferForm
from forms.transaction_form import AddTransactionForm
from ..customers.customers import database_to_dict
from ..breadcrumbs import update_breadcrumb, pop_breadcrumb, clear_breadcrumb


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


@account_bp.route('/manage_accounts/<int:customer_id>')
@login_required
def manage_accounts(customer_id):
    update_breadcrumb('Manage Account', url_for('account.manage_accounts', customer_id=customer_id))
    add_account_form = AddAccountForm()
    add_transaction_form = AddTransactionForm()
    customer = Customer.query.get_or_404(customer_id) 
    accounts = customer.Accounts  
    return render_template('accounts/manage_accounts.html', add_transaction_form=add_transaction_form, add_account_form=add_account_form, customer=customer, accounts=accounts, current_user=current_user)

@account_bp.route('/account_handling/<int:customer_id>/<int:account_id>', methods=['GET', 'POST'])
@login_required
def account_handling(account_id, customer_id):
    update_breadcrumb('Account Handling', url_for('account.account_handling', account_id=account_id,customer_id=customer_id))
    account = Account.query.get_or_404(account_id)
    transfer_form = TransferForm()
    eligible_accounts = Account.query.filter(Account.CustomerId == account.CustomerId, Account.Id != account_id).all()
    transfer_form.to_account.choices = [(acc.Id, f'{acc.AccountType} - {acc.Id}') for acc in eligible_accounts]

    edit_account_form = EditAccountForm(obj=account)
    # Populate forms and handle submissions as needed
    return render_template('/accounts/account_handling.html', account=account, transfer_form=transfer_form, edit_account_form=edit_account_form)

@account_bp.route('/add_account/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def add_account(customer_id):
    form = AddAccountForm()
    if form.validate_on_submit():
        balance = form.balance.data if form.balance.data is not None else 0
        new_account = Account(
            AccountType=form.account_type.data,
            Balance=balance,
            CustomerId=customer_id,
            Created=datetime.utcnow()
        )
        db.session.add(new_account)
        db.session.commit()
        flash('Account added successfully!', 'success')
        return redirect(url_for('customer.customer_detail', user_id=customer_id))
    # If the form is not submitted or validation fails
    return render_template('customers/customer_detail.html', form=form, customer_id=customer_id)


@account_bp.route('/edit_account/<int:account_id>', methods=['GET', 'POST'])
@login_required
def edit_account(account_id):
    account = Account.query.get_or_404(account_id)
    form = EditAccountForm(obj=account)
    if form.validate_on_submit():
        account.AccountType = form.account_type.data
        db.session.commit()
        flash('Account updated successfully.', 'success')
        return redirect(url_for('account.manage_accounts', customer_id=account.CustomerId))
    return render_template('account_handling.html', account=account, edit_account_form=form)

@account_bp.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    data = request.get_json()
    account_id = data.get('account_id')
    confirm_text = data.get('confirm_text')

    if confirm_text != "CONFIRM":
        return jsonify({'message': 'Confirmation failed. Account not deleted.'}), 400

    account = Account.query.get(account_id)
    if not account:
        return jsonify({'message': 'Account not found'}), 404

    if account.Balance > 0:
        return jsonify({'message': 'Cannot delete account with a balance.'}), 400

    # Delete all transactions associated with this account
    Transaction.query.filter_by(AccountId=account_id).delete()

    db.session.delete(account)
    db.session.commit()
    return jsonify({'message': 'Account deleted successfully'}), 200

    

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

    