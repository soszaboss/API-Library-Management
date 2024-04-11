import marshmallow as ma


class BookSGetchema(ma.Schema):
    id = ma.fields.Integer()
    title = ma.fields.String()
    auteur = ma.fields.String()
    date_published = ma.fields.Date()
    genre = ma.fields.String()
    image = ma.fields.String()
    isbn10 = ma.fields.String()
    isbn15 = ma.fields.String()
    description = ma.fields.String()
    pages = ma.fields.Integer()
    language = ma.fields.String()
    publisher = ma.fields.String()


class BookPostSchema(ma.Schema):
    title = ma.fields.String(required=True)
    auteur = ma.fields.String(required=True, default='Unknown')
    date_published = ma.fields.String(default=None)
    genre = ma.fields.String(default=None)
    image = ma.fields.String(default=None)
    isbn10 = ma.fields.String(default=None)
    isbn15 = ma.fields.String(default=None)
    description = ma.fields.String(default=None)
    pages = ma.fields.Integer(default=None)
    language = ma.fields.String(default=None)
    publisher = ma.fields.String(default=None)


class BookIdSchema(ma.Schema):
    id = ma.fields.Integer()
