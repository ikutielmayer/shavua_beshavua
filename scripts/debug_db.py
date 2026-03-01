from app import create_app, db
from sqlalchemy import inspect

app = create_app()
with app.app_context():
    inspector = inspect(db.engine)
    columns = [c['name'] for c in inspector.get_columns('donation')]
    print(f"Columns in 'donation' table: {columns}")
    
    user_columns = [c['name'] for c in inspector.get_columns('user')]
    print(f"Columns in 'user' table: {user_columns}")
