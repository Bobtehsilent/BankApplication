#Template jag kan använda och lägga till vad som behövs.


import unittest
from model import db, Customer
from app import create_app
from config import TestConfig

class ModelTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test variables."""
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Tear down test variables."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # Example test case
    def test_customer_creation(self):
        """Test customer can be created."""
        customer = Customer(GivenName='John', Surname='Doe', PersonalNumber='1234567890', EmailAddress='john@example.com')
        db.session.add(customer)
        db.session.commit()
        self.assertTrue(Customer.query.count() == 1)
