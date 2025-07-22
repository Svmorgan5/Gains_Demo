from flask import Flask, send_from_directory
from backend.models import db
from backend.extensions import ma, limiter, cache
from backend.blueprints.gyms import gyms_bp
from backend.blueprints.members import members_bp
from backend.blueprints.gymSubscriptions import subscriptions_bp
from backend.blueprints.payment import payment_bp
import os
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS


SWAGGER_URL = '/api/docs'
API_URL = '/swagger.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Gains Demo API"}
)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
    CORS(app)
    # add extensions
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    
#----------Docker support-----------
    @app.route("/")
    def index():
        return app.send_static_file("index.html")

    @app.route("/swagger.yaml")
    def swagger_yaml():
        root_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        return send_from_directory(root_dir, "swagger.yaml")
    
    #registering Blueprints
    app.register_blueprint(gyms_bp, url_prefix='/gyms')
    app.register_blueprint(members_bp, url_prefix='/members')
    app.register_blueprint(subscriptions_bp, url_prefix='/subscriptions')
    app.register_blueprint(payment_bp, url_prefix='/payments')
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    


    return app
