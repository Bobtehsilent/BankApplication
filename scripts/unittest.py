import unittest
from unittest.mock import patch
from app import create_app
from models import db, Account, Customer, Transaction
from blueprints.transactions.transactions import validate_transaction, transfer_funds
from scripts.transaction_script import fetch_transactions, check_transactions, send_report
from datetime import datetime, timedelta
from config import TestConfig

class TransactionTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.customer = Customer(GivenName="Test", Surname="User", PersonalNumber="1234567890", EmailAddress="test@example.com")
        db.session.add(self.customer)
        db.session.commit()
        self.account = Account(AccountType='Checking', Created=datetime.utcnow(), Balance=1000, CustomerId=self.customer.Id)
        db.session.add(self.account)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_withdraw_more_than_balance(self):
        account = Account(AccountType='Checking', Created=datetime.utcnow(), Balance=100, CustomerId=self.customer.Id)
        db.session.add(account)
        db.session.commit()

        is_valid, message = validate_transaction(account.Id, -150, 'withdraw')
        self.assertFalse(is_valid, "Should not allow withdrawing more than the balance")

    def test_transfer_more_than_balance(self):
        from_account = Account(AccountType='Checking', Created=datetime.utcnow(), Balance=100, CustomerId=self.customer.Id)
        db.session.add(from_account)
        db.session.commit()
        
        to_account = Account(AccountType='Savings', Created=datetime.utcnow(), Balance=100, CustomerId=self.customer.Id)
        db.session.add(to_account)
        db.session.commit()

        result, message = transfer_funds(from_account.Id, to_account.Id, 1500)
        self.assertFalse(result, "Should not allow transferring more than balance")
        self.assertEqual(message, "Insufficient funds.", "The message should indicate insufficient funds.")

    def test_deposit_negative_amount(self):
        account = Account(AccountType='Checking', Created=datetime.utcnow(), Balance=100, CustomerId=self.customer.Id)
        db.session.add(account)
        db.session.commit()

        is_valid, message = validate_transaction(account.Id, -100, 'deposit')
        self.assertFalse(is_valid, "Should not allow depositing negative amounts")

    def test_withdraw_positive_amount(self):
        account = Account(AccountType='Checking', Created=datetime.utcnow(), Balance=100, CustomerId=self.customer.Id)
        db.session.add(account)
        db.session.commit()

        is_valid, message = validate_transaction(account.Id, 100, 'withdraw')
        self.assertFalse(is_valid, "Should not allow withdrawing positive amounts")

    def test_fetch_transactions(self):
        recent_deposit_transaction = Transaction(Amount=100, AccountId=self.account.Id, NewBalance=500, Type='Credit', Operation='Deposit', Date=datetime.utcnow())
        recent_withdrawal_transaction = Transaction(Amount=50, AccountId=self.account.Id, NewBalance=300, Type='Debit', Operation='Withdraw', Date=datetime.utcnow())
        
        db.session.add_all([recent_deposit_transaction, recent_withdrawal_transaction])
        db.session.commit()

        fetched_transactions = fetch_transactions()

        self.assertTrue(len(fetched_transactions) > 0, "Should fetch recent transactions")
        print(f"tested {fetched_transactions}")


    def test_check_suspicious_transactions(self):
        suspicious_transaction_deposit = Transaction(Amount=16000, AccountId=self.account.Id, NewBalance=17000,Type='Credit', Operation='Deposit', Date=datetime.utcnow())
        normal_transaction_withdrawal = Transaction(Amount=100, AccountId=self.account.Id, NewBalance=200,Type='Debit', Operation='Withdraw', Date=datetime.utcnow() - timedelta(days=1))
        suspicious_transaction_transfer = Transaction(Amount=15000, AccountId=self.account.Id, NewBalance=18000,Type='Debit', Operation='Transfer', Date=datetime.utcnow())

        db.session.add_all([suspicious_transaction_deposit, normal_transaction_withdrawal, suspicious_transaction_transfer])
        db.session.commit()

        transactions = [suspicious_transaction_deposit, normal_transaction_withdrawal, suspicious_transaction_transfer]

        result = check_transactions(transactions)

        self.assertTrue(len(result) == 2, "Should identify suspicious transactions based on amount and type")

if __name__ == '__main__':
    unittest.main()
