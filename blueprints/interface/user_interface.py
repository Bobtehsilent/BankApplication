from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required
from sqlalchemy.sql import func
from models import Customer, Account, db
from ..customers.customers import customer_to_dict


interface_bp = Blueprint('user_interface', __name__)


@interface_bp.route('/interface')
@login_required
def dashboard():
    customer_count = Customer.query.count()
    account_count = Account.query.count()
    total_balance = db.session.query(db.func.sum(Account.Balance)).scalar()
    country_counts = db.session.query(Customer.CountryCode, func.count(Customer.Id)).group_by(Customer.CountryCode).all()
    customer_data = {country_code: count for country_code, count in country_counts}

    country_customer_data = get_top_customers_by_country()

    return render_template('/interface/user_interface.html', 
                           customer_data=customer_data, 
                           country_customer_data=country_customer_data, 
                           customer_count=customer_count, 
                           account_count=account_count,
                           total_balance=total_balance)


def get_top_customers_by_country():
    # This dictionary will hold country codes as keys and lists of top 5 customers as values
    country_top_customers = {}

    # Get a distinct list of country codes from the customers
    country_codes = db.session.query(Customer.CountryCode).distinct().all()

    for country_code_tuple in country_codes:
        country_code = country_code_tuple[0]

        # Fetch top 5 customers by total balance in accounts for each country
        top_customers = db.session.query(
            Customer.Id,
            Customer.GivenName,
            Customer.Surname,
            Customer.PersonalNumber,
            Customer.Streetaddress,
            Customer.City,
            func.sum(Account.Balance).label('total_balance')
        ).join(Account).filter(Customer.CountryCode == country_code) \
         .group_by(Customer.Id) \
         .order_by(func.sum(Account.Balance).desc()) \
         .limit(5).all()

        # Convert query results to a more friendly format (list of dicts)
        top_customers_data = [{
            'id': customer.Id,
            'personalnumber': customer.PersonalNumber,
            'name': customer.GivenName,
            'lastname': customer.Surname,
            'address': customer.Streetaddress,
            'city': customer.City,
            'total_balance': customer.total_balance
        } for customer in top_customers]

        country_top_customers[country_code] = top_customers_data
    print("Loaded")

    return country_top_customers
    

