from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from forms.login_form import LoginForm
from forms.employee_ticket_forms import EmployeeTicketForm


main_bp = Blueprint('main', __name__)


@main_bp.route("/")
def homepage():
    ticket_form = EmployeeTicketForm()
    form = LoginForm()
    return render_template("/homepage/homepage.html",ticket_form=ticket_form, form=form)