from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import Customer, db, User
from flask_login import login_user, logout_user
from forms.login_form import LoginForm

login_bp = Blueprint('login', __name__)


#route for logging in
@login_bp.route('/login', methods=['POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(Username=form.username.data).first()
        if user and user.check_password(form.password.data): 
            login_user(user)
            return redirect(url_for('user_interface.dashboard'))
        else:
            flash('Login unsuccessful. Please check your username and password', 'danger')
    else:
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                flash(f"{fieldName}: {err}", 'danger')
    return redirect(url_for('main.homepage')) 
    
@login_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))

#check/create if there is any cashier/admin   
def create_initial_users():
    if not User.query.filter_by(Role='Cashier').first():
        cashier = User(
            Username = 'stefanholmbergcashier'  ,
            FirstName = 'stefan',
            LastName = 'holmberg',
            Role = 'Cashier',
            CompanyEmail = 'stefan.holmberg@nackademin.se',
            InformationPermission = True,
            ManagementPermission = True,
            AdminPermission = False
        )
        cashier.set_password('Hejsan123')
        db.session.add(cashier)

        print("initial Cashier account added")

    if not User.query.filter_by(Role='Admin').first():
        admin = User(
            Username = 'stefanholmbergadmin',
            FirstName = 'Stefan',
            LastName = 'Holmberg',
            Role = 'Admin',
            CompanyEmail = 'stefan.holmberg@systementor.se',
            InformationPermission = True,
            ManagementPermission = True,
            AdminPermission = True
        )
        admin.set_password('Hejsan123')
        db.session.add(admin)
        print("initial Admin account created")
    
    db.session.commit()
    print("Initial users found. Starting application")
        