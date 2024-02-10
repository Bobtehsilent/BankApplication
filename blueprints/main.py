from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from models import Customer



main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def homepage():
    return render_template("homepage.html")


@main_bp.route('/search_customers', methods=['GET'])
def search_bar():    
    if request.args.get('ajax', 0, type=int):
        search_query = request.args.get('search', '')
        query = Customer.query
        if search_query:
            query = query.filter(Customer.GivenName.contains(search_query) |
                         Customer.Surname.contains(search_query) |
                         Customer.EmailAddress.contains(search_query) |
                         Customer.Country.contains(search_query)) \
                 .order_by(Customer.GivenName.asc(), Customer.Surname.asc())  # Sort alphabetically
        results = query.limit(15).all() 
        customers = [{'id': customer.Id, 'name': f"{customer.GivenName} {customer.Surname}"} for customer in results]
        return jsonify(customers)