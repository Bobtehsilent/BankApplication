from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric
from faker import Faker
import barnum
import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from sqlalchemy.sql.expression import func 
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash
from dateutil.relativedelta import relativedelta
import string

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__= "Customers"
    Id = db.Column(db.Integer, primary_key=True)
    GivenName = db.Column(db.String(50), unique=False, nullable=False)
    Surname = db.Column(db.String(50), unique=False, nullable=False)
    Streetaddress = db.Column(db.String(50), unique=False)
    City = db.Column(db.String(50), unique=False)
    Zipcode = db.Column(db.String(10), unique=False)
    Country = db.Column(db.String(30), unique=False)
    CountryCode = db.Column(db.String(2), unique=False)
    Birthday = db.Column(db.DateTime, unique=False)
    PersonalNumber = db.Column(db.String(20), unique=False, nullable=False)
    TelephoneCountryCode = db.Column(db.String(20))
    Telephone = db.Column(db.String(50), unique=False)
    EmailAddress = db.Column(db.String(50), unique=False, nullable=False)
    Accounts = db.relationship('Account', backref='Customer',
     lazy=True)
    
    
    #LUHN CALCULATION for personalnumbers
    def calculate_luhn(self, number):
        def digits_of(n):
            return [int(d) for d in str(n)]
        digits = digits_of(number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d*2))
        return (10 - (checksum % 10)) % 10
    
    #i changed nationalid to personalnumber. since it is a swedish bank you must have one.
    def set_swedish_personal_number(self):
        #generate a random date between 1960 and 2020
        start_date = datetime(1960, 1, 1)
        end_date = datetime(2020, 12, 31)
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + relativedelta(days=random_number_of_days)

        #format it to yyyymmdd
        date_part = random_date.strftime('%Y%m%d')

        #generate three random digits
        three_digits = random.randint(100,999)

        #combine and calculate the control using luhn
        temp_number = f"{date_part}{three_digits}"
        control_digit = self.calculate_luhn(temp_number)

        self.PersonalNumber = f"{date_part}-{three_digits}{control_digit}"
    


class Account(db.Model):
    __tablename__ = "Accounts"
    Id = db.Column(db.Integer, primary_key=True)
    AccountType = db.Column(db.String(10), nullable=False)
    Created = db.Column(db.DateTime, nullable=False)
    Balance = db.Column(Numeric(10, 2), nullable=False)
    Transactions = db.relationship('Transaction', backref='Account', lazy=True)
    CustomerId = db.Column(db.Integer, db.ForeignKey('Customers.Id'), nullable=False)

class Transaction(db.Model):
    __tablename__ = "Transactions"
    Id = db.Column(db.Integer, primary_key=True)
    Type = db.Column(db.String(20), nullable=False)
    Operation = db.Column(db.String(50), nullable=False)
    Date = db.Column(db.DateTime, nullable=False)
    Amount = db.Column(Numeric(10, 2), nullable=False)
    NewBalance = db.Column(Numeric(10, 2), unique=False, nullable=False)
    AccountId = db.Column(db.Integer, db.ForeignKey('Accounts.Id'), nullable=False)


class User(db.Model):
    __tablename__= "User"
    Id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50))
    Password = db.Column(db.String(255))
    CompanyEmail = db.Column(db.String(50))
    FirstName = db.Column(db.String(50))
    LastName = db.Column(db.String(50))
    Role = db.Column(db.String(50), default='Cashier') #admin or cashier
    # Permissions
    InformationPermission = db.Column(db.Boolean, default=True)
    ManagementPermission = db.Column(db.Boolean, default=False)
    AdminPermission = db.Column(db.Boolean, default=False)


    def is_admin(self):
        return current_user.is_authenticated and current_user.Role == 'Admin'
    
    def is_cashier(self):
        return current_user.is_authenticated and current_user.Role == 'Cashier'

    #creating and checking passwords
    def set_password(self, password):
        self.Password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.Password, password)
    
    def generate_password(self, length=6):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(length))
    
    #flask_login integration
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.Id)

class EmployeeTicket(db.Model):
    __tablename__= "EmployeeTicket"
    Id = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(50))
    LastName = db.Column(db.String(50))
    Email = db.Column(db.String(50))
    Message = db.Column(db.String(255))
    UserId = db.Column(db.Integer, db.ForeignKey('User.Id'), nullable=True)

    User = db.relationship('User', backref='Ticket', lazy=True)

def load_country_codes(filename='country_codes.txt'):
    country_codes = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            parts = line.strip().split(',')
            if len(parts) == 4:
                country_codes.append({
                    'code': parts[0].strip(),
                    'name': parts[1].strip(),
                    'tel_code': parts[2].strip(),
                    'fake_code': parts[3].strip()
                })
    return country_codes


def seedData(db, country_codes_filename):
    fake = Faker()
    country_codes = load_country_codes(country_codes_filename)
    email_domains = ['example.com', 'mail.com', 'test.org']
    operation_choices_credit = ['Deposit cash', 'Salary', 'Transfer to']
    operation_choices_debit = ['ATM withdrawal', 'Payment', 'Bank withdrawal', 'Transfer from']

    current_count = Customer.query.count()
    target_count = 20

    if current_count >= target_count:
        print("Target count reached, skipping seeding.")
        return

    try:
        # Seed Customers up to target_count
        while current_count < target_count:  # Adjust based on remaining count
            country = random.choice(country_codes)
            Faker.seed(random.randint(0, 9999))
            try:
                fake = Faker(country['fake_code'])
            except AttributeError:
                print(f"Faker locale `{country['fake_code']}` not supported. Using 'en_US' as fallback.")
                fake = Faker('en_US')
            
            customer = Customer()
            customer.set_swedish_personal_number()  # Use your method for personal number generation
            given_name = fake.first_name()
            surname = fake.last_name()
            email = f"{given_name}.{surname}@{random.choice(email_domains)}".lower()

            customer.GivenName = given_name
            customer.Surname = surname
            customer.Streetaddress = fake.street_address()[:50]
            customer.City = fake.city()
            customer.Zipcode = fake.postcode()
            customer.Country = country['name']
            customer.CountryCode = country['code']
            customer.Birthday = datetime.strptime(customer.PersonalNumber[:8], '%Y%m%d').date()
            customer.EmailAddress = email
            customer.TelephoneCountryCode = country['tel_code']
            customer.Telephone = fake.phone_number()

            db.session.add(customer)
            db.session.flush()

            # Seed Accounts and Transactions ensuring balance never goes below 0
            for _ in range(random.randint(1, 3)):
                account_created_date = datetime.now() - timedelta(days=random.randint(365, 3650))
                initial_balance = 0
                account = Account(
                    AccountType=random.choice(["Personal", "Checking", "Savings"]),
                    Created=account_created_date,
                    Balance=initial_balance,
                    CustomerId=customer.Id
                )

                db.session.add(account)
                db.session.flush()
                last_transaction_date = account.Created
                balance = account.Balance

                for _ in range(random.randint(5, 20)):  # Generate 5-20 transactions
                    days_since_last_transaction = random.randint(1, 90)  # Up to 90 days between transactions
                    transaction_date = last_transaction_date + timedelta(days=days_since_last_transaction)
                    last_transaction_date = transaction_date

                    # Randomly decide the transaction amount; ensure it's within a realistic range
                    if random.choice([True, False]):  # Decide between deposit (credit) and withdrawal (debit)
                        amount = random.uniform(50, 5000)  # Deposit amount
                        operation = random.choice(['Deposit cash', 'Salary', 'Transfer to'])
                        balance += amount  # Increase account balance
                    else:
                        if balance > 50:  # Only allow withdrawals if there's enough balance
                            amount = -random.uniform(50, min(5000, balance))  # Withdrawal amount, ensuring balance doesn't go negative
                            operation = random.choice(['ATM withdrawal', 'Payment', 'Bank withdrawal', 'Transfer from'])
                            balance += amount  # Decrease account balance
                        else:
                            continue  # Skip withdrawal if balance is too low

                    transaction = Transaction(
                        Type="Credit" if amount > 0 else "Debit",
                        Operation=operation,
                        Date=transaction_date,
                        Amount=amount,
                        NewBalance=balance,
                        AccountId=account.Id
                    )
                    db.session.add(transaction)

                account.Balance = balance
                db.session.add(account)

            # Seed Users
            for _ in range(1):  # Adjust the number as needed
                user = User(
                    Username=fake.user_name(),
                    Password=generate_password_hash(fake.password()),
                    CompanyEmail=f"{fake.user_name()}@{random.choice(email_domains)}",
                    FirstName=fake.first_name(),
                    LastName=fake.last_name(),
                    Role=random.choice(['Cashier', 'Admin'])
                )
                db.session.add(user)
                db.session.flush()
                    # Seed EmployeeTickets
                    # for _ in range(1):  # Adjust as needed
                ticket = EmployeeTicket(
                    FirstName=fake.first_name(),
                    LastName=fake.last_name(),
                    Email=f"{fake.user_name()}@{random.choice(email_domains)}",
                    Message=fake.sentence(),
                    UserId=user.Id
                )
                db.session.add(ticket)
            if current_count % 20 == 0:
                print(f"20 records made: current: {current_count}")
                db.session.commit()
            current_count += 1

        db.session.commit()
        print("Data seeding complete")

    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")