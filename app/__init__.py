import random
import dateparser
from flask import Flask
from .config import Config
from .database import db, User, Role, State, Book, Copie
from flask_migrate import Migrate
from flask_security import hash_password, SQLAlchemyUserDatastore, Security
from flask_smorest import Api
from faker import Faker
import json


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    migrate = Migrate()

    # initialize the app with the extension
    db.init_app(app)
    migrate.init_app(app, db)

    # initialize flask smorest

    api = Api(app)

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, user_datastore)

    @app.before_request
    def before_request():
        with app.app_context():
            # db.drop_all()
            # db.create_all()
            fake = Faker()
            user_datastore.find_or_create_role(name="Admin", description="...")
            user_datastore.find_or_create_role(name="Librerian", description="...")
            user_datastore.find_or_create_role(name="User", description="...")
            if not user_datastore.find_user(email="admin@email.com"):
                user_datastore.create_user(email="admin@email.com", password="admin", first_name=fake.first_name(),
                                           last_name=fake.last_name(), username="admin", roles=["Admin"])
            if not user_datastore.find_user(email="librerian@email.com"):
                user_datastore.create_user(email="librerian@email.com", password=hash_password("librerian"),
                                           first_name=fake.first_name(), last_name=fake.last_name(),
                                           username="librerian", roles=["Librerian"])
            state_books = [
                {
                    "etat": "Neuf",
                    "descprition": "le livre peut être offert. Il a été lu mais n’a qu’une très légère pliure de lecture sur le recto de la couverture et tout de l’aspect d’un livre neuf12."
                },
                {
                    "etat": "Très Bon État",
                    "descprition": "Le livre a déjà été lu, mais il est toujours en excellent état. Les éventuelles marques sur la couverture sont peu nombreuses et visibles."
                },
                {
                    "etat": "Très Bon État",
                    "descprition": "le livre peut être offert. Il a été lu mais n’a qu’une très légère pliure de lecture sur le recto de la couverture et tout de l’aspect d’un livre neuf12."
                },
                {
                    "etat": "État Correct ",
                    "descprition": "Le livre a été lu plusieurs fois et présente des marques d’usure apparentes. La couverture peut être légèrement endommagée, mais son intégrité est intacte."
                },
                {
                    "etat": "État Usagé",
                    "descprition": "Le livre peut être lu dans son intégralité : aucune page manquante ni aucun autre défaut susceptible de compromettre la lisibilité du texte."
                }
            ]

            for state in state_books:
                etat = state["etat"]
                descprition = state["descprition"]
                book_state_exite = db.session.query(State).filter_by(state=etat).one_or_none()
                if not book_state_exite:
                    db.session.add(State(state=etat, description=descprition))

            with open('app/data/books.json', 'r') as f:
                books_data = json.load(f)
                for data in books_data:
                    book = db.session.query(Book).filter_by(title=data['title']).one_or_none()
                    if not book:
                        new_book = Book(title=data['title'],
                                        auteur=data['author'],
                                        date_published=dateparser.parse(data['publication_date']).date(),
                                        genre=data['genre'],
                                        image=data['image'],
                                        isbn10=data['isbn10'].strip() if data['isbn10'] != None else None,
                                        isbn15=data['isbn15'].strip() if data['isbn15'] != None else None,
                                        description=data['description'],
                                        pages=data['page'] if data['page'] != 'Unknown' else None,
                                        language=data['language'],
                                        publisher=data['publishers'])
                        db.session.add(new_book)
                        db.session.flush()  # This will assign an ID to new_book
                        lenght = random.randint(1, 25)
                        for i in range(lenght):
                            db.session.add(Copie(
                                book=new_book.id,
                                state=random.choice([1, 2, 3, 4]),
                                available=random.choice([True, False]),
                            ))

            db.session.commit()

    # implementing authentificztion
    from app.auth import blp as auth_blp
    api.register_blueprint(auth_blp)

    #implementing book
    from app.book import blp as book_blp
    api.register_blueprint(book_blp)

    return app
