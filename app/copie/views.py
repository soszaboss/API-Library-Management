from flask.views import MethodView
from flask_security import auth_required, roles_accepted
from sqlalchemy.exc import NoResultFound
from flask_smorest import abort
from app.database import Copie, Book, State, db
from . import blp
from app.shema import SuccessSchema
from .schema import CopiePostSchema, CopieIdSchema, CopieGetSchema


@blp.route('/copies')
class Copies(MethodView):
    @blp.response(200, CopieGetSchema(many=True), description='Show all the book copies available')
    def get(self):
        try:
            q = db.session.query(
                Copie.id,
                Book.title,
                State.state,
                Copie.available
            ).join(Copie, Book.id == Copie.book).join(State, Copie.state == State.id)

        except NoResultFound:
            abort(404, message='No book copies found')
        else:
            return q

    @auth_required("token")
    @roles_accepted("Admin", "Librerian")
    @blp.response(201, CopieGetSchema())
    @blp.arguments(CopiePostSchema)
    def post(self, data):
        try:
            copie = Copie(**data)
            db.session.add(copie)
            db.session.flush()
            copie_id = copie.id
        except Exception as e:
            abort(400, message=str(e))
        else:
            db.session.commit()
            copie = db.session.query(Copie.id, Book.title, State.state, Copie.available).join(Copie, Book.id == Copie.book).join(State, Copie.state == State.id).filter(Copie.id == copie_id).first()
            return copie if copie else abort(404, message='Book copie not found')


@blp.route('/<int:copie_id>')
class OneSingleBook(MethodView):
    @blp.response(201, CopieGetSchema())
    def get(self, copie_id):
        try:
            copie = db.session.query(Copie.id, Book.title, State.state, Copie.available).join(Copie, Book.id == Copie.book).join(State, Copie.state == State.id).filter(Copie.id == copie_id).first()
        except NoResultFound:
            abort(404, message='No book copie found, check the book_id')
        else:
            if copie is not None:
                return copie
            else:
                abort(404, message='No book copie found, check the book_id')

    @blp.response(200, CopieGetSchema())
    @blp.arguments(CopiePostSchema, location='json', as_kwargs=True)
    @roles_accepted("Admin", "Librerian")
    def put(self, copie_id, **kwargs):
        try:
            copie = Copie.query.get(copie_id)
            if not copie:
                abort(404, message='Book Copies Not Found')
            book = kwargs.get('book')
            if book is not None and book != '':
                copie.book = book
            state = kwargs.get('state')
            if state is not None and state != '':
                copie.state = state
            available = kwargs.get('available')
            if available is not None and available != '':
                copie.available = available
            db.session.commit()
        except Exception as e:
            abort(400, message=str(e))
        else:
            copie = db.session.query(Copie.id, Book.title, State.state, Copie.available).join(Copie, Book.id == Copie.book).join(State, Copie.state == State.id).filter(Copie.id == copie_id).first()
            return copie

    # @blp.response(204)
    # @roles_accepted("Admin", "Librerian")
    # def delete(self, copie_id):
    #     try:
    #         copie = Copie.query.get(copie_id)
    #         if not copie:
    #             abort(404, message='Book not found')
    #         db.session.delete(copie)
    #         db.session.commit()
    #     except Exception as e:
    #         abort(400, message=str(e))
    #     else:
    #         return '', 204
