from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS  # Import CORS
import pandas
USER_NOT_FOUND_MESSAGE = 'user not found'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)
CORS(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {'id': self.id,'username': self.username, 'email': self.email}

db.create_all()

#create a test route
@app.route('/test', methods=['GET'])
def test():
  return make_response(jsonify({'message': 'test route'}), 200)


# create a user
@app.route('/users', methods=['POST'])
def create_user():
  try:
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return make_response(jsonify({'message': 'user created'}), 201)
  except Exception as e:
    return make_response(jsonify({'message': f'error creating user: {e}'}), 500)

# get all users
@app.route('/users', methods=['GET'])
def get_users():
  try:
    users = User.query.all()
    return make_response(jsonify([user.json() for user in users]), 200)
  except Exception as e:
    return make_response(jsonify({'message': f'error getting users: {e}'}), 500)

# get a user by id
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
  try:
    user = User.query.filter_by(id=user_id).first()
    if user:
      return make_response(jsonify({'user': user.json()}), 200)
    return make_response(jsonify({'message': USER_NOT_FOUND_MESSAGE}), 404)
  except Exception as e:
    return make_response(jsonify({'message': f'error getting user: {e}'}), 500)

# update a user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
  try:
    user = User.query.filter_by(id=user_id).first()
    if user:
      data = request.get_json()
      user.username = data['username']
      user.email = data['email']
      db.session.commit()
      return make_response(jsonify({'message': 'user updated'}), 200)
    return make_response(jsonify({'message': USER_NOT_FOUND_MESSAGE}), 404)
  except Exception as e:
    return make_response(jsonify({'message': f'error updating user: {e}'}), 500)

# delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
  try:
    user = User.query.filter_by(id=user_id).first()
    if user:
      db.session.delete(user)
      db.session.commit()
      return make_response(jsonify({'message': 'user deleted'}), 200)
    return make_response(jsonify({'message': USER_NOT_FOUND_MESSAGE}), 404)
  except Exception as e:
    return make_response(jsonify({'message': f'error deleting user: {e}'}), 500)

#create a new test route for weather response
@app.route('/newtest', methods=['GET'])
def newtest():
  return make_response(jsonify({'message': 'new test route for weather response'}), 200)
