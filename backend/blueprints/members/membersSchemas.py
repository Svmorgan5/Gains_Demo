from dataclasses import fields
from backend.models import Member, db
from backend.extensions import ma
from marshmallow import fields

class MemberSchema(ma.SQLAlchemyAutoSchema):
    subscription_name = fields.String(required=True)
    password = fields.String(
        load_only=True,
        required=True, 
        validate=lambda p: len(p) >= 8
    )
    password_hash = fields.String(
        dump_only=True
    )
    class Meta:
        model = Member
        load_instance = False    # return a dict from .load()
        # No exclude needed—explicit fields above override default behavior

class MemberCreateSchema(MemberSchema):
    subscription_name = fields.String(required=True)
    # You can add validation to restrict to allowed values if you want


member_schema = MemberSchema()
members_schema = MemberSchema(many=True)
login_schema = MemberSchema(exclude=['name'])
member_create_schema = MemberCreateSchema()