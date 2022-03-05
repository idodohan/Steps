from flask import Blueprint, request, jsonify
from src.database import User, db
from src.constants.http_status_codes import HTTP_201_CREATED, HTTP_409_CONFLICT

users_blueprint = Blueprint("users", __name__, url_prefix="/api/v1/users")


@users_blueprint.route('/register', methods=['POST'])
def register():
    """
    creates a new user and adds it to the db
    :return:
    """
    username = request.json['username']

    # if the user already exists
    if db.session.query(User).filter_by(username=username).first() is not None:
        return jsonify({'error': "username is taken"}), HTTP_409_CONFLICT

    # creates the user object
    user = User(username=username)

    # adds it to the db
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': "User created",
        'user': {
            'username': username
        }

    }), HTTP_201_CREATED



def get_user_by_id(id: int) ->  User:
    """
    :param id: user id
    :return: returns user with the matching id
    """
    user = User.query.get(id)
    if user:
        return user
