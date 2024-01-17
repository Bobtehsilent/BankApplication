from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import Customer, db
from werkzeug.security import check_password_hash, generate_password_hash

#Logging in blueprint and functionality
login_bp = Blueprint('login', __name__)


#route for logging in
@login_bp.route('/login', methods=['POST'])
def login():
    #login form
    username = request.form['username']
    password = request.form['password']
    user = Customer.query.filter_by(EmailAddress=username).first()

    #check if the user is admin or customer
    if user and user.check_password(password):
        if user.Role == 'Admin':
            #opens the admin page
            return redirect(url_for('admin.dashboard'))
        else:
            #opens the customer page
            return redirect(url_for('user.dashboard'))
    else:
        flash("Login failure, try again")
        return redirect(url_for('main.homepage'))

#check if there is any customers/admins for testwork        
def create_initial_users():
    #Check if there is atleast one admin
    if not Customer.query.filter_by(Role='Admin').first():
        admin = Customer(
            GivenName= 'Sebastian',
            Surname = 'Admin',
            Streetaddress = 'Slottsgatan 21',
            City = 'Västerås',
            Zipcode = '14123',
            Country = 'Sweden',
            CountryCode = '46',
            Birthday = '1990-01-01',
            Telephone = '0739025151',
            EmailAddress = 'sebastian@admin.com'          
        )
        admin.set_password('password')
        admin.set_swedish_personal_number()
        admin.Role = 'Admin'
        db.session.add(admin)

        print("initial admin account added")

    #check if there is atleast one customer
    if not Customer.query.filter_by(Role='Customer').first():
        customer = Customer(
            GivenName = 'Sebastian',
            Surname = 'Customer',
            Streetaddress = 'Slottsgatan 21',
            City = 'Västerås',
            Zipcode = '14123',
            Country = 'Sverige',
            CountryCode = '46',
            Birthday = '1990-10-21',
            Telephone = '072-232133',
            EmailAddress = 'Sebastian@customer.com'
        )
        #using functions to hash password and generate a personal number
        customer.set_password('password')
        customer.set_swedish_personal_number()
        db.session.add(customer)
        print("initial customer account added")
    
    db.session.commit()
    print("both initial accounts created.")
        