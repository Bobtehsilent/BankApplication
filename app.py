from flask import Flask, render_template
from flask_migrate import Migrate, upgrade
from blueprints.main import main_bp
from blueprints.contact_form import contact_form_bp

from models import db, seedData

 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost/SpringBank'
db.app = app
db.init_app(app)
app.secret_key = 'password'
migrate = Migrate(app,db)

app.register_blueprint(main_bp)
app.register_blueprint(contact_form_bp)

@app.errorhandler(Exception)
def handle_exception(e):
    print(str(e)) 

if __name__  == "__main__":
    with app.app_context():
        upgrade()
    seedData(db)
    app.run()