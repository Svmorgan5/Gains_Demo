from . import members_bp
from .membersSchemas import member_schema, members_schema, login_schema, member_create_schema
from backend.models import Gym, Member, GymSubscription, db
from flask import request, jsonify
from backend.utils.utils import encode_token, decode_token, token_required
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import ValidationError
from sqlalchemy import select
from datetime import date
from backend.models import SubscriptionPlan

# ---------------------------
# Member Login Route
# ---------------------------
@members_bp.route("/login", methods=["POST"])
def login_member():
    try:
        # Only require email and password for login
        credentials = login_schema.load(request.json, partial=("name", "phone"))
        email = credentials['email']
        password = credentials['password']
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Find member by email
    query = select(Member).where(Member.email == email)
    member = db.session.execute(query).scalars().first()

    # Check password and return token if valid
    if member and check_password_hash(member.password_hash, password):
        token = encode_token(member.id)
        response = {
            "status": "success",
            "message": "Login successful",
            "token": token
        }
        return jsonify(response), 200
    else:
        return jsonify({"message": "Invalid email or password!"}), 401

# ---------------------------
# Create a new member (must be called by a gym)
# ---------------------------
@members_bp.route("/", methods=["POST"])
@token_required
def create_member(gym_id):
    try:
        # Validate and load member data from request
        member_data = member_create_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Prevent duplicate members by email
    query = select(Member).where(Member.email == member_data["email"])
    if db.session.execute(query).scalars().first():
        return jsonify({"error": "Member already exists with this email"}), 400

    # Hash the password before saving
    password = member_data.pop("password")
    member_data["password_hash"] = generate_password_hash(password)

    # Get subscription plan name from payload
    subscription_name = member_data.pop("subscription_name")

    # Create the member record
    new_member = Member(**member_data)
    db.session.add(new_member)
    db.session.commit()

    # Create a subscription for the new member to this gym
    new_subscription = GymSubscription(
        gym_id=gym_id,
        member_id=new_member.id,
        subscription_name=SubscriptionPlan(subscription_name),  # Convert string to Enum
        start_date=date.today()
    )
    db.session.add(new_subscription)
    db.session.commit()

    return member_schema.jsonify(new_member), 201

# ---------------------------
# Get member details and all their subscriptions
# ---------------------------
@members_bp.route("/me", methods=["GET"])
@token_required
def get_member_details(member_id):
    # Get the member by their ID from the token
    member = db.session.get(Member, member_id)
    if not member:
        return jsonify({"error": "Member not found"}), 404

    # Get all subscriptions for this member
    subscriptions = db.session.execute(
        select(GymSubscription).where(GymSubscription.member_id == member_id)
    ).scalars().all()

    # Serialize member and subscriptions for response
    member_json = member_schema.dump(member)
    member_json["subscriptions"] = [
        {
            "gym_name": sub.gym.name,
            "subscription_name": sub.subscription_name.value if hasattr(sub.subscription_name, "value") else sub.subscription_name,
            "start_date": sub.start_date,
            "end_date": sub.end_date
        }
        for sub in subscriptions
    ]

    return jsonify(member_json), 200

# ---------------------------
# Update member profile
# ---------------------------
@members_bp.route("/me", methods=["PUT"])
@token_required
def update_member(member_id):
    try:
        # Allow partial updates for member info
        member_data = member_schema.load(request.json, partial=("email", "name", "phone"))
    except ValidationError as e:
        return jsonify(e.messages), 400

    member = db.session.get(Member, member_id)
    if not member:
        return jsonify({"error": "Member not found"}), 404

    # Update member fields with new data
    for key, value in member_data.items():
        setattr(member, key, value)

    db.session.commit()
    return member_schema.jsonify(member), 200

# ---------------------------
# Delete member account (self-delete)
# ---------------------------
@members_bp.route("/me", methods=["DELETE"])
@token_required
def delete_member(member_id):
    member = db.session.get(Member, member_id)
    if not member:
        return jsonify({"error": "Member not found"}), 404

    db.session.delete(member)
    db.session.commit()
    return jsonify({"message": "Member deleted successfully"}), 200

# ---------------------------
# Gym removes a member from its own gym
# If member has no other subscriptions, delete member entirely
# ---------------------------
@members_bp.route("/<int:member_id>", methods=["DELETE"])
@token_required
def gym_delete_member(gym_id, member_id):
    # Find the subscription linking this member to this gym
    subscription = db.session.execute(
        select(GymSubscription).where(
            GymSubscription.gym_id == gym_id,
            GymSubscription.member_id == member_id
        )
    ).scalars().first()

    if not subscription:
        return jsonify({"error": "Member not found in this gym"}), 404

    # Remove the subscription
    db.session.delete(subscription)
    db.session.commit()

    # If member has no other subscriptions, delete member record
    remaining_subs = db.session.execute(
        select(GymSubscription).where(GymSubscription.member_id == member_id)
    ).scalars().all()

    if not remaining_subs:
        member = db.session.get(Member, member_id)
        if member:
            db.session.delete(member)
            db.session.commit()

    return jsonify({"message": "Member removed from gym (and deleted if no other subscriptions)"}), 200