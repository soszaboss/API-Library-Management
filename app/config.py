import os
import dotenv

dotenv.load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # configure the SQLite database, relative to the app instance folder
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') \
                              or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_TITLE = os.environ.get('API_TITLE')
    API_VERSION = os.environ.get('API_VERSION')
    OPENAPI_VERSION = os.environ.get('OPENAPI_VERSION')

    # A faire des recherches
    SECURITY_PASSWORD_SALT = "thisissaltt"
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    # SECURITY_USERNAME_ENABLE=os.environ.get('SECURITY_USERNAME_ENABLE')
