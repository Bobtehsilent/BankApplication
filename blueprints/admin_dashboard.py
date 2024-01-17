from flask import Blueprint, jsonify, render_template, request
from sqlalchemy.sql import func
from models import Customer, Account, db


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard')
def dashboard():
    customer_count = Customer.query.count()
    account_count = Account.query.count()
    total_balance = db.session.query(db.func.sum(Account.Balance)).scalar()
    country_counts = db.session.query(
        Customer.CountryCode, func.count(Customer.Id)
    ).group_by(Customer.CountryCode).all()
    customer_data = {country_code: count for country_code, count in country_counts}
    country_customer_data = {}
    for country_code, _ in country_counts:
        customers = Customer.query.filter_by(CountryCode=country_code).all()
        customer_list = [{'name': c.GivenName, 'email': c.EmailAddress} for c in customers]
        country_customer_data[country_code] = customer_list

    return render_template('admin_dashboard.html', 
                           customer_data=customer_data, 
                           country_customer_data=country_customer_data, 
                           customer_count=customer_count, 
                           account_count=account_count, 
                           total_balance=total_balance)

@admin_bp.route('/get-customers-for-country')
def get_customers_for_country():
    country_code = request.args.get('country_code')
    try:
        # Fetch customers for the country
        customers = Customer.query.filter_by(CountryCode=country_code).all()
        customer_data = [{'name': customer.GivenName, 'email': customer.EmailAddress} for customer in customers]
        return jsonify({"countryName": country_code, "customers": customer_data})
    except Exception as e:
        # Log the exception for debugging
        print(e)
        # Return a server error response
        return jsonify({"error": "Server error"}), 500
