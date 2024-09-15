from os import environ
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

#Generic Class for sql
class Base(DeclarativeBase):
    pass

app = Flask(__name__)

#This should be an a git ignored flaskenvironment
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')
app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY')



#New SQLAlchemy Class a constructor function
db = SQLAlchemy(model_class=Base)
#Method call and pass in the app.
db.init_app(app)

#Instance of Marshmallow,bcrypt,jwt and pass the app.
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)