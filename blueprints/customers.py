from flask import Blueprint, request, render_template
from flask_login import login_required
from datetime import datetime
from models import Customer, db, Account
from sqlalchemy.orm import joinedload
from collections import defaultdict

customer_bp = Blueprint('customer', __name__, url_prefix='/customers')


#list customers
@customer_bp.route('/customer_list', endpoint='customer_list')
@login_required
def customer_list():
    page = request.args.get('page', 1, type=int)
    per_page = 15
    search_query = request.args.get('search', '')
    sort_column = request.args.get('sort_column', 'Surname')
    sort_order = request.args.get('sort_order', 'asc')

    if 'page' not in request.args and 'search' not in request.args:
        if request.args.get('sort_column') == sort_column:
            sort_order = 'desc' if sort_order == 'asc' else 'asc'
            
    query = Customer.query.options(joinedload(Customer.Accounts).joinedload(Account.Transactions))
    if search_query:
        query = query.filter(Customer.GivenName.contains(search_query) |
                             Customer.Surname.contains(search_query) |
                             Customer.EmailAddress.contains(search_query) |
                             Customer.Country.contains(search_query)) #add more later like phone number etc
    if sort_order == 'asc':
        query = query.order_by(getattr(Customer, sort_column).asc())
    else:
        query = query.order_by(getattr(Customer, sort_column).desc())


    paginated_customers = query.paginate(page=page, per_page=per_page, error_out=False)
    customers_dict = database_to_dict(paginated_customers)
    return render_template('customers.html', customers=customers_dict, 
                           paginated=paginated_customers, 
                           sort_column=sort_column, sort_order=sort_order,
                           search_query=search_query)

#Important for the customer list page. makes the detail page work
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
        'GroupedAccounts': grouped_accounts,
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
@customer_bp.route('/customer_detail/<int:id>', methods=['GET'], endpoint='get_customer_details')
def get_customer(id):
    customer = customer.query.get_or_404(id)
    return render_template('customer_detail.html', customer=customer)

#adding customers
@customer_bp.route('/add_customer', methods=['POST'])
def add_customer():
    GivenName = request.form['first_name']
    Surname = request.form['last_name']
    Streetaddress = request.form['street_address']
    City = request.form['city']
    Zipcode = request.form['zip_code']
    Country = request.form['country']
    CountryCode = request.form['country_code']
    Birthday = request.form['irthday']
    NationalId = request.form['national_id']
    TelephoneCountryCode = request.form['telephone_country_code']
    Telephone = request.form['phone_number']
    EmailAddress = request.form['email_address']

    new_customer = Customer(
        GivenName=GivenName, Surname=Surname, Streetaddress=Streetaddress,
        City=City, Zipcode=Zipcode, Country=Country, CountryCode=CountryCode,
        Birthday=Birthday, NationalId=NationalId, TelephoneCountryCode=TelephoneCountryCode,
        Telephone=Telephone, EmailAddress=EmailAddress
    )

    db.session.add(new_customer)
    db.session.commit()

    return 'customer added successfully'

# updating customer
@customer_bp.route('/customers/update/<int:id>', methods=['POST'])
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    customer.GivenName = request.form['first_name']
    customer.Surname = request.form['last_name']
    customer.Streetaddress = request.form['street_address']
    customer.City = request.form['city']
    customer.Zipcode = request.form['zip_code']
    customer.Country = request.form['country']
    customer.CountryCode = request.form['country_code']
    customer.Birthday = request.form['birthday']
    customer.NationalId = request.form['national_id']
    customer.TelephoneCountryCode = request.form['telephone_country_code']
    customer.Telephone = request.form['phone_number']
    customer.EmailAddress = request.form['email']

    db.session.commit()
    return 'Customer updated Successfully'

#Deleting a customer
@customer_bp.route('/customers/delete/<int:id>', methods=['POST'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return 'Customer deleted successfully'

#Customer count
@customer_bp.route('/customer_count', methods=['GET'])
def customer_count():
    pass