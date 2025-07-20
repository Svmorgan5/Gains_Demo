from flask import Blueprint

gyms_bp = Blueprint('gyms_bp', __name__)

from . import routes 