from datetime import datetime, timedelta
from models import Transaction, Account, Customer
from flask_mailman import EmailMessage, Mail
from threading import Thread
import time

def fetch_transactions():
    three_days_ago = datetime.now() - timedelta(days=3)
    return Transaction.query.filter(Transaction.Date >= three_days_ago).all()

def check_transactions(transactions):
    suspicious_transactions = []

    transactions_per_account = {}
    for transaction in transactions:
        if transaction.AccountId not in transactions_per_account:
            transactions_per_account[transaction.AccountId] = []
        transactions_per_account[transaction.AccountId].append(transaction)

    for account_id, account_transactions in transactions_per_account.items():
        total_amount = sum(t.Amount for t in account_transactions)
        for transaction in account_transactions:
            if transaction.Amount > 15000 or total_amount > 23000:
                suspicious_transactions.append(transaction)
                break  

    return suspicious_transactions

def send_report(suspicious_transactions, mail):
    print(f"Debug: mail object before send {mail}") 
    if not suspicious_transactions:
        print("No suspicious transactions found.")
        return

    transactions_by_country = {}
    for transaction in suspicious_transactions:
        # Fetch the account and then the customer to get the country
        account = Account.query.get(transaction.AccountId)
        customer = Customer.query.get(account.CustomerId)
        country = customer.Country

        if country not in transactions_by_country:
            transactions_by_country[country] = []
        transactions_by_country[country].append(transaction)

    for country, transactions in transactions_by_country.items():
        subject = "Suspicious Transactions Report"
        body = "List of suspicious transactions:\n\n"
        for transaction in transactions:
            body += f"Customer Name: {customer.GivenName} {customer.Surname}, Account Number: {account.Id}, Transaction ID: {transaction.Id}, Amount: {transaction.Amount}\n"
        recipient = f"{country.lower()}@testbanken.se"  # Ensuring the email is all lowercase
        email = EmailMessage(subject=subject, body=body, to=[recipient])
        email.send()
        print(f"Report sent to {recipient}.")



def check_and_send_reports(mail):
    transactions = fetch_transactions()
    suspicious_transactions = check_transactions(transactions)
    send_report(suspicious_transactions, mail)
    print("Tasks ran")

# def run_once_at_startup(mail):
#     print(mail)
#     print("Running initial check and sending reports if any...")
#     check_and_send_reports(mail)
#     print("Initial check completed.")


# def start_daily_task_thread(mail):
#     task_thread = Thread(target=run_daily_task, args=(mail,))
#     task_thread.daemon = True 
#     task_thread.start()

