from app import create_app, db
from sqlalchemy import text

app = create_app()
with app.app_context():
    print("Checking for new columns in 'user' table...")
    try:
        # Check if column exists
        with db.engine.connect() as conn:
            # We use text() for raw SQL in SQLAlchemy 2.0+
            result = conn.execute(text("SHOW COLUMNS FROM user LIKE 'is_verified'"))
            if not result.fetchone():
                print("Adding 'is_verified' column...")
                conn.execute(text("ALTER TABLE user ADD COLUMN is_verified BOOLEAN DEFAULT FALSE"))
            
            result = conn.execute(text("SHOW COLUMNS FROM user LIKE 'verification_code'"))
            if not result.fetchone():
                print("Adding 'verification_code' column...")
                conn.execute(text("ALTER TABLE user ADD COLUMN verification_code VARCHAR(6)"))
            
            conn.commit()
            print("Database updated successfully.")
    except Exception as e:
        print(f"Error updating database: {e}")
