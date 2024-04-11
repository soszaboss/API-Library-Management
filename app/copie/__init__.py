from flask_smorest import Blueprint

blp = Blueprint('copie',__name__, url_prefix='/copie', description='Operation on The Book Copie(s)')

from app.copie.views import *
