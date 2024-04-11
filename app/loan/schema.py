import marshmallow as ma


class LoanPostSchema(ma.Schema):
    copie = ma.fields.Integer(required=True)


class LoanGetSchema(ma.Schema):
    id = ma.fields.Integer(required=True)
    copie = ma.fields.Integer(required=True)
    user = ma.fields.Integer(required=True)
    date_loaned = ma.fields.DateTime(required=True)
    date_due = ma.fields.DateTime(required=True)
    loan_status = ma.fields.Integer(required=True)
