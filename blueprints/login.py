from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import Customer
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
            return render_template('admin_dashboard.html')
        else:
            #opens the customer page
            return render_template('user_dashboard.html')
    else:
        flash("Login failure, try again")
        return redirect(url_for('main.homepage'))
        
    
    #Handle login failure
            
def hash_password():
    # When creating a new user
    hashed_password = generate_password_hash('plain_text_password')

    # When checking a password
    check_password_hash(hashed_password, 'plain_text_password')