from flask import Blueprint, request, flash, redirect, url_for, render_template
from models import db, User, EmployeeTicket
from forms.employee_ticket_forms import EmployeeTicketForm

ticket_bp = Blueprint('ticket', __name__)

@ticket_bp.route("/contact_form", methods=['GET', 'POST'])
def employee_ticket():
    form = EmployeeTicketForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        message = form.message.data

        existing_user = User.query.filter(
            (User.FirstName == first_name) & (User.LastName == last_name) |
            (User.CompanyEmail == email)
        ).first()

        new_ticket = EmployeeTicket(FirstName=first_name, LastName=last_name, Email=email, Message=message)

        if existing_user:
            new_ticket.UserId = existing_user.Id
            flash('Existing user found: ' + existing_user.FirstName + ' ' + existing_user.LastName)
        else:
            flash('No existing user found. Contact information saved')

        db.session.add(new_ticket)
        db.session.commit()
        flash('Thank you for your ticket')
        return redirect(url_for('main.homepage'))

    # For GET requests, or if form is not valid
    return render_template('/homepage/homepage.html', form=form)