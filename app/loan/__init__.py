from flask_smorest import Blueprint

blp = Blueprint('loan', __name__, url_prefix='/loan')

from app.loan.views import *
