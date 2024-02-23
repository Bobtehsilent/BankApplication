from flask import render_template, redirect, url_for, flash, Blueprint
from forms.login_form import RegisterForm  # Adjust the import path as necessary
from models import User, db
from flask_login import current_user

admin_tools_bp = Blueprint('admin_tools', __name__)

@admin_tools_bp.route('/manage_user', methods=['GET', 'POST'])
def manage_user():
    if not current_user.is_authenticated or current_user.Role != 'Admin':
        # Redirect non-admin users
        return redirect(url_for('main.homepage'))
        
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            Username=form.username.data,
            Password=form.password.data,  # Make sure to hash the password
            CompanyEmail=form.email.data,
            FirstName=form.first_name.data,
            LastName=form.last_name.data,
            Role=form.role.data,
            InformationPermission=form.information_permission.data,
            ManagementPermission=form.management_permission.data,
            AdminPermission=form.admin_permission.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('New user has been successfully registered.', 'success')
        return redirect(url_for('admin_tools.manage_user'))
    return render_template('/admin/manage_user.html', form=form)