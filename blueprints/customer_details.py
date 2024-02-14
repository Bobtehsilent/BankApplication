from flask import Blueprint, render_template, url_for


customer_detail_bp = Blueprint('customer_detail', __name__, url_prefix='/details')

@customer_detail_bp.route('/customer_detail/<int:user_id>')
def details(user_id):
    return render_template('customer_detail.html', user_id=user_id)



@customer_detail_bp.route('/anchor_links')
def anchor_links():
    # Construct base URLs for the links
    details_base_url = url_for('customer.details', user_id=0)[:-1]  
    manage_base_url = url_for('manage_customer', user_id=0)[:-1] 
    return render_template('your_template.html', details_base_url=details_base_url, manage_base_url=manage_base_url)