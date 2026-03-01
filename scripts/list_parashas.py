from app import create_app, db
from app.models import Parasha
from datetime import datetime

app = create_app()
with app.app_context():
    parashas = Parasha.query.all()
    print(f"Total Parashot found: {len(parashas)}")
    for p in parashas:
        print(f"ID={p.id}, name={p.name_es}, start={p.week_start}, end={p.week_end}")
    
    now = datetime.now()
    print(f"Current server time: {now}")
    print(f"Current date: {now.date()}")
