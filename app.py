from flask import Flask, render_template
from flask_migrate import Migrate, upgrade
from flask_login import LoginManager
from sqlalchemy import text
from models import db, seedData, Customer, read_european_countries, User
from config import Config, TestConfig
from blueprints.login import create_initial_users
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
    from blueprints.contact_form import contact_form_bp
    from blueprints.accounts import account_bp
    from blueprints.customers import customer_bp
    from blueprints.transactions import transactions_bp
    from blueprints.login import login_bp
    from blueprints.user_interface import interface_bp
    from blueprints.user_dashboard import user_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(contact_form_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(account_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(interface_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(login_bp)

    login_manager.login_view = 'main.homepage'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get_or_404(user_id)

    app.jinja_env.globals.update(is_admin=User.is_admin)
    app.jinja_env.globals.update(is_cashier=User.is_cashier)

    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f"Error: {str(e)}")
        return render_template('error.html'), 500
    
    return app

config_class = TestConfig if os.getenv('FLASK_ENV') == 'testing' else Config
app = create_app(config_class=TestConfig)


if __name__  == "__main__":
    with app.app_context():
        upgrade()
        create_initial_users()
        seedData(db, read_european_countries('static/countrycodes/country_codes.txt'))
    app.run()