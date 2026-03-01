from app import create_app, db
from sqlalchemy import text

app = create_app()
with app.app_context():
    print("Migrating donation table...")
    try:
        with db.engine.connect() as conn:
            # Check for duration_type
            result = conn.execute(text("SHOW COLUMNS FROM donation LIKE 'duration_type'"))
            if not result.fetchone():
                print("Adding duration_type...")
                conn.execute(text("ALTER TABLE donation ADD COLUMN duration_type VARCHAR(20) DEFAULT 'single'"))
            
            # Check for weeks_count
            result = conn.execute(text("SHOW COLUMNS FROM donation LIKE 'weeks_count'"))
            if not result.fetchone():
                print("Adding weeks_count...")
                conn.execute(text("ALTER TABLE donation ADD COLUMN weeks_count INT DEFAULT 1"))
            
            conn.commit()
            print("Donation migration completed.")
    except Exception as e:
        print(f"Error: {e}")
