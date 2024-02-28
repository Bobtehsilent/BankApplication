
class Config(object):
    SECRET_KEY = 'password'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@localhost/SpringBank'
    SQL_TRACK_MODIFICATIONS = False
    DEBUG = True

    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = 'your-email@example.com'
    

class TestConfig(Config):
    SECRET_KEY = 'password'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True