#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User, UserSchema

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204
    
class Signup(Resource):
    
    def post(self):
        data = request.get_json()

        # create new user
        user = User(username = data["username"])
        user.password_hash = data["password"]

        # save the user to db
        db.session.add(user)
        db.session.commit()

        # log in by storing user_id in the session
        session['user_id'] = user.id

        # return user object
        return UserSchema().dump(user), 201

class CheckSession(Resource):

    def get(self):
        # query to find the user, using the User.id against the session user_id
        user = User.query.filter(User.id == session.get("user_id")).first()


        if user:
            return UserSchema().dump(user), 201
        else:
            return {}, 204
        
class Login(Resource):

    def post(self):
        username = request.get_json().get("username")
        user = User.query.filter_by(username=username).first()

        if user:
            session["user_id"] = user.id
            return {'id': user.id, 'username': user.username}, 200
        else:
            return {'message': 'Invalid login'}, 401
        
class Logout(Resource):

    def delete(self):
        cleared = session['user_id'] = None
        return cleared, 204

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup')
api.add_resource(CheckSession, '/check_session')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
