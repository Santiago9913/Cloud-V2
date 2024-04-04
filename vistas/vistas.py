from flask_restful import Resource
from flask import request
from modelos import User, db
from werkzeug.security import generate_password_hash

class VistaSignUp(Resource):

    def post(self):
        username = request.json["username"]
        password1 = request.json['password1']
        password2 = request.json['password2']
        email = request.json['email']

        if not username or not password1 or not password2 or not email:
            return {'message': 'All fields must be filled'}, 400

        user = User.query.filter((User.username == username) | (User.email == email)).first()

        if user is None:
            if password1 == password2:
                encrypted_password = generate_password_hash(password1)
                user = User(username=username, password=encrypted_password, email=email)
                db.session.add(user)
                db.session.commit()
                return {'message': 'User created successfully'}, 201
            else:
                return {'message': 'Passwords do not match'}, 400
        else:
            return {'message': 'User already exists'}, 409
