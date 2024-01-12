from flask import Blueprint, render_template
from sqlalchemy.sql import func
from models import Customer, Account, db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard')
def dashboard():
    customer_count = Customer.query.count()
    account_count = Account.query.count()
    total_balance = db.session.query(db.func.sum(Account.Balance)).scalar()
    return render_template('admin_dashboard.html', customer_count=customer_count, account_count=account_count, total_balance=total_balance)