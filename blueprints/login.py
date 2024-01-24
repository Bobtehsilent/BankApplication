from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import Customer, db, User
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

#Logging in blueprint and functionality
login_bp = Blueprint('login', __name__)


#route for logging in
@login_bp.route('/login', methods=['POST'])
def login():
    try:
        #login form
        username = request.form['username']
        password = request.form['password']
        print(password)
        user = User.query.filter_by(Username=username).first()
        print(user.Username)
        print(user.Password)
        #check if the user is admin or customer
        if user and user.check_password(password):
            login_user(user)
            print('logging in!')
            return redirect(url_for('user_interface.dashboard'))
        else:
            flash("Login failure, try again")
            return redirect(url_for('main.homepage'))
    except:
        flash("Login failure, try again")
        return redirect(url_for('main.homepage'))
    
@login_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))

#check/create if there is any cashier/admin   
def create_initial_users():
    #Check if there is atleast one cashier
    if not User.query.filter_by(Role='Cashier').first():
        cashier = User(
            Username = 'cashiertest'  ,
            Password = 'password',
            FirstName = 'Keso',
            LastName = 'Oboy',
            Role = 'Cashier',
            CompanyEmail = 'keso.oboy@test.com',
            InformationPermission = True,
            ManagementPermission = True,
            #to be added later i guess
            PlaceholderPermission = False
        )
        cashier.set_password('password')
        db.session.add(cashier)

        print("initial Cashier account added")

    #check if there is atleast one customer
    if not User.query.filter_by(Role='Admin').first():
        admin = User(
            Username = 'admintest',
            Password = 'password',
            FirstName = 'Joakim',
            LastName = 'Norborg',
            Role = 'Admin',
            CompanyEmail = 'joakim.norborg@test.com',
            # Permissions
            InformationPermission = True,
            ManagementPermission = True,
            #to be added later i guess
            PlaceholderPermission = True
        )
        #using functions to hash password and generate a personal number
        admin.set_password('password')
        db.session.add(admin)
        print("initial Admin account created")
    
    db.session.commit()
    print("Initial users found. Starting application")
        