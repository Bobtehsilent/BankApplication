from flask import Blueprint, render_template, url_for
from models import Customer


customer_detail_bp = Blueprint('customer_detail', __name__, url_prefix='/details')

# @customer_detail_bp.route('/customer_detail/<int:user_id>')
# def details(user_id):
#     customer = Customer.query.get_or_404(user_id)
#     return render_template('/customer/customer_detail.html', customer=customer)


# @customer_detail_bp.route('/anchor_links')
# def anchor_links():
#     details_base_url = url_for('customer.details', user_id=0)[:-1]  
#     manage_base_url = url_for('manage_customer', user_id=0)[:-1] 
#     return render_template('your_template.html', details_base_url=details_base_url, manage_base_url=manage_base_url)