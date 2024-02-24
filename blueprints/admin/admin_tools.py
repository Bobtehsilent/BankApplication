from flask import render_template, redirect, url_for, flash, Blueprint, request
from forms.login_form import RegisterForm, EditUserForm, EditUserPasswordForm
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
            Password=form.password.data,
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

@admin_tools_bp.route('/edit_user', methods=['GET', 'POST'])
def edit_user():
    form = EditUserForm(request.form)
    if request.method == 'POST' and form.validate():
        user_id = form.user_id.data
        user = User.query.get(user_id)
        if not user:
            flash('User not found.', 'danger')
            return redirect(url_for('admin_tools.manage_user'))

        # Update user details
        user.Username = form.username.data
        user.CompanyEmail = form.email.data
        user.FirstName = form.first_name.data
        user.LastName = form.last_name.data
        user.Role = form.role.data
        user.InformationPermission = form.information_permission.data
        user.ManagementPermission = form.management_permission.data
        user.AdminPermission = form.admin_permission.data

        db.session.commit()
        flash('User updated successfully.', 'success')
        return redirect(url_for('admin_tools.manage_user'))

    # For GET request or initial page load
    return render_template('/admin/manage_user.html', form=form)

@admin_tools_bp.route('/change_password', methods=['POST'])
def change_password():
    form = EditUserPasswordForm(request.form)
    if form.validate_on_submit():
        user = User.query.get(form.user_id.data)
        if user:
            # Assuming you have a method to hash the password
            user.password = user.set_password(form.password.data)
            db.session.commit()
            flash('Password updated successfully', 'success')
        else:
            flash('User not found', 'danger')
    else:
        flash('Error updating password', 'danger')
    return redirect(url_for('admin_tools.manage_user'))

@admin_tools_bp.route('/delete_user', methods=['POST'])
def delete_user():
    user_id = request.form.get('user_id')
    confirm_text = request.form.get('confirm_text')
    if confirm_text == "CONFIRM":
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            flash('User deleted successfully', 'success')
        else:
            flash('User not found', 'danger')
    else:
        flash('Confirmation failed. User not deleted.', 'danger')
    return redirect(url_for('admin_tools.manage_user'))