from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(16), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

    id = fields.String()
    username = fields.String()
    password = fields.String()
    email = fields.String()