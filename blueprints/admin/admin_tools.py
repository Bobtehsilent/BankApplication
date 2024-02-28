from flask import render_template, redirect, url_for, flash, Blueprint, request, jsonify
from flask_login import login_required
from forms.login_form import RegisterForm, EditUserForm, EditUserPasswordForm
from models import User, db
from flask_login import current_user

admin_tools_bp = Blueprint('admin_tools', __name__)

@admin_tools_bp.route('/manage_user', methods=['GET', 'POST'])
@login_required
def manage_user():
    if not current_user.is_authenticated or current_user.Role != 'Admin':
        # Redirect non-admin users
        return redirect(url_for('user_interface.interface'))
    edit_user_form = EditUserForm()
    change_password_form = EditUserPasswordForm()
    add_user_form = RegisterForm()
    if add_user_form.validate_on_submit():
        user = User(
            Username=add_user_form.username.data,
            Password=add_user_form.password.data,
            CompanyEmail=add_user_form.email.data,
            FirstName=add_user_form.first_name.data,
            LastName=add_user_form.last_name.data,
            Role=add_user_form.role.data,
            InformationPermission=add_user_form.information_permission.data,
            ManagementPermission=add_user_form.management_permission.data,
            AdminPermission=add_user_form.admin_permission.data
        )
        user.set_password(add_user_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('New user has been successfully registered.', 'success')
        return redirect(url_for('admin_tools.manage_user'))
    return render_template('/admin/manage_user.html', add_user_form=add_user_form, edit_user_form=edit_user_form, change_password_form=change_password_form)

@admin_tools_bp.route('/get_users')
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    users_pagination = User.query.paginate(page=page, per_page=per_page, error_out=False)
    users = users_pagination.items

    users_data = [{
        'id': user.Id,
        'username': user.Username,
        'email': user.CompanyEmail,
        'first_name': user.FirstName,
        'last_name': user.LastName,
        'role': user.Role,
        # Add other fields as necessary
    } for user in users]

    return jsonify({
        'users': users_data,
        'has_next': users_pagination.has_next,
        'has_prev': users_pagination.has_prev,
        'next_num': users_pagination.next_num,
        'prev_num': users_pagination.prev_num,
        'page': users_pagination.page,
        'total_pages': users_pagination.pages,
    })

@admin_tools_bp.route('/edit_user', methods=['GET', 'POST'])
@login_required
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
@login_required
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
@login_required
def delete_user():
    data = request.get_json()
    user_id = data.get('user_id')
    confirm_text = data.get('confirm_text')
    if confirm_text == "CONFIRM":
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'User deleted successfully'}), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    else:
        return jsonify({'message': 'Confirmation failed. User not deleted.'}), 400