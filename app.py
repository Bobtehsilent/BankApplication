from flask import Flask, render_template
from flask_migrate import Migrate, upgrade
from flask_login import LoginManager
from models import Customer
from blueprints.main import main_bp
from blueprints.contact_form import contact_form_bp
from blueprints.accounts import account_bp
from blueprints.customers import customer_bp
from blueprints.transactions import transactions_bp
from blueprints.login import login_bp, create_initial_users
from blueprints.admin_dashboard import admin_bp
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
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)
app.register_blueprint(login_bp)

login_manager.login_view = 'login.login'

@login_manager.user_loader
def load_user(user_id):
    return Customer.query.get(int(user_id))

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Error: {str(e)}")
    return render_template('error.html'), 500

if __name__  == "__main__":
    with app.app_context():
        upgrade()
        create_initial_users()
        #seedData(db)
    app.run()