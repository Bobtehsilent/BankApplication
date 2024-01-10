from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from blueprints.main import main_bp



from models import db, seedData

 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:hejsan123@localhost/Bank'
db.app = app
db.init_app(app)
migrate = Migrate(app,db)

app.register_blueprint(main_bp)
 

if __name__  == "__main__":
    with app.app_context():
        upgrade()
    
    #seedData(db)
    app.run()