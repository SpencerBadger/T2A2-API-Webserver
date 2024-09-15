from flask import Blueprint, request
from init import db
from models.show import Show, ShowSchema
from auth import authorize_owner
from datetime import date
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity 
)

shows_bp = Blueprint('shows',__name__,url_prefix='/shows')

@shows_bp.route('/<int:id>')
def one_Show(id):
    """
    Get one Show by ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the Show
    """
    show = db.session.get(Show,id)
    if not show:
        abort(404,description=f'Show with id {id} not found')
    return ShowSchema().dump(show), 200

@shows_bp.route('/')
def all_Shows():
    """
    Get all Shows
    ---
    """
    stmt = db.select(Show)
    Shows = db.session.scalars(stmt).all()
    return ShowSchema(many=True, only=['id','title','description','date_created']).dump(Shows)

@shows_bp.route('/', methods=['POST'])
@jwt_required()
def create_Show():
    """
    Create a new Show
    ---
    """
    show_info = ShowSchema(only=['title']).load(request.json, unknown='exclude')
    show = Show(
        title=show_info['title'],
        description=show_info.get('description', ''),
        date_created=date.today(),
        user_id=get_jwt_identity()
    )
    db.session.add(show)
    db.session.commit()
    return ShowSchema().dump(show), 201

@shows_bp.route('/<int:id>', methods=['PUT','PATCH'])
@jwt_required()
def update_Show(id):
    """
    Update a Show by ID
    ---
    """
    show = db.session.get(Show, id)
    if not show:
        abort(404, description=f'Show with id {id} not found')
    authorize_owner(show)
    
    show_info = ShowSchema(only=['title']).load(request.json, unknown='exclude')
    show.title = show_info.get('title', show.title)
    show.description = show_info.get('description', show.description)
    
    db.session.commit()
    return ShowSchema().dump(show), 200


@shows_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_Show(id):
    """
    Delete a Show by ID
    ---
    """
    show = db.session.get(Show, id)
    if not show:
        abort(404, description=f'Show with id {id} not found')
    authorize_owner(show)

    
    db.session.delete(show)
    db.session.commit()
    return {
        "message": f"Show with id {id} has been successfully deleted.",
        "Success": True
    }, 200
