from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
import barnum
import random
from datetime import datetime  
from datetime import timedelta  
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
    Telephone = db.Column(db.String(20), unique=False)
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
    Balance = db.Column(db.Integer, nullable=False)
    Transactions = db.relationship('Transaction', backref='Account', lazy=True)
    CustomerId = db.Column(db.Integer, db.ForeignKey('Customers.Id'), nullable=False)

class Transaction(db.Model):
    __tablename__ = "Transactions"
    Id = db.Column(db.Integer, primary_key=True)
    Type = db.Column(db.String(20), nullable=False)
    Operation = db.Column(db.String(50), nullable=False)
    Date = db.Column(db.DateTime, nullable=False)
    Amount = db.Column(db.Integer, nullable=False)
    NewBalance = db.Column(db.Integer, unique=False, nullable=False)
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

class CustomerContact(db.Model):
    __tablename__= "CustomerContact"
    Id = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(50))
    LastName = db.Column(db.String(50))
    Email = db.Column(db.String(50))
    Message = db.Column(db.String(255))
    CustomerId = db.Column(db.Integer, db.ForeignKey('Customers.Id'), nullable=True)

    customer = db.relationship('Customer', backref='contacts', lazy=True)

# def read_european_countries(file_path):
#     countries = []
#     with open(file_path, 'r') as file:
#         for line in file:
#             _, code, name = line.strip().split('\t')
#             countries.append((code, name))
#         return countries
    
def load_country_codes(filename='country_codes.txt'):
    country_codes = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            parts = line.strip().split(',')
            if len(parts) == 3:
                country_codes.append({
                    'code': parts[0].strip(),
                    'name': parts[1].strip(),
                    'tel_code': parts[2].strip()
                })
    return country_codes

# def add_overdraft_to_debt_account(customer, overdraft_amount):
#     debt_account = Account.query.filter_by(CustomerId=customer.Id, AccountType="Debt").first()
#     if not debt_account:
#         debt_account = Account(
#             CustomerId=customer.Id,
#             AccountType="Debt",
#             Created=datetime.now(),
#             Balance=0  # Start with a zero balance
#         )
#         db.session.add(debt_account)
    
#     # Add the overdraft amount to the Debt account's balance
#     debt_account.Balance += overdraft_amount
#     db.session.commit()

# def add_overdraft_to_debt_account(customer_id, overdraft_amount):
#     # Find or create a "Debt" account for the customer
#     debt_account = Account.query.filter_by(CustomerId=customer_id, AccountType="Debt").first()
#     if not debt_account:
#         debt_account = Account(
#             CustomerId=customer_id,
#             AccountType="Debt",
#             Created=datetime.now(),
#             Balance=0
#         )
#         db.session.add(debt_account)
#     # Update the debt account's balance
#     debt_account.Balance += overdraft_amount

def seedData(db, european_countries):
    try:
        current_count =  Customer.query.count()
        target_count = 300
        
        while current_count < target_count:
            customer = Customer()
            
            customer.GivenName, customer.Surname = barnum.create_name()
            customer.Streetaddress = barnum.create_street()
            customer.Zipcode, customer.City, _  = barnum.create_city_state_zip()
            country_code, country_name = random.choice(european_countries)
            customer.Country = country_name
            customer.CountryCode = country_code
            customer.Birthday = barnum.create_birthday()
            customer.set_swedish_personal_number()
            customer.Telephone = barnum.create_phone()
            customer.EmailAddress = barnum.create_email().lower()

            for x in range(random.randint(1,4)):
                account = Account()

                c = random.randint(0,100)
                if c < 33:
                    account.AccountType = "Personal"    
                elif c < 66:
                    account.AccountType = "Checking"    
                else:
                    account.AccountType = "Savings"    


                start = datetime.now() + timedelta(days=-random.randint(1000,10000))
                account.Created = start
                account.Balance = 0
                
                for n in range(random.randint(0,30)):
                    belopp = random.randint(0,30)*100
                    tran = Transaction()
                    start = start+ timedelta(days=-random.randint(10,100))
                    if start > datetime.now():
                        break
                    tran.Date = start
                    account.Transactions.append(tran)
                    tran.Amount = belopp
                    if account.Balance - belopp < 0:
                        tran.Type = "Debit"
                    else:
                        if random.randint(0,100) > 70:
                            tran.Type = "Debit"
                        else:
                            tran.Type = "Credit"

                    r = random.randint(0,100)
                    if tran.Type == "Debit":
                        account.Balance = account.Balance + belopp
                        if r < 20:
                            tran.Operation = "Deposit cash"
                        elif r < 66:
                            tran.Operation = "Salary"
                        else:
                            tran.Operation = "Transfer"
                    else:
                        account.Balance = account.Balance - belopp
                        if r < 40:
                            tran.Operation = "ATM withdrawal"
                        if r < 75:
                            tran.Operation = "Payment"
                        elif r < 85:
                            tran.Operation = "Bank withdrawal"
                        else:
                            tran.Operation = "Transfer"

                    tran.NewBalance = account.Balance


                customer.Accounts.append(account)

            db.session.add(customer)
            if current_count % 20 == 0:
                print(f"20 records made: current: {current_count}")
                db.session.commit()
            current_count += 1

    except Exception as e:
        db.session.rollback()
        print(f"an error occurred: {e}")
    print("Data seeding complete")