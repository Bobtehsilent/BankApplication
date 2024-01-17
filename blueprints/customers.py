from flask import Blueprint, request, render_template
from models import Customer, db

customer_bp = Blueprint('customer', __name__, url_prefix='/customers')

@customer_bp.route('/')
def customer_list():
    page = request.args.get('page', 1, type=int)
    paginated_customers = Customer.query.paginate(page, per_page=20, error_out=False)

    return render_template('customers.html', customers=paginated_customers)

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