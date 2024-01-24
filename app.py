from flask import Flask, render_template
from flask_migrate import Migrate, upgrade
from flask_login import LoginManager
from models import Customer, read_european_countries, User
from blueprints.main import main_bp
from blueprints.contact_form import contact_form_bp
from blueprints.accounts import account_bp
from blueprints.customers import customer_bp
from blueprints.transactions import transactions_bp
from blueprints.login import login_bp, create_initial_users
from blueprints.user_interface import interface_bp
from blueprints.user_dashboard import user_bp

from models import db, seedData


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost/SpringBank'
db.app = app
app.debug = True
db.init_app(app)
app.secret_key = 'password'
migrate = Migrate(app,db)
login_manager = LoginManager()
login_manager.init_app(app)

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
    return User.query.get(int(user_id))

app.jinja_env.globals.update(is_admin=User.is_admin)
app.jinja_env.globals.update(is_cashier=User.is_cashier)

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Error: {str(e)}")
    return render_template('error.html'), 500

european_countries = read_european_countries('static/countrycodes/country_codes.txt')
if __name__  == "__main__":
    with app.app_context():
        upgrade()
        create_initial_users()
        seedData(db, european_countries)
    app.run()