from . import payment_bp
from backend.models import Payment, GymSubscription, db
from backend.blueprints.payment.paymentSchemas import payment_schema, payments_schema
from flask import request, jsonify
from backend.utils.utils import token_required
from sqlalchemy import select
from marshmallow import ValidationError

# ---------------------------
# Get all payments for a specific subscription
# Accessible by gym or member
# ---------------------------
@payment_bp.route("/subscription/<int:subscription_id>", methods=["GET"])
@token_required
def get_payments_for_subscription(user_id, gym_subscription_id):
    # Query all payments linked to this subscription
    payments = db.session.execute(
        select(Payment).where(Payment.gym_subscription_id == gym_subscription_id)
    ).scalars().all()
    return payments_schema.jsonify(payments), 200

# ---------------------------
# Get all payments for the authenticated member
# ---------------------------
@payment_bp.route("/member", methods=["GET"])
@token_required
def get_member_payments(member_id):
    # Find all subscriptions for this member
    subs = db.session.execute(
        select(GymSubscription.id).where(GymSubscription.member_id == member_id)
    ).scalars().all()
    # Get all payments linked to those subscriptions
    payments = db.session.execute(
        select(Payment).where(Payment.gym_subscription_id.in_(subs))
    ).scalars().all()
    return payments_schema.jsonify(payments), 200

# ---------------------------
# Get all payments for the authenticated gym
# ---------------------------
@payment_bp.route("/gym", methods=["GET"])
@token_required
def get_gym_payments(gym_id):
    # Find all subscriptions for this gym
    subs = db.session.execute(
        select(GymSubscription.id).where(GymSubscription.gym_id == gym_id)
    ).scalars().all()
    # Get all payments linked to those subscriptions
    payments = db.session.execute(
        select(Payment).where(Payment.gym_subscription_id.in_(subs))
    ).scalars().all()
    return payments_schema.jsonify(payments), 200

# ---------------------------
# Create a payment for a subscription
# ---------------------------
@payment_bp.route("/subscription/<int:subscription_id>", methods=["POST"])
@token_required
def create_payment(user_id, subscription_id):
    try:
        # Validate payment data from request
        data = payment_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Create the payment record
    new_pay = Payment(
        gym_subscription_id = subscription_id,
        amount              = data["amount"],
        status              = data.get("status", "paid")
    )
    db.session.add(new_pay)
    db.session.commit()
    return payment_schema.jsonify(new_pay), 201

# ---------------------------
# Delete a payment (admin or authorized user)
# ---------------------------
@payment_bp.route("/<int:payment_id>", methods=["DELETE"])
@token_required
def delete_payment(user_id, payment_id):
    # Find the payment by ID
    payment = db.session.get(Payment, payment_id)
    if not payment:
        return jsonify({"error": "Payment not found"}), 404

    # Delete the payment record
    db.session.delete(payment)
    db.session.commit()
    return jsonify({"message": "Payment deleted"}), 200