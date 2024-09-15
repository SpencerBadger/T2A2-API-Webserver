from datetime import date
from typing import Optional
from init import db,ma
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String,Text, ForeignKey
from init import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp

class Show(db.Model):
    __tablename__ = 'shows'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text)
    date_created: Mapped[date] = mapped_column(default=date.today)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship('User', back_populates='shows')

class ShowSchema(ma.Schema):
    title = fields.String(required=True, validate=Regexp('^[0-9a-zA-Z ]+$'))
    user = fields.Nested("UserSchema", exclude=['password'])

    class Meta:
        fields = ('id', 'title', 'description', 'date_created', 'user_id')
