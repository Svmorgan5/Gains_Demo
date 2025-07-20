from . import subscriptions_bp
from backend.models import GymSubscription, db, SubscriptionPlan, Member
from backend.blueprints.gymSubscriptions.subscriptionsSchemas import gym_subscription_schema, gym_subscriptions_schema, gym_subscription_update_schema
from flask import request, jsonify
from backend.utils.utils import token_required
from sqlalchemy import select
from marshmallow import ValidationError

# ---------------------------
# Gym views all its subscriptions
# ---------------------------
@subscriptions_bp.route("/gym", methods=["GET"])
@token_required
def get_gym_subscriptions(gym_id):
    # Query all subscriptions for the current gym
    query = select(GymSubscription).where(GymSubscription.gym_id == gym_id)
    subscriptions = db.session.execute(query).scalars().all()
    return gym_subscriptions_schema.jsonify(subscriptions), 200

# ---------------------------
# Member views all their subscriptions
# ---------------------------
@subscriptions_bp.route("/member", methods=["GET"])
@token_required
def get_member_subscriptions(member_id):
    # Query all subscriptions for the current member
    query = select(GymSubscription).where(GymSubscription.member_id == member_id)
    subscriptions = db.session.execute(query).scalars().all()
    return gym_subscriptions_schema.jsonify(subscriptions), 200

# ---------------------------
# Update a subscription (gym or member can update)
# ---------------------------
@subscriptions_bp.route("/<int:subscription_id>", methods=["PUT"])
@token_required
def update_subscription(user_id, subscription_id):
    # Find the subscription by ID
    subscription = db.session.get(GymSubscription, subscription_id)
    if not subscription:
        return jsonify({"error": "Subscription not found"}), 404

    try:
        # Load update data, allowing partial updates
        update_data = gym_subscription_update_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Update the subscription fields with new data
    for key, value in update_data.items():
        setattr(subscription, key, value)

    db.session.commit()
    return gym_subscription_schema.jsonify(subscription), 200

# ---------------------------
# Cancel a subscription (gym or member can delete)
# If a member has no other subscriptions after deletion, remove the member too
# ---------------------------
@subscriptions_bp.route("/<int:subscription_id>", methods=["DELETE"])
@token_required
def delete_subscription(user_id, subscription_id):
    # Find the subscription by ID
    subscription = db.session.get(GymSubscription, subscription_id)
    if not subscription:
        return jsonify({"error": "Subscription not found"}), 404

    member_id = subscription.member_id

    # Delete the subscription
    db.session.delete(subscription)
    db.session.commit()

    # Check if the member has any other subscriptions left
    remaining_subs = db.session.execute(
        select(GymSubscription).where(GymSubscription.member_id == member_id)
    ).scalars().all()

    # If no subscriptions remain, delete the member as well
    if not remaining_subs:
        member = db.session.get(Member, member_id)
        if member:
            db.session.delete(member)
            db.session.commit()

    return jsonify({"message": "Subscription deleted and member removed if no other subscriptions"}), 200