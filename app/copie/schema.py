import marshmallow as ma


class CopieGetSchema(ma.Schema):
    id = ma.fields.Integer()
    title = ma.fields.String()
    state = ma.fields.String()
    available = ma.fields.Bool()


class CopiePostSchema(ma.Schema):
    book = ma.fields.Integer(required=True)
    state = ma.fields.Integer(required=True)
    available = ma.fields.Bool(required=True)

class CopieIdSchema(ma.Schema):
    id = ma.fields.Integer(required=True)