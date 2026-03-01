from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Create 'ikutiel' admin if not exists
    admin_ikutiel = User.query.filter_by(username='ikutiel').first()
    if not admin_ikutiel:
        admin_ikutiel = User(
            username='ikutiel',
            first_name='Yekutiel',
            last_name='Admin',
            email='ikutiel@shavuabeshavua.com',
            phone='+123456789',
            has_whatsapp=True,
            password=generate_password_hash('B7654321b', method='scrypt'),
            role='admin'
        )
        db.session.add(admin_ikutiel)
        db.session.commit()
        print("Admin user 'ikutiel' created.")
    
    from app.models import Parasha
    from datetime import datetime, timedelta
    now = datetime.now().date()
    parasha = Parasha.query.first()
    if not parasha:
        p = Parasha(
            name_es='Terumá',
            name_en='Terumah',
            name_he='תרומה',
            week_start=now - timedelta(days=now.weekday()), # Monday
            week_end=now - timedelta(days=now.weekday()) + timedelta(days=6) # Sunday
        )
        db.session.add(p)
        db.session.commit()
        print("Sample Parasha added.")
