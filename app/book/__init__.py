from flask_smorest import Blueprint

blp = Blueprint('book',__name__, url_prefix='/book', description='Operation on The Book')

from app.book.views import *
