from sqlalchemy_utils import UUIDType
from sqlalchemy.dialects.postgresql import JSONB

from zou.app import db
from zou.app.models.serializer import SerializerMixin
from zou.app.models.base import BaseMixin


class Comment(db.Model, BaseMixin, SerializerMixin):
    shotgun_id = db.Column(db.Integer)

    object_id = db.Column(UUIDType(binary=False), nullable=False)
    object_type = db.Column(db.String(80), nullable=False)
    text = db.Column(db.Text())
    data = db.Column(JSONB)

    person_id = db.Column(
        UUIDType(binary=False), db.ForeignKey("person.id"), nullable=False)

    def __repr__(self):
        return "<Comment of %s>" % self.object_id
