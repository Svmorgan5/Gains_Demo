from backend.models import GymSubscription
from backend.extensions import ma
from marshmallow import fields

class GymSubscriptionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GymSubscription
        load_instance = True

    # Optionally, show gym name and member name in output
    gym_name = fields.String(attribute="gym.name", dump_only=True)
    member_name = fields.String(attribute="member.name", dump_only=True)

gym_subscription_schema = GymSubscriptionSchema()
gym_subscriptions_schema = GymSubscriptionSchema(many=True)

class GymSubscriptionUpdateSchema(ma.SQLAlchemySchema):
    # Only allow updating certain fields
    subscription_name = fields.String(required=False)
    end_date = fields.Date(required=False)

gym_subscription_update_schema = GymSubscriptionUpdateSchema()