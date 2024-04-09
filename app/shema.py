import marshmallow as ma


class SuccessSchema(ma.Schema):
    message = ma.fields.String()
