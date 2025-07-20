# backend/blueprints/payment/paymentSchemas.py
from backend.models import Payment
from backend.extensions import ma
from marshmallow import fields

class PaymentSchema(ma.SQLAlchemyAutoSchema):
    member_name = fields.Function(lambda p: p.gym_subscription.member.name)
    paid_at     = fields.DateTime(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Payment
        load_instance = False
        #include_fk = True
        exclude = ("gym_subscription_id",)

    amount = fields.Float(required=True)
    status = fields.String(load_default="paid")

payment_schema = PaymentSchema()
payments_schema = PaymentSchema(many=True)
