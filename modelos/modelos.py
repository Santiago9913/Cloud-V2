import enum
import datetime
from sqlalchemy import Enum
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True

class Extension(enum.Enum):
    MP4 = 'mp4'
    MOV = 'mov'
    WMV = 'wmv'
    AVI = 'avi'

class Status(enum.Enum):
    UPLOADED = 'uploaded'
    PROCESSED = 'processed'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    filename = db.Column(db.String(128), nullable=False)
    extension = db.Column(Enum(Extension), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    modified_at = db.Column(db.DateTime, onupdate=datetime.datetime.now())
    status = db.Column(Enum(Status), nullable=False, default=Status.UPLOADED)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class EnumField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return value.value.upper()

class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_relationships = True
        load_instance = True

    extension = EnumField()
    status = EnumField()