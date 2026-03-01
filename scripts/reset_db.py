import sys
import os
sys.path.append(os.getcwd())
from app import create_app, db
from app.models import Parasha, Question, User
from datetime import datetime, timedelta

def reset_and_populate():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Database schemas recreated.")

        # Add Parashas
        base_date = datetime(2026, 2, 28).date() # Today is Feb 28
        parashas_data = [
            ('Tetzavé', 'Tetzave', 'תצוה', base_date - timedelta(days=7), base_date),
            ('Ki Tisá', 'Ki Tisa', 'כי תשא', base_date + timedelta(days=1), base_date + timedelta(days=7)),
            ('Vayakhel', 'Vayakhel', 'ויקהל', base_date + timedelta(days=8), base_date + timedelta(days=14)),
            ('Pekudé', 'Pekude', 'פקודי', base_date + timedelta(days=15), base_date + timedelta(days=21)),
            ('Vayikrá', 'Vayikra', 'ויקרא', base_date + timedelta(days=22), base_date + timedelta(days=28)),
        ]

        for p_es, p_en, p_he, start, end in parashas_data:
            p = Parasha(name_es=p_es, name_en=p_en, name_he=p_he, week_start=start, week_end=end)
            db.session.add(p)
        
        db.session.commit()
        print("Parashas added.")

        # Create Admin
        admin = User(username='admin', email='admin@example.com', role='admin')
        admin.password = 'pbkdf2:sha256:600000$yN6RzXh8$8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e' # Needs real hash for login, but this is a stub
        from werkzeug.security import generate_password_hash
        admin.password = generate_password_hash('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Admin user created (admin / admin123)")

if __name__ == '__main__':
    reset_and_populate()
