from flask import Flask, jsonify, request, abort, Blueprint, url_for
from collections import defaultdict
from flask_sqlalchemy import SQLAlchemy
from models import Customer, Account, Transaction, User, CustomerContact
from sqlalchemy import or_
from blueprints.customers.customers import customer_to_dict

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customerobj = Customer.query.get(customer_id)
    if customerobj is None:
        return jsonify({'error': 'Customer not found'}), 404
    customer = customer_to_dict(customerobj)
    return jsonify(customer)

# Customer list api call

@api_bp.route('/customer_lists', methods=['GET'])
def get_customer_list():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    sort_column = request.args.get('sort_column', 'Surname')
    sort_order = request.args.get('sort_order', 'asc')
    search_query = request.args.get('search', '').strip()

    query = Customer.query

    if search_query:
        query = query.filter(or_(
            Customer.Id.contains(search_query),
            Customer.Surname.contains(search_query),
            Customer.GivenName.contains(search_query),
            Customer.Streetaddress.contains(search_query),
            Customer.City.contains(search_query),
            Customer.Country.contains(search_query),
        ))

    if sort_order == 'asc':
        query = query.order_by(getattr(Customer, sort_column).asc())
    else:
        query = query.order_by(getattr(Customer, sort_column).desc())

    paginated_customers = query.paginate(page=page, per_page=per_page, error_out=False)
    customers = [customer_to_dict(customer) for customer in paginated_customers.items]  # Assume customer_to_dict is implemented

    return jsonify({
        'customers': customers,
        'pagination': {
            'total_pages': paginated_customers.pages,
            'current_page': paginated_customers.page,
            'has_prev': paginated_customers.has_prev,
            'has_next': paginated_customers.has_next,
            'prev_num': paginated_customers.prev_num if paginated_customers.has_prev else None,
            'next_num': paginated_customers.next_num if paginated_customers.has_next else None,
        }
    })


@api_bp.route('/api/accounts/<int:account_id>', methods=['GET'])
def get_account(account_id):
    account = Account.query.get(account_id)
    if account is None:
        return jsonify({'error': 'Account not found'}), 404
    return jsonify({
        'Id': account.Id,
        'AccountType': account.AccountType,
        'Balance': account.Balance,
        # Include other fields as necessary
    })

#transaction get

@api_bp.route('/api/transactions/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    if transaction is None:
        return jsonify({'error': 'Transaction not found'}), 404
    return jsonify({
        'Id': transaction.Id,
        'Type': transaction.Type,
        'Amount': transaction.Amount,
        # Include other fields as necessary
    })

# Graph data

@api_bp.route('/graph_transactions/<int:customer_id>', methods=['GET'])
def transactions_graph(customer_id):
    transactions = Transaction.query.join(Account).filter(
        Account.CustomerId == customer_id
    ).order_by(Transaction.Date.asc()).all()
    
    # Use account ID as the key to differentiate between accounts of the same type
    balances_by_account = defaultdict(lambda: {"type": "", "balances": []})
    
    for transaction in transactions:
        account_id = transaction.AccountId
        account_type = transaction.Account.AccountType
        # Initialize account type if not already set
        if not balances_by_account[account_id]["type"]:
            balances_by_account[account_id]["type"] = account_type
        
        # Adjust balance based on the transaction type
        previous_balance = balances_by_account[account_id]["balances"][-1]["cumulative_balance"] if balances_by_account[account_id]["balances"] else 0
        new_balance = previous_balance + transaction.Amount if transaction.Type == "Debit" else previous_balance - transaction.Amount
        
        # Prevent balance from going below zero, if required by your system's logic
        
        balances_by_account[account_id]["balances"].append({
            "date": transaction.Date.strftime("%Y-%m-%d"),
            "cumulative_balance": new_balance
        })

    # Prepare the result for JSON serialization
    result = [{
        "account_id": account_id,
        "account_type": data["type"],
        "balances": data["balances"]
    } for account_id, data in balances_by_account.items()]
    
    return jsonify(result)

#load transaction in customer details.

@api_bp.route('/customers/<int:customer_id>/transactions', methods=['GET'])
def more_transactions(customer_id):
    page = request.args.get('page', 1, type=int)
    limit = 20
    offset = (page - 1) * limit

    transactions_query = Transaction.query.join(Account).join(Customer) \
                                    .filter(Customer.Id == customer_id) \
                                    .order_by(Transaction.Date.desc())

    transactions = transactions_query.offset(offset).limit(limit).all()
    total_transactions = transactions_query.count()
    has_more_data = (page * limit) < total_transactions

    transactions_data = [{
        'account_id': transaction.AccountId,
        'date': transaction.Date.strftime('%Y-%m-%d'),
        'amount': transaction.Amount,
        'new_balance': transaction.NewBalance,
        'type': transaction.Type,
        'operation': transaction.Operation
    } for transaction in transactions]
    
    return jsonify([transactions_data, has_more_data])

@api_bp.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({
        'Id': user.Id,
        'Username': user.Username,
        'Role': user.Role,
        # Include other fields as necessary
    })

@api_bp.route('/api/customercontacts/<int:contact_id>', methods=['GET'])
def get_customer_contact(contact_id):
    contact = CustomerContact.query.get(contact_id)
    if contact is None:
        return jsonify({'error': 'Contact not found'}), 404
    return jsonify({
        'Id': contact.Id,
        'FirstName': contact.FirstName,
        'LastName': contact.LastName,
        'Email': contact.Email,
        # Include other fields as necessary
    })
