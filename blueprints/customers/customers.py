from flask import Blueprint, request, render_template, jsonify, flash, redirect, url_for
from flask_login import login_required
from sqlalchemy import or_
from models import Customer, db, Transaction, Account, load_country_codes
from collections import defaultdict
from forms.customer_forms import AddCustomerForm, EditCustomerForm
from forms.account_forms import AddAccountForm
from blueprints.breadcrumbs import update_breadcrumb, pop_breadcrumb, clear_breadcrumb
from datetime import datetime

customer_bp = Blueprint('customer', __name__, url_prefix='/customers')


#list customers
@customer_bp.route('/customer_list', methods=['GET'])
@login_required
def customer_list():
    return render_template('customers/customers.html')

def database_to_dict(customers):
    return [customer_to_dict(customer) for customer in customers]

def transaction_to_dict(transaction):
    return {
        'Id': transaction.Id,
        'Type': transaction.Type,
        'Operation': transaction.Operation,
        'Date': transaction.Date.strftime("%Y-%m-%d"),
        'Amount': transaction.Amount,
        'NewBalance': transaction.NewBalance
    }

def account_to_dict(account):
    return {
        'Id': account.Id,
        'AccountType': account.AccountType,
        'Created': account.Created.strftime("%Y-%m-%d"),
        'Balance': account.Balance,
    }

def customer_to_dict(customer):
    accounts_dict = [account_to_dict(account) for account in customer.Accounts]
    grouped_accounts = group_accounts_by_type(accounts_dict)
    total_balance = sum(account['Balance'] for account in accounts_dict)
    return {
        'Id': customer.Id,
        'GivenName': customer.GivenName,
        'Surname': customer.Surname,
        'Birthday': customer.Birthday,
        'Streetaddress': customer.Streetaddress,
        'Zipcode': customer.Zipcode,
        'City': customer.City,
        'Country': customer.Country,
        'Telephone': customer.Telephone,
        'EmailAddress': customer.EmailAddress,
        'PersonalNumber': customer.PersonalNumber,
        'Accounts': accounts_dict,
        'GroupedAccounts': dict(grouped_accounts),
        'total_balance': total_balance
    }

def group_accounts_by_type(accounts):
    grouped_accounts = defaultdict(lambda: {'count': 0, 'total_balance': 0})
    for account in accounts:
        account_type = account['AccountType']
        grouped_accounts[account_type]['count'] += 1
        grouped_accounts[account_type]['total_balance'] += account['Balance']
    return grouped_accounts

#Get customer details
@customer_bp.route('/customer_detail/<int:user_id>')
@login_required
def customer_detail(user_id):
    clear_breadcrumb()
    update_breadcrumb('Customer detail', url_for('customer.customer_detail', user_id=user_id))

    form = AddAccountForm()
    customerobj = Customer.query.get_or_404(user_id)
    initial_transactions = Transaction.query.join(Account, Transaction.AccountId == Account.Id)\
                                    .join(Customer, Account.CustomerId == Customer.Id)\
                                    .filter(Customer.Id == user_id)\
                                    .order_by(Transaction.Date.desc())\
                                    .limit(20).all()
    transactions = [{
        'account_id': transaction.AccountId,
        'date': transaction.Date.strftime('%Y-%m-%d'),
        'amount': transaction.Amount,
        'type': transaction.Type,
        'operation': transaction.Operation
    } for transaction in initial_transactions]

    customer = customer_to_dict(customerobj)
    return render_template('/customers/customer_detail.html', form=form, customer=customer, transactions=transactions)


@customer_bp.route('/manage_customer')
@login_required
def manage_customer():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    edit_customer_form = EditCustomerForm()
    add_customer_form = AddCustomerForm()
    country_codes = load_country_codes('static/countrycodes/country_codes.txt')
    add_customer_form.country.choices = [(c['name'], c['name']) for c in country_codes]
    edit_customer_form.country.choices = [(c['name'], c['name']) for c in country_codes]

    paginated_customers = Customer.query.paginate(page=page, per_page=per_page)

    return render_template('/customers/manage_customer.html', 
                           customers=paginated_customers.items, 
                           add_customer_form=add_customer_form,
                           pagination=paginated_customers,
                           edit_customer_form=edit_customer_form)

@customer_bp.route('/add/customer', methods=['GET', 'POST'])
@login_required
def add_customer():
    form = AddCustomerForm()
    country_codes = load_country_codes('static/countrycodes/country_codes.txt')
    form.country.choices = [(c['name'], c['name']) for c in country_codes]

    if form.validate_on_submit():
        customer_data = process_form_data(form, country_codes)
        new_customer = create_customer(customer_data)
        create_initial_account_and_transaction(new_customer)
        
        flash('Customer added successfully!', 'success')
        return redirect(url_for('customer.manage_customer'))

    return render_template('/customers/manage_customer.html', form=form)

def process_form_data(form, country_codes):
    selected_country = form.country.data
    selected_country_code = next((c['code'] for c in country_codes if c['name'] == selected_country), None)
    selected_tel_code = next((c['tel_code'] for c in country_codes if c['name'] == selected_country), None)
    birthday_str = form.birthday.data.strftime('%Y%m%d')
    personal_number = f"{birthday_str}-{form.personalnumber_last4.data}"
    raw_telephone = form.telephone.data
    processed_telephone = f"({selected_tel_code}){raw_telephone.lstrip('0')}"
    
    return {
        'GivenName': form.givenname.data.capitalize(),
        'Surname': form.surname.data.capitalize(),
        'EmailAddress': form.email.data,
        'Birthday': form.birthday.data,
        'Telephone': processed_telephone,
        'Streetaddress': form.address.data,
        'City': form.city.data.capitalize(),
        'Zipcode': form.zipcode.data,
        'Country': form.country.data,
        'CountryCode': selected_country_code,
        'TelephoneCountryCode': selected_tel_code,
        'PersonalNumber': personal_number
    }

def create_customer(customer_data):
    new_customer = Customer(**customer_data)
    db.session.add(new_customer)
    db.session.flush()  # Flush to get the new_customer ID if needed immediately
    return new_customer

def create_initial_account_and_transaction(customer):
    base_account = Account(
        CustomerId=customer.Id,
        AccountType='Checking',
        Created=datetime.utcnow(),
        Balance=0
    )
    db.session.add(base_account)
    db.session.flush()  # Ensure account ID is generated

    base_transaction = Transaction(
        AccountId=base_account.Id,
        Amount=0,
        NewBalance=0,
        Date=datetime.utcnow(),
        Type='Initial',
        Operation='Account Opening'
    )
    db.session.add(base_transaction)
    db.session.commit()

@customer_bp.route('/edit_customer', methods=['GET', 'POST'])
@login_required
def edit_customer():
    edit_customer_form = EditCustomerForm(request.form)
    country_codes = load_country_codes('static/countrycodes/country_codes.txt')
    edit_customer_form.country.choices = [(c['name'], c['name']) for c in country_codes]
    if request.method == 'POST' and edit_customer_form.validate():
        customer_id = edit_customer_form.id.data
        customer = Customer.query.get_or_404(customer_id)
        if not customer:
            flash('Customer not found.', 'danger')
            return redirect(url_for('customer.manage_customer'))
        update_customer_data(customer, edit_customer_form)
        db.session.commit()
        flash('Customer updated successfully!', 'success')
        return redirect(url_for('customer.customer_detail', customer_id=customer_id))

        # For GET request or when the form is not validated
    return render_template('/customers/manage_customer.html', edit_customer_form=edit_customer_form)

def update_customer_data(customer, form):
    birthday_str = form.birthday.data.strftime('%Y%m%d')
    customer.GivenName = form.givenname.data
    customer.Surname = form.surname.data
    customer.EmailAddress = form.email.data
    customer.Telephone = form.telephone.data
    customer.Streetaddress = form.address.data
    customer.City = form.city.data
    customer.Zipcode = form.zipcode.data
    customer.Country = form.country.data
    customer.Birthday = form.birthday.data
    customer.PersonalNumber = f"{birthday_str}-{form.personalnumber_last4.data}"


#Deleting a customer
@customer_bp.route('/customers/delete/<int:id>', methods=['POST'])
def delete_customer():
    pass
