from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import Customer
from werkzeug.security import check_password_hash, generate_password_hash

#Logging in blueprint and functionality
login_bp = Blueprint('login', __name__)


#route for login stuff
@login_bp.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = Customer.query.filter_by(EmailAddress=username).first()

    if user and user.password == password:
        if is_admin == 'Admin':
            return render_template('index_admin.html')
        if is_admin == 'Customer':
            return render_template('index_user.html')
        else:
            flash("Login failure, try again")
        
    
    #Handle login failure
            
def hash_password():
    # When creating a new user
    hashed_password = generate_password_hash('plain_text_password')

    # When checking a password
    check_password_hash(hashed_password, 'plain_text_password')