from flask import Blueprint, request, render_template, flash, redirect, url_for
from models import db, Customer, CustomerContact

contacts_bp = Blueprint('Contact', __name__)

@contacts_bp.route("/submit_contact_form", methods=['POST'])
def contact_form():
    first_name = request.form['contact_first_name']
    last_name = request.form['contact_last_name']
    email = request.form['contact_email']
    message = request.form['contact_message']

    #Check if there is a customer with this name or email already
    existing_customer = Customer.query.filter(
        (Customer.GivenName == first_name) &
        (Customer.Surname == last_name) |
        (Customer.EmailAddress == email)
    ).first()

    new_contact= CustomerContact(FirstName=first_name, LastName=last_name, Email=email, Message=message)

    if existing_customer:
        #if there is a existing customer matching names or email it will foreign key link it.
        new_contact.CustomerId = existing_customer.Id
        flash('Existing customer found: ' + existing_customer.GivenName + ' ' + existing_customer.Surname)
    else:
        flash('No existing customer found. contact information saved')

    db.session.add(new_contact)
    db.session.commit()

    return redirect(url_for('index'))