from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import Customer, db, User
from flask_login import login_user, logout_user
from forms.login_form import LoginForm

#Logging in blueprint and functionality
login_bp = Blueprint('login', __name__)


#route for logging in
@login_bp.route('/login', methods=['POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(Username=form.username.data).first()
        if user and user.check_password(form.password.data):  # Adjust this check based on your model
            login_user(user)
            # Redirect to the next page or dashboard after successful login
            return redirect(url_for('user_interface.dashboard'))
        else:
            flash('Login unsuccessful. Please check your username and password', 'danger')
    else:
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                flash(f"{fieldName}: {err}", 'danger')
    # Redirect back to the home page (or wherever your popup is) if login fails
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
            AdminPermission = False
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
            AdminPermission = True
        )
        #using functions to hash password and generate a personal number
        admin.set_password('password')
        db.session.add(admin)
        print("initial Admin account created")
    
    db.session.commit()
    print("Initial users found. Starting application")
        