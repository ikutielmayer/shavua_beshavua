from app import create_app, db
import os

app = create_app()
with app.app_context():
    print("Creating all tables (including UserAnswer)...")
    db.create_all()
    print("Done! If the table already existed, nothing changed. If it was missing, it's now created.")
