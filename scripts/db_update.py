from app import create_app, db
from app.models import User, Parasha, Question, Participation, Donation

app = create_app()

with app.app_context():
    print("Dropping all tables...")
    db.drop_all()
    print("Creating all tables...")
    db.create_all()
    print("Tables re-created successfully.")

print("Running create_admin.py to restore initial data...")
# I will run this via command line after this file is written
