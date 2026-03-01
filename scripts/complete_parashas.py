from app import create_app, db
from app.models import Parasha, Question
from datetime import date, timedelta

app = create_app()
with app.app_context():
    # List of Parashot for the rest of the Jewish year (standard calendar)
    # Starting after Pekudei (March 28, 2026)
    
    parashot_data = [
        # Sefer Vayikra
        ('Vayikrá', 'Vayikra', 'ויקרא', date(2026, 4, 11)), # April 4 is sometimes Pesach/special or adjustment
        ('Tzav', 'Tzav', 'צו', date(2026, 4, 18)),
        ('Sheminí', 'Shemini', 'שמיני', date(2026, 4, 25)),
        ('Tazría-Metzorá', 'Tazria-Metzora', 'תזריע-מצורע', date(2026, 5, 2)),
        ('Ajarei Mot-Kedoshim', 'Acharei Mot-Kedoshim', 'אחרי מות-קדושים', date(2026, 5, 9)),
        ('Emor', 'Emor', 'אמור', date(2026, 5, 16)),
        ('Behar-Bejukotai', 'Behar-Bechukotai', 'בהר-בחוקתי', date(2026, 5, 23)),
        # Sefer Bamidbar
        ('Bemidbar', 'Bamidbar', 'במדבר', date(2026, 5, 30)),
        ('Nasó', 'Naso', 'נשא', date(2026, 6, 6)),
        ('Behaalotjá', 'Behaalotcha', 'בהעלותך', date(2026, 6, 13)),
        ('Shelaj Lejá', 'Shelach Lecha', 'שלח לך', date(2026, 6, 20)),
        ('Kóraj', 'Korach', 'קרח', date(2026, 6, 27)),
        ('Jukat-Balak', 'Chukat-Balak', 'חקת-בלק', date(2026, 7, 4)),
        ('Pinjás', 'Pinchas', 'פינחס', date(2026, 7, 11)),
        ('Matot-Maséi', 'Matot-Masei', 'מטות-מסעי', date(2026, 7, 18)),
        # Sefer Devarim
        ('Devarim', 'Devarim', 'דברים', date(2026, 7, 25)),
        ('Vaetjanán', 'Vaetchanan', 'ואתחנן', date(2026, 8, 1)),
        ('Ékev', 'Ekev', 'עקב', date(2026, 8, 8)),
        ('Reé', 'Re\'eh', 'ראה', date(2026, 8, 15)),
        ('Shoftim', 'Shoftim', 'שופטים', date(2026, 8, 22)),
        ('Ki Tetzé', 'Ki Tetze', 'כי תצא', date(2026, 8, 29)),
        ('Ki Tavó', 'Ki Tavo', 'כי תבא', date(2026, 9, 5)),
        ('Nitzavim-Vayélej', 'Nitzavim-Vayelech', 'נצבים-וילך', date(2026, 9, 12)),
        # Ha'azinu is close to Rosh Hashana/Yom Kippur
        ('Haazinu', 'Haazinu', 'האזינו', date(2026, 9, 19)),
    ]

    for es, en, he, sat_date in parashot_data:
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
            
            # Placeholder question
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
    print("Database fully populated with Parashot until the end of the year cycle.")
