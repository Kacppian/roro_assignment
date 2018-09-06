from project import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text as sa_text

# class Repository(db.Model):
#     id = db.Column(
#                    UUID(as_uuid=True),
#                    primary_key=True,
#                    server_default=sa_text("uuid_generate_v4()")
#                    )
#     name = db.Column(db.String(250), nullable=False, unique=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


# class User(db.Model):
#     __tablename__ = 'users'

#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(250), nullable=False, unique=True)
#     password = db.Column(db.String(250), nullable=False)
#     username = db.Column(db.String(250), nullable=False, unique=True)
#     active = db.Column(db.Integer, nullable=False)
#     repos = db.relationship('Repository', backref='user', lazy=True)
#     creation_time = db.Column(
#                               db.TIMESTAMP,
#                               server_default=db.func.current_timestamp(),
#                               nullable=False
#                               )

