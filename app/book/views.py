import dateparser
from flask.views import MethodView
from flask_security import auth_required, roles_required, roles_accepted
from sqlalchemy.exc import NoResultFound
from flask_smorest import abort

from app.database import Book, db
from . import blp
from app.shema import SuccessSchema
from .schema import BookPostSchema, BookSGetchema, BookIdSchema


@blp.route('/books')
class Books(MethodView):
    @blp.response(200, BookSGetchema(many=True), description='Show all the books available')
    def get(self):
        try:
            books = db.session.query(Book).all()
        except NoResultFound:
            abort(404, message='No books found')
        else:
            return books

    @auth_required("token")
    @roles_accepted("Admin", "Librerian")
    @blp.response(201, BookSGetchema())
    @blp.arguments(BookPostSchema)
    def post(self, data):
        try:
            book = Book(**data)
            db.session.add(book)
            db.session.flush()
            book_id = book.id
        except Exception as e:
            abort(400, message=str(e))
        else:
            db.session.commit()
            book = Book.query.get(book_id)
            return book if book else abort(404, message='Book not found')


@blp.route('/<int:book_id>')
class OneSingleBook(MethodView):
    @blp.response(201, BookSGetchema())
    def get(self, book_id):
        try:
            book = Book.query.get(book_id)
        except NoResultFound:
            abort(404, message='No books found, check the book_id')
        else:
            return book

    @blp.response(200, BookSGetchema())
    @blp.arguments(BookPostSchema, location='json', as_kwargs=True)
    @roles_accepted("Admin", "Librerian")
    def put(self, book_id, **kwargs):
        try:
            book = Book.query.get(book_id)
            if not book:
                abort(404, message='Book not found')
            title = kwargs.get('title')
            if title is not None and title != '':
                book.title = title
            auteur = kwargs.get('auteur')
            if auteur is not None and auteur != '':
                book.auteur = auteur
            date_published = kwargs.get('date_published')
            if date_published is not None and date_published != '':
                book.date_published = dateparser.parse(date_published).date()
            genre = kwargs.get('genre')
            if genre is not None and genre != '':
                book.genre = genre
            image = kwargs.get('image')
            if image is not None and image != '':
                book.image = image
            isbn10 = kwargs.get('isbn10')
            if isbn10 is not None and isbn10 != '':
                book.isbn10 = isbn10
            isbn15 = kwargs.get('isbn15')
            if isbn15 is not None and isbn15 != '':
                book.isbn15 = isbn15
            description = kwargs.get('description')
            if description is not None and description != '':
                book.description = description
            pages = kwargs.get('pages')
            if pages is not None:
                book.pages = pages
            language = kwargs.get('language')
            if language is not None and language != '':
                book.language = language
            publisher = kwargs.get('publisher')
            if publisher is not None and publisher != '':
                book.publisher = publisher
            db.session.commit()
        except Exception as e:
            abort(400, message=str(e))
        else:
            return book

    @blp.response(204)
    @roles_accepted("Admin", "Librerian")
    def delete(self, book_id):
        try:
            book = Book.query.get(book_id)
            if not book:
                abort(404, message='Book not found')
            db.session.delete(book)
            db.session.commit()
        except Exception as e:
            abort(400, message=str(e))
        else:
            return '', 204
