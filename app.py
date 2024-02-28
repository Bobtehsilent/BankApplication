from flask import Flask, render_template
from flask_migrate import Migrate, upgrade
from flask_login import LoginManager
from models import db, seedData, User, Transaction, Customer, EmployeeTicket, Account
from config import Config, TestConfig
from blueprints.login.login import create_initial_users
from scripts.transaction_script import check_and_send_reports
from scripts.truncate_tables import truncate_tables
from threading import Thread
import time
from datetime import datetime, timedelta
from flask_mailman import Mail
import os

login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    Migrate(app, db)
    login_manager.init_app(app)

    #Registering blueprints
    from blueprints.main import main_bp
    from blueprints.employeeticket.employee_ticket import ticket_bp
    from blueprints.accounts.accounts import account_bp
    from blueprints.customers.customers import customer_bp
    from blueprints.transactions.transactions import transactions_bp
    from blueprints.login.login import login_bp
    from blueprints.interface.user_interface import interface_bp
    from blueprints.admin.admin_tools import admin_tools_bp
    from api.api import api_bp
    app.register_blueprint(admin_tools_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(ticket_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(account_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(interface_bp)
    app.register_blueprint(login_bp)

    login_manager.login_view = 'main.homepage'

    @login_manager.user_loader
    def load_user(user_id):
        user = User.query.get_or_404(user_id)
        if user:
            return user
        else:
            return None

    app.jinja_env.globals.update(is_admin=User.is_admin)
    app.jinja_env.globals.update(is_cashier=User.is_cashier)

    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f"Error: {str(e)}")
        return render_template('error.html'), 500
    
    return app

config_class = TestConfig if os.getenv('FLASK_ENV') == 'testing' else Config
app = create_app(config_class)
mail = Mail(app)

def run_daily_task(mail):
    def task():
        with app.app_context():
            while True:
                now = datetime.now()
                if 1 <= now.hour < 6:
                    print("It's between 01:00 and 06:00. Running task...")
                    check_and_send_reports(mail)
                    print("Task completed. Checking again in 5 minutes.")
                    time.sleep(300)
                else:
                    if now.hour >= 6:
                        next_run_time = now.replace(day=now.day, hour=1, minute=0, second=0, microsecond=0) + timedelta(days=1)
                    else:
                        next_run_time = now.replace(hour=1, minute=0, second=0, microsecond=0)
                    time_to_sleep = (next_run_time - now).total_seconds()
                    print(f"Not time yet. Current time: {now}. Sleeping for {time_to_sleep/60/60} hours.")
                    time.sleep(time_to_sleep)
    
    thread = Thread(target=task)
    thread.start()

if __name__  == "__main__":
    with app.app_context():
        upgrade()
        create_initial_users()
        run_daily_task(mail)
        #truncate_tables([Transaction, Account, EmployeeTicket, User, Customer], db.session)
        seedData(db, 'static/countrycodes/country_codes.txt')
    app.run()