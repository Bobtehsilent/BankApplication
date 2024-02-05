class Config(object):
    SECRET_KEY = 'password'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@localhost/SpringBank'
    SQL_TRACK_MODIFICATIONS = False
    DEBUG = False

class TestConfig(Config):
    SECRET_KEY = 'password'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@localhost/SpringBank_testing'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True