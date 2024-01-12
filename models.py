from flask_sqlalchemy import SQLAlchemy
import barnum
import random
from datetime import datetime  
from datetime import timedelta  
from werkzeug.security import generate_password_hash, check_password_hash
from dateutil.relativedelta import relativedelta

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
    Telephone = db.Column(db.String(20), unique=False)
    EmailAddress = db.Column(db.String(50), unique=False, nullable=False)
    Password = db.Column(db.String(128))
    Role = db.Column(db.String(10), default='Customer')
    Accounts = db.relationship('Account', backref='Customer',
     lazy=True)
    
    def set_password(self, password):
        self.Password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.Password, password)
    

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
        #generate a random date between 1900 and 2020
        start_date = datetime(1900, 1, 1)
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
    __tablename__= "Accounts"
    Id = db.Column(db.Integer, primary_key=True)
    AccountType = db.Column(db.String(10), unique=False, nullable=False)
    Created = db.Column(db.DateTime, unique=False, nullable=False)
    Balance = db.Column(db.Integer, unique=False, nullable=False)
    Transactions = db.relationship('Transaction', backref='Account',
     lazy=True)
    CustomerId = db.Column(db.Integer, db.ForeignKey('Customers.Id'), nullable=False)

    # def withdraw(self, amount):
    #     account = Account.query.get_or_404()
    #     account.Balance += amount
    #     db.session.add()
    #     db.session.commit()
    #     return f"{amount} has been withdrawn"

class Transaction(db.Model):
    __tablename__= "Transactions"
    Id = db.Column(db.Integer, primary_key=True)
    Type = db.Column(db.String(20), unique=False, nullable=False)
    Operation = db.Column(db.String(50), unique=False, nullable=False)
    Date = db.Column(db.DateTime, unique=False, nullable=False)
    Amount = db.Column(db.Integer, unique=False, nullable=False)
    NewBalance = db.Column(db.Integer, unique=False, nullable=False)
    AccountId = db.Column(db.Integer, db.ForeignKey('Accounts.Id'), nullable=False)

class CustomerContact(db.Model):
    __tablename__= "CustomerContact"
    Id = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(50))
    LastName = db.Column(db.String(50))
    Email = db.Column(db.String(50))
    Message = db.Column(db.String(255))
    CustomerId = db.Column(db.Integer, db.ForeignKey('Customers.Id'), nullable=True)

    customer = db.relationship('Customer', backref='contacts', lazy=True)

def seedData(db):
    antal =  Customer.query.count()
    while antal < 300:
        customer = Customer()
        
        customer.GivenName, customer.Surname = barnum.create_name()

        customer.Streetaddress = barnum.create_street()
        customer.Zipcode, customer.City, _  = barnum.create_city_state_zip()
        customer.Country = "USA"
        customer.CountryCode = "US"
        customer.Birthday = barnum.create_birthday()
        n = barnum.create_cc_number()
        customer.NationalId = customer.Birthday.strftime("%Y%m%d-") + n[1][0][0:4]
        customer.TelephoneCountryCode = 55
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
        db.session.commit()
        
        antal = antal + 1