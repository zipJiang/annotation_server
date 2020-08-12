"""Define different model to be
used for database.
"""
from datetime import datetime
from typing import Text
from . import db
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class AnnotationResult(db.Model):
    """To store the annotation result in a relational dataset.
    """
    __tablename__ = 'annotation_results'
    id = db.Column(db.Integer, primary_key=True)
    progress_id = db.Column(db.Integer, db.ForeignKey('progresses.id'))
    result = db.Column(db.Text())
    row_id = db.Column(db.Integer)


class Progress(db.Model):
    """This model is used to recognize the
    relationship of a single user on a single
    file (one-to-one user, many-to-one file)
    """
    __tablename__ = 'progresses'
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    results = db.relationship('AnnotationResult', backref='progress',
                              lazy='dynamic')


class AnnotationContent(db.Model):
    """A structure to store content for every hit in a row.
    """
    __tablename__ = 'annotation_content'
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'))
    content = db.Column(db.Text())
    row_id = db.Column(db.Integer)


class File(db.Model):
    """A list of files related to the roles.
    """
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    hit_num = db.Column(db.Integer)
    filename = db.Column(db.Text(), unique=True, index=True)
    taskname = db.Column(db.Text(), unique=True, index=True)
    description = db.Column(db.Text())
    progresses = db.relationship('Progress', backref='file', lazy='dynamic')
    annotation_contents = db.relationship('AnnotationContent',
                                          backref='file', lazy='dynamic')
    # also we neewd information about the template.
    # we put it here because we only have to initialize it once
    template = db.Column(db.Text())

    def __repr__(self):
        return '<File %r>' % self.filename


class Role(db.Model):
    """Roles to be assigned to users.
    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model, UserMixin):
    """User model.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    progresses = db.relationship('Progress', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password: Text):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def ping(self):
        """Setting the last time of visit.
        """
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        # Why here we don't need commit?


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
