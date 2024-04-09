from flask_smorest import Blueprint

blp = Blueprint('auth', __name__, url_prefix='/auth', description='Operation on The User')

from app.auth.views import *
