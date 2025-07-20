from . import subscriptions_bp
from backend.models import GymSubscription, db, SubscriptionPlan, Member
from backend.blueprints.gymSubscriptions.subscriptionsSchemas import gym_subscription_schema, gym_subscriptions_schema, gym_subscription_update_schema
from flask import request, jsonify
from backend.utils.utils import token_required
from sqlalchemy import select
from marshmallow import ValidationError

# GET: Gym views all its subscriptions
@subscriptions_bp.route("/gym", methods=["GET"])
@token_required
def get_gym_subscriptions(gym_id):
    query = select(GymSubscription).where(GymSubscription.gym_id == gym_id)
    subscriptions = db.session.execute(query).scalars().all()
    return gym_subscriptions_schema.jsonify(subscriptions), 200

# GET: Member views all their subscriptions
@subscriptions_bp.route("/member", methods=["GET"])
@token_required
def get_member_subscriptions(member_id):
    query = select(GymSubscription).where(GymSubscription.member_id == member_id)
    subscriptions = db.session.execute(query).scalars().all()
    return gym_subscriptions_schema.jsonify(subscriptions), 200

# PUT: Update a subscription (gym or member can update)
@subscriptions_bp.route("/<int:subscription_id>", methods=["PUT"])
@token_required
def update_subscription(user_id, subscription_id):
    subscription = db.session.get(GymSubscription, subscription_id)
    if not subscription:
        return jsonify({"error": "Subscription not found"}), 404

    try:
        update_data = gym_subscription_update_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for key, value in update_data.items():
        setattr(subscription, key, value)

    db.session.commit()
    return gym_subscription_schema.jsonify(subscription), 200

# DELETE- Cancel a subscription (gym or member can delete)
@subscriptions_bp.route("/<int:subscription_id>", methods=["DELETE"])
@token_required
def delete_subscription(user_id, subscription_id):
    subscription = db.session.get(GymSubscription, subscription_id)
    if not subscription:
        return jsonify({"error": "Subscription not found"}), 404

    member_id = subscription.member_id

    db.session.delete(subscription)
    db.session.commit()

    # Check if the member has any other subscriptions
    remaining_subs = db.session.execute(
        select(GymSubscription).where(GymSubscription.member_id == member_id)
    ).scalars().all()

    if not remaining_subs:
        member = db.session.get(Member, member_id)
        if member:
            db.session.delete(member)
            db.session.commit()

    return jsonify({"message": "Subscription deleted and member removed if no other subscriptions"}), 200