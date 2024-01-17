from flask import Blueprint, request, render_template
from flask_login import login_required
from models import Customer, db

customer_bp = Blueprint('customer', __name__, url_prefix='/customers')

@customer_bp.route('/customer_list', endpoint='customer_list')
def customer_list():
    all_customers = [customer_to_dict(customer) for customer in Customer.query.all()]
    page = request.args.get('page', 1, type=int)
    per_page = 20
    paginated_customers = Customer.query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('customers.html', customers=paginated_customers, all_customers=all_customers)

@customer_bp.route('/customer_detail/<int:id>', methods=['GET'], endpoint='get_customer_details')
def get_customer(id):
    customer = customer.query.get_or_404(id)
    return render_template('customer_detail.html', customer=customer)

def customer_to_dict(customer):
    return {
        'Id': customer.Id,
        'GivenName': customer.GivenName,
        'Surname': customer.Surname,
        'Country': customer.Country,
        'Telephone': customer.Telephone,
        'EmailAddress': customer.EmailAddress,
        'PersonalNumber': customer.PersonalNumber
        # Add other fields as needed
    }

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


@customer_bp.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return render_template('customer_detail.html', customer=customer)

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

@customer_bp.route('/customers/delete/<int:id>', methods=['POST'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return 'Customer deleted successfully'

@customer_bp.route('/customer_count', methods=['GET'])
def customer_count():
    pass