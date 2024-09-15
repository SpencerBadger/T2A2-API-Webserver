from datetime import timedelta
from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, UserSchema
from flask_jwt_extended import create_access_token
from auth import admin_only

users_bp = Blueprint('users',__name__,url_prefix='/users')

@users_bp.route('/login', methods=['POST'])
def login():
    """
    User login
    """
    parameters = UserSchema(only=['email', 'password']).load(request.json, unknown='exclude')
    stmt = db.select(User).where(User.email == parameters['email'])
    user = db.session.scalar(stmt)

    if user and bcrypt.check_password_hash(user.password,parameters['password']):
        token = create_access_token(identity=user.id, expires_delta=timedelta(hours=2))
        return {'token': token}
    else:
        return {'error': 'Invalid password'}, 401

@users_bp.route('/', methods=['POST'])
@admin_only
def create_user():
    """
    Create a new user
    """
    user_info = UserSchema(only=['email', 'password', 'name', 'is_admin']).load(request.json, unknown='exclude')

    # Hash the user's password before saving it
    hashed_password = bcrypt.generate_password_hash(user_info['password']).decode('utf-8')

    user = User(
        email=user_info['email'],
        password=hashed_password,  # Save hashed password
        name=user_info.get('name'),
        is_admin=user_info.get('is_admin', False)  # Default to False if is_admin not provided
    )
    
    db.session.add(user)
    db.session.commit()

    # Do not return the password in the response
    return UserSchema(exclude=['password']).dump(user), 201

@users_bp.route('/')
def list_users():
    """
    Retrieve all users.
    """
    stmt = db.select(User)
    Users = db.session.scalars(stmt).all()
    return UserSchema(many=True, only=['id','email','password','name','is_admin']).dump(Users)

@users_bp.route('/<int:id>', methods=['DELETE'], endpoint='delete_user')
@admin_only
def delete_User(id):
    """
    Delete a User by ID
    ---
    """
    user = db.session.get(User, id)
    if not user:
        abort(404, description=f'User with id {id} not found')

    db.session.delete(user)
    db.session.commit()
    return {
        "message": f"User with id {id} has been successfully deleted.",
        "success": True
    }, 200