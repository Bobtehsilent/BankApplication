from models import Customer, db

country_code = 'SE'
customers = Customer.query.filter_by(CountryCode=country_code).all()
print(customers)