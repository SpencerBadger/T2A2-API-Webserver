from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from init import db
from models.user import User
from flask import abort, jsonify, make_response

def admin_only(fn):
    """ Check admin

    The database is queried for a user with an id that matches
    the id in the JWT and that also has a true admin value
    """
    @jwt_required()
    def inner(*args, **kwargs):
        user_id = get_jwt_identity()
        stmt = db.select(User).where(User.id == user_id, User.is_admin == True)
        user = db.session.scalar(stmt)

        if user:
            return fn(*args, **kwargs)
        else:
            return jsonify({"error": "You must be an admin to access this resource"}), 403
    return inner

def authorize_owner(Show):
    user_id = get_jwt_identity()
    if user_id != Show.user_id:
        abort(make_response(jsonify(error="You must be the Show owner to access this resource"),403))
