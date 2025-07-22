from backend import create_app
from backend.models import db


app = create_app('TestingConfig')  # Use TestingConfig for testing


with app.app_context():
    #db.drop_all()  # Drop all tables if they exist
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)  