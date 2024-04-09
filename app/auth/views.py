from flask.views import MethodView
from flask_security import SQLAlchemyUserDatastore, hash_password
from flask_smorest import abort
from app.auth.schema import UserSchema
from app.shema import SuccessSchema
from app.database import db, User, Role
from flask_security import auth_required, roles_required
from faker import Faker
from app.auth import blp


@blp.route('/sign-up')
class UserModel(MethodView):
    def __init__(self):
        self.user_datastore = SQLAlchemyUserDatastore(db, User, Role)

    fake = Faker()
    exemple = {
        'email': fake.email(),
        'password': fake.password(),
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'username': fake.user_name(),
        'roles': ["Librerian"]
    }
    exemple1 = {'response': 'New user created successfully'}

    @blp.arguments(UserSchema, location='json', description='Passing required user informations, email, password, '
                                                            'first_name, last_name, username', required=True,
                   as_kwargs=True,
                   example=exemple)
    @blp.response(201, SuccessSchema, description='New user created successfully', example=exemple1)
    @auth_required("token")
    @roles_required("Admin")
    def post(self, **kwargs):
        try:
            email = kwargs["email"]
            password = kwargs["password"]
            first_name = kwargs["first_name"]
            last_name = kwargs["last_name"]
            username = kwargs["username"]
            roles = kwargs["roles"]
            print(roles)
        except Exception as e:
            abort(404, message=str(e))
        else:
            if email is None or password is None or first_name is None or last_name is None or username is None or roles is None:
                abort(404, message="Missing required field(s)")
            else:
                if roles not in ["Librerian", "User", "Admin"]:
                    abort(404, message="Role has to be Librerian, User or Admin")
                else:
                    try:
                        self.user_datastore.create_user(
                            email=email,
                            password=hash_password(password),
                            first_name=first_name,
                            last_name=last_name,
                            username=username,
                            roles=[roles]
                        )
                        db.session.commit()
                    except Exception as e:
                        abort(404, message=str(e))
                    else:
                        return {"message": f"{roles} created successfully"}, 201
