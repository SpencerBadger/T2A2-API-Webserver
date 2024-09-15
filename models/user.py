from init import db,ma
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String,Boolean
from typing import Optional, List
from marshmallow import fields
from marshmallow.validate import Length

class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(200), unique=True)
    password: Mapped[str] = mapped_column(String(200))
    is_admin: Mapped[bool] = mapped_column(Boolean(), server_default='False')
    shows: Mapped[List['Show']] = relationship('Show',back_populates='user')

class UserSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(validate=Length(min=8), required=True)

    class Meta:
        fields = ('id', 'name', 'email','password', 'is_admin')