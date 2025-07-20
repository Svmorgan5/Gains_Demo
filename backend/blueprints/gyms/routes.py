from . import gyms_bp
from .gymSchemas import gym_schema, login_schema, public_gyms_schema, public_gym_schema
from backend.blueprints.members.membersSchemas import member_schema, members_schema
from backend.models import Gym, Member, GymSubscription, db
from flask import request, jsonify
from backend.utils.utils import encode_token, decode_token, token_required
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import ValidationError
from sqlalchemy import select



@gyms_bp.route("/login", methods=["POST"])
def login_gym():
    try:
        # Only require email and password for login
        credentials = gym_schema.load(request.json, partial=("name", "contact_number", "location"))
        email = credentials['email']
        password = credentials['password']
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Gym).where(Gym.email == email)
    gym = db.session.execute(query).scalars().first()

    if gym and check_password_hash(gym.password_hash, password):
        token = encode_token(gym.id)
        response = {
            "status": "success",
            "message": "Login successful",
            "token": token
        }
        return jsonify(response), 200
    else:
        return jsonify({"message": "Invalid email or password!"}), 401

@gyms_bp.route("/", methods=["POST"])
def create_gym():
    try:
        gym_data = gym_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    
    query = select(Gym).where(Gym.email == gym_data["email"])
    if db.session.execute(query).scalars().first():
        return jsonify({"error": "Gym already exists with this email"}), 400

    new_gym = Gym(
        name           = gym_data["name"],
        contact_number = gym_data.get("contact_number"),
        email          = gym_data["email"],
        location       = gym_data["location"],
        password_hash  = generate_password_hash(gym_data["password"])
    )

    db.session.add(new_gym)
    db.session.commit()
    return gym_schema.jsonify(new_gym), 201

@gyms_bp.route("/", methods=["GET"])
def get_all_gyms():
    gyms= db.session.execute(select(Gym)).scalars().all()
    return public_gyms_schema.jsonify(gyms), 200

@gyms_bp.route("/<int:gym_id>", methods=["GET"])
def get_gym_by_id(gym_id):
    gym = db.session.get(Gym, gym_id)
    if not gym:
        return jsonify({"error": "Gym not found"}), 404
    return public_gym_schema.jsonify(gym), 200

@gyms_bp.route("/members", methods=["GET"])
@token_required
def get_gym_members(gym_id):
    # Get all member IDs for this gym from GymSubscription
    sub_query = select(GymSubscription.member_id).where(GymSubscription.gym_id == gym_id)
    member_ids = [row[0] for row in db.session.execute(sub_query).all()]

    # Now get all members with those IDs
    if member_ids:
        query = select(Member).where(Member.id.in_(member_ids))
        members = db.session.execute(query).scalars().all()
    else:
        members = []

    return members_schema.jsonify(members), 200

@gyms_bp.route("/update", methods=["PUT"])
@token_required
def update_gym(gym_id):
    gym = db.session.get(Gym, gym_id)
    if not gym:
        return jsonify({"error": "Gym not found"}), 404

    try:
        gym_data = gym_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Check for duplicate email
    new_email = gym_data.get("email")
    if new_email and new_email != gym.email:
        query = select(Gym).where(Gym.email == new_email)
        existing_gym = db.session.execute(query).scalars().first()
        if existing_gym:
            return jsonify({"error": "Email already in use by another gym"}), 400

    for key, value in gym_data.items():
        setattr(gym, key, value)

    db.session.commit()
    return gym_schema.jsonify(gym), 200

@gyms_bp.route("/delete", methods=["DELETE"])
@token_required
def delete_gym(gym_id):
    gym = db.session.get(Gym, gym_id)
    if not gym:
        return jsonify({"error": "Gym not found"}), 404

    db.session.delete(gym)
    db.session.commit()
    return jsonify({"message": "Gym deleted successfully"}), 200