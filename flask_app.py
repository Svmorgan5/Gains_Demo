from backend import create_app
from backend.models import db


app = create_app('ProductionConfig')  # Change to 'DevelopmentConfig' or 'TestingConfig' as needed


with app.app_context():
    #db.drop_all()  # Drop all tables if they exist
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)  