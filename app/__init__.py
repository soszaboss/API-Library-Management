from flask import Flask
from .config import Config
from .database import db, User, Role
from flask_migrate import Migrate
from flask_security import hash_password, SQLAlchemyUserDatastore, Security
from flask_smorest import Api
from faker import Faker


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

            db.session.commit()

    from app.auth.views import blp as auth_blp
    app.register_blueprint(auth_blp)
    return app
