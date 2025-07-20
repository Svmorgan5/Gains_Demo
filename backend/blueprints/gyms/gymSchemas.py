from dataclasses import fields
from backend.models import Gym, db
from backend.extensions import ma
from marshmallow import fields

class GymSchema(ma.SQLAlchemyAutoSchema):
    
    password = fields.String(
        load_only=True,
        required=True, 
        validate=lambda p: len(p) >= 8
    )
    
    password_hash = fields.String(
        dump_only=True
    )

    class Meta:
        model = Gym
        load_instance = False    # return a dict from .load()
        # No exclude needed—explicit fields above override default behavior


gym_schema = GymSchema()
gyms_schema = GymSchema(many=True)
login_schema = GymSchema(exclude=['name', 'contact_number'])

class PublicGymSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Gym
        exclude = ("password_hash", "id")
        load_instance = True
public_gym_schema = PublicGymSchema()
public_gyms_schema = PublicGymSchema(many=True)
