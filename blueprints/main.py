from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from forms.login_form import LoginForm


main_bp = Blueprint('main', __name__)


@main_bp.route("/")
def homepage():
    form = LoginForm()
    return render_template("/homepage/homepage.html", form=form)