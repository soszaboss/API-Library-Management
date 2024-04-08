import marshmallow as ma


class UserSchema(ma.Schema):
    email = ma.fields.String()
    password = ma.fields.String()
    first_name = ma.fields.String()
    last_name = ma.fields.String()
    username = ma.fields.String()
    roles = ma.fields.String()


class SuccessSchema(ma.Schema):
    message = ma.fields.String()
