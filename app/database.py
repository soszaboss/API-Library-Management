from sqlalchemy.orm import Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship, backref
from sqlalchemy import DateTime, Column, Integer, String, ForeignKey, TEXT, Date
from sqlalchemy.sql import func


# Initialize the Extension

db = SQLAlchemy()


class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(TEXT())
    permissions = Column(ARRAY(String), nullable=True)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True)
    password = Column(String(255), nullable=False)
    first_name = Column(String(50), unique=False, nullable=False)
    last_name = Column(String(50), unique=False, nullable=False)
    username = Column(String(50), unique=True, nullable=True)
    created_at = Column(DateTime(), default=func.now())
    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User %r>' % self.username


class Book(db.Model):
    __tablename__ = 'book'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    auteur: Mapped[str] = mapped_column(String(50), nullable=False, default='Unknown')
    date_published = Column(Date(), nullable=True)
    genre: Mapped[str] = mapped_column(TEXT(),nullable=True)
    image: Mapped[str] = mapped_column(nullable=True)
    isbn10: Mapped[str] = mapped_column(nullable=True, default=None)
    isbn15: Mapped[str] = mapped_column(nullable=True, default=None)
    description: Mapped[str] = mapped_column(TEXT(),nullable=True)
    pages: Mapped[int] = mapped_column(nullable=True)
    language: Mapped[str] = mapped_column(nullable=True, default='Unknown')
    publisher: Mapped[str] = mapped_column(nullable=True, default=None)

    def __repr__(self):
        return '<Book %r>' % self.title


class State(db.Model):
    __tablename__ = 'book_state'
    id = Column(Integer, primary_key=True)
    state: Mapped[str] = mapped_column(String(15), unique=True)
    description = Column(TEXT())

    def __repr__(self):
        return '<State %r>' % self.state


class Copie(db.Model):
    __tablename__ = 'copie'
    id: Mapped[int] = mapped_column(primary_key=True)
    book: Mapped[int] = mapped_column(ForeignKey("book.id"))
    state: Mapped[int] = mapped_column(ForeignKey("book_state.id"))
    available: Mapped[bool] = mapped_column(default=True)

    def __repr__(self):
        return '<Copies %r>' % self.available


class Loan(db.Model):
    __tablename__ = 'loan'
    id: Mapped[int] = mapped_column(primary_key=True)
    copie: Mapped[int] = mapped_column(ForeignKey("copie.id"))
    user: Mapped[int] = mapped_column(ForeignKey('user.id'))
    date_loaned = Column(DateTime(), default=func.now())
    goback_date = Column(DateTime())
