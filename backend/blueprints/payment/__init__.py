from flask import Blueprint

payment_bp = Blueprint("payment", __name__)

from . import routes  # Import your routes after defining the blueprint