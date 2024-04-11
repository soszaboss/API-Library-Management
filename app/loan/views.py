from datetime import datetime, timedelta
from sqlalchemy import select
from flask_smorest import abort
from app.database import db, Loan, Copie
from flask.views import MethodView
from app.loan import blp
from app.loan.schema import LoanGetSchema, LoanPostSchema
from flask_security import current_user, roles_required, roles_accepted


@blp.route('loans/')
class LoansView(MethodView):
    @blp.response(200, LoanGetSchema(many=True), description='All Loans')
    @roles_required('Admin')
    def get(self):
        try:
            loans = Loan.query.all()
            return loans
        except Exception as e:
            abort(500, e)

    @blp.arguments(LoanPostSchema, location='json', as_kwargs=True)
    @blp.response(201, LoanGetSchema, description='New Loan')
    @roles_required('User')
    def post(self, **kwargs):
        try:
            copie = kwargs.get('copie')
            is_available = db.session.scalar(select(Copie).where(Copie.id == copie)).available
        except:
            abort(404, 'No such copies!')
        else:
            if is_available:
                try:
                    user_id = current_user.id
                    date_loaned = datetime.now()

                    # Ajoute 14 jours à date_loaned pour obtenir date_due
                    date_due = date_loaned + timedelta(days=14)

                    loan = Loan(copie=copie, user=user_id, date_loaned=date_loaned, date_due=date_due,
                                loan_status=3)
                    db.session.query(Copie).get(copie).available = False
                    db.session.add(loan)
                    db.session.flush()
                    loan_id = loan.id

                except Exception as e:
                    print(e)
                    abort(500, e)

                else:
                    db.session.commit()
                    q = Loan.query.get(loan_id)
                    return q
            else:
                abort(404, f'copie with id: {copie} is not available')

@blp.route('/<int:id>')
class LoansById(MethodView):

    @blp.response(200, LoanGetSchema)
    @roles_required('User')
    def get(self, id):
        # Récupère l'emprunt avec l'ID spécifié
        loan = Loan.query.get(id)
        if not loan:
            abort(404, f'Loan with id: {id} does not exist')
        return loan

    # @blp.arguments(LoanPostSchema, location='json')
    # @blp.response(200, LoanGetSchema)
    # def put(self, args, id):
    #     # Récupère l'emprunt avec l'ID spécifié
    #     loan = Loan.query.get(id)
    #     if not loan:
    #         abort(404, f'Loan with id: {id} does not exist')
    #
    #     # Met à jour les attributs de l'emprunt avec les valeurs fournies
    #     for key, value in args.items():
    #         setattr(loan, key, value)
    #
    #     # Enregistre les modifications dans la base de données
    #     db.session.commit()
    #
    #     return loan
