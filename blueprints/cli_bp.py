from datetime import date
from flask import Blueprint
from init import db,bcrypt
from models.user import User
from models.show import Show


db_commands = Blueprint('db',__name__)

@db_commands.cli.command('create')
def db_create():
    db.drop_all()
    db.create_all()
    print('created tables')
    users = [
        User(
            email='administrator1@shows.com',
            name='Administrator',
            password=bcrypt.generate_password_hash('showadmin').decode('utf-8'),
            is_admin=True
            ),
        User(
            email='showUser@Show.com',
            name='John Doe',
            password=bcrypt.generate_password_hash('useradmin').decode('utf-8'),
            is_admin=False
            ),
    ]
    db.session.add_all(users)
    db.session.commit()

    shows = [
        Show(title='Bridge over the river',description='Action', date_created=date.today(),user_id=users[0].id),
        Show(title='Titanic',description='Romcom', date_created=date.today(),user_id=users[0].id),
        Show(title='Warcraft',description='Awesome', date_created=date.today(),user_id=users[0].id),
        Show(title='Bill and Ted',description='Excellent', date_created=date.today(),user_id=users[0].id),
        Show(title='Tsk Tsk',description='Silent', date_created=date.today(),user_id=users[1].id),
    ]
    
    db.session.add_all(shows)
    db.session.commit()

    print('Users created, Shows seeded.')
