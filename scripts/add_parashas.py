from app import create_app, db
from app.models import Parasha, Question
from datetime import date, timedelta

app = create_app()
with app.app_context():
    # Update Terumah end date to be precisely Feb 28th (Saturday)
    terumah = Parasha.query.get(1)
    if terumah:
        terumah.week_end = date(2026, 2, 28)
        db.session.commit()
        print("Terumah updated.")

    data = [
        ('Tetzavé', 'Tetzaveh', 'תצוה', date(2026, 3, 7)),
        ('Ki Tisá', 'Ki Tisa', 'כי תשא', date(2026, 3, 14)),
        ('Vayakhel', 'Vayakhel', 'ויקהל', date(2026, 3, 21)),
        ('Pekudé', 'Pekudei', 'פקודי', date(2026, 3, 28)),
    ]

    for es, en, he, sat_date in data:
        existing = Parasha.query.filter_by(name_es=es).first()
        if not existing:
            p = Parasha(
                name_es=es,
                name_en=en,
                name_he=he,
                week_start=sat_date - timedelta(days=6),
                week_end=sat_date
            )
            db.session.add(p)
            db.session.flush()
            
            # Add a placeholder question for it
            q = Question(
                parasha_id=p.id,
                text_es=f"Pregunta inicial de {es}",
                text_en=f"Initial question for {en}",
                text_he=f"שאלה ראשונה של {he}",
                option_a_es="Opción A",
                option_b_es="Opción B",
                option_c_es="Opción C",
                correct_option='a'
            )
            db.session.add(q)
            print(f"Added Parasha: {es}")

    db.session.commit()
    print("Database updated with more Parashot.")
