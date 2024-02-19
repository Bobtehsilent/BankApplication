from flask import Blueprint, request, flash, redirect, url_for
from models import db, Customer, CustomerContact

#Functionality for the contact form on the main page.

## IMPORTANT TO DO, PROTECTION AGAINST SQLINJECT AND SUCH
contact_form_bp = Blueprint('contact_form_bp', __name__)

@contact_form_bp.route("/contact_form", methods=['POST'])
def contact_form():
    print("Form Submitted")
    first_name = request.form['contact_first_name']
    last_name = request.form['contact_last_name']
    email = request.form['contact_email']
    message = request.form['contact_message']

    #Check if there is a customer with this name or email already
    existing_customer = Customer.query.filter(
        (Customer.GivenName == first_name) & (Customer.Surname == last_name) |
        (Customer.EmailAddress == email)
    ).first()

    new_contact= CustomerContact(FirstName=first_name, LastName=last_name, Email=email, Message=message)

    if existing_customer:
        #if there is a existing customer matching names or email it will foreign key link it.
        new_contact.CustomerId = existing_customer.Id
        flash('Existing customer found: ' + existing_customer.GivenName + ' ' + existing_customer.Surname)
    else:
        flash('No existing customer found. contact information saved')
    print(first_name, last_name, email, message)
    db.session.add(new_contact)
    db.session.commit()
    # ADD IN PROTECTIONS FOR SQL INJECTIONS.
    return redirect(url_for('main.homepage'))