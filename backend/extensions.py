from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask_caching import Cache

ma = Marshmallow()
limiter = Limiter(
    key_func=lambda: "global",
    default_limits=["800 per day", "300 per hour"],
    storage_uri="memory://",
)
cache = Cache()