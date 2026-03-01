from app import create_app, db
from app.models import Parasha, Question

def add_questions(parasha_name_es, qs):
    p = Parasha.query.filter_by(name_es=parasha_name_es).first()
    if not p: return
    Question.query.filter_by(parasha_id=p.id).delete()
    for d in qs:
        q = Question(
            parasha_id=p.id, text_es=d['text_es'], text_en=d['text_en'], text_he=d['text_he'],
            option_a_es=d['a_es'], option_a_en=d['a_en'], option_a_he=d['a_he'],
            option_b_es=d['b_es'], option_b_en=d['b_en'], option_b_he=d['b_he'],
            option_c_es=d['c_es'], option_c_en=d['c_en'], option_c_he=d['c_he'],
            correct_option=d['correct']
        )
        db.session.add(q)
    print(f"Added {len(qs)} to {parasha_name_es}")

app = create_app()
with app.app_context():
    # TETZAVE (Fixed)
    add_questions('Tetzavé', [
        {'text_es': '¿Aceite para la Menorá?', 'text_en': 'Oil for Menorah?', 'text_he': 'שמן למנורה?', 'a_es': 'Oliva puro', 'a_en': 'Pure olive', 'a_he': 'זית זך', 'b_es': 'Nuez', 'b_en': 'Nut', 'b_he': 'אגוז', 'c_es': 'Sésamo', 'c_en': 'Sesame', 'c_he': 'שומשום', 'correct': 'a'},
        {'text_es': '¿Quiénes eran Kohanim?', 'text_en': 'Who were Kohanim?', 'text_he': 'מי הכהנים?', 'a_es': 'Aharón e hijos', 'a_en': 'Aaron & sons', 'a_he': 'אהרן ובניו', 'b_es': 'Moisés e hijos', 'b_en': 'Moses & sons', 'b_he': 'משה ובניו', 'c_es': 'Levi e hijos', 'c_en': 'Levi & sons', 'c_he': 'לוי ובניו', 'correct': 'a'},
        {'text_es': '¿Piedras en el Joshen?', 'text_en': 'Stones in Choshen?', 'text_he': 'אבנים בחושן?', 'a_es': '12', 'a_en': '12', 'a_he': '12', 'b_es': '10', 'b_en': '10', 'b_he': '10', 'c_es': '7', 'c_en': '7', 'c_he': '7', 'correct': 'a'},
        {'text_es': '¿Color del Meíl?', 'text_en': 'Meil color?', 'text_he': 'צבע המעיל?', 'a_es': 'Tejelet (azul)', 'a_en': 'Techelet (blue)', 'a_he': 'תכלת', 'b_es': 'Blanco', 'b_en': 'White', 'b_he': 'לבן', 'c_es': 'Rojo', 'c_en': 'Red', 'c_he': 'אדום', 'correct': 'a'},
        {'text_es': '¿En el borde del Meíl?', 'text_en': 'On Meil rim?', 'text_he': 'בשולי המעיל?', 'a_es': 'Campanas y granadas', 'a_en': 'Bells & poms', 'a_he': 'פעמונים ורימונים', 'b_es': 'Flecos', 'b_en': 'Fringes', 'b_he': 'ציצית', 'c_es': 'Cintas', 'c_en': 'Ribbons', 'c_he': 'סרטים', 'correct': 'a'},
        {'text_es': '¿Texto en el Tzitz?', 'text_en': 'Tzitz text?', 'text_he': 'מה בציץ?', 'a_es': 'Kodesh L\'Hashem', 'a_en': 'Holy to God', 'a_he': 'קדש לה\'', 'b_es': 'Shma Israel', 'b_en': 'Shma Israel', 'b_he': 'שמע ישראל', 'c_es': 'Elohim', 'c_en': 'Elohim', 'c_he': 'אלוהים', 'correct': 'a'},
        {'text_es': '¿Altar de Oro para qué?', 'text_en': 'Golden altar for?', 'text_he': 'מזבח הזהב למה?', 'a_es': 'Incienso', 'a_en': 'Incense', 'a_he': 'קטורת', 'b_es': 'Sangre', 'b_en': 'Blood', 'b_he': 'דם', 'c_es': 'Agua', 'c_en': 'Water', 'c_he': 'מים', 'correct': 'a'},
        {'text_es': '¿Dentro del Joshen?', 'text_en': 'Inside Choshen?', 'text_he': 'בתוך החושן?', 'a_es': 'Urim y Tumim', 'a_en': 'Urim & Thummim', 'a_he': 'אורים ותומים', 'b_es': 'Maná', 'b_en': 'Manna', 'b_he': 'מן', 'c_es': 'Varas', 'c_en': 'Staffs', 'c_he': 'מטות', 'correct': 'a'},
        {'text_es': '¿Encendido de Menorá?', 'text_en': 'Lighting Menorah?', 'text_he': 'הדלקת המנורה?', 'a_es': 'Diario', 'a_en': 'Daily', 'a_he': 'תמיד', 'b_es': 'Semanal', 'b_en': 'Weekly', 'b_he': 'שבועי', 'c_es': 'Mensual', 'c_en': 'Monthly', 'c_he': 'חודשי', 'correct': 'a'},
        {'text_es': '¿Días de consagración?', 'text_en': 'Days of consecration?', 'text_he': 'ימי מילואים?', 'a_es': '7', 'a_en': '7', 'a_he': '7', 'b_es': '40', 'b_en': '40', 'b_he': '40', 'c_es': '12', 'c_en': '12', 'c_he': '12', 'correct': 'a'}
    ])

    # KI TISA
    add_questions('Ki Tisá', [
        {'text_es': '¿Censo con qué?', 'text_en': 'Census with?', 'text_he': 'מפקד עם?', 'a_es': 'Medio Shekel', 'a_en': 'Half Shekel', 'a_he': 'מחצית השקל', 'b_es': 'Un cordero', 'b_en': 'A lamb', 'b_he': 'כבש', 'c_es': 'Vino', 'c_en': 'Wine', 'c_he': 'יין', 'correct': 'a'},
        {'text_es': '¿Material del Kior?', 'text_en': 'Kior material?', 'text_he': 'חומר הכיור?', 'a_es': 'Bronce', 'a_en': 'Bronze', 'a_he': 'נחושת', 'b_es': 'Plata', 'b_en': 'Silver', 'b_he': 'כסף', 'c_es': 'Oro', 'c_en': 'Gold', 'c_he': 'זהב', 'correct': 'a'},
        {'text_es': '¿Artesano Bezalel?', 'text_en': 'Artisan Bezalel?', 'text_he': 'בצלאל האומן?', 'a_es': 'Judá', 'a_en': 'Judah', 'a_he': 'יהודה', 'b_es': 'Dan', 'b_en': 'Dan', 'b_he': 'דן', 'c_es': 'Levi', 'c_en': 'Levi', 'c_he': 'לוי', 'correct': 'a'},
        {'text_es': '¿Pecado del becerro?', 'text_en': 'Sin of the calf?', 'text_he': 'חטא העגל?', 'a_es': 'Idolatría', 'a_en': 'Idolatry', 'a_he': 'עבודה זרה', 'b_es': 'Robo', 'b_en': 'Theft', 'b_he': 'גזל', 'c_es': 'Mentira', 'c_en': 'Lying', 'c_he': 'שקר', 'correct': 'a'},
        {'text_es': '¿Tablas rotas por?', 'text_en': 'Tablets broken by?', 'text_he': 'משה שיבר הלוחות?', 'a_es': 'Moisés', 'a_en': 'Moses', 'a_he': 'משה', 'b_es': 'Aharón', 'b_en': 'Aaron', 'b_he': 'אהרן', 'c_es': 'Fuego', 'c_en': 'Fire', 'c_he': 'אש', 'correct': 'a'},
        {'text_es': '¿Moisés en el monte?', 'text_en': 'Moses on mount?', 'text_he': 'משה בהר?', 'a_es': '40 días', 'a_en': '40 days', 'a_he': '40 יום', 'b_es': '7 días', 'b_en': '7 days', 'b_he': '7 ימים', 'c_es': 'Una noche', 'c_en': 'One night', 'c_he': 'לילה', 'correct': 'a'},
        {'text_es': '¿Rostro de Moisés?', 'text_en': 'Moses face?', 'text_he': 'פני משה?', 'a_es': 'Brillaba', 'a_en': 'Shone', 'a_he': 'קרן אור', 'b_es': 'Triste', 'b_en': 'Sad', 'b_he': 'עצוב', 'c_es': 'Rojo', 'c_en': 'Red', 'c_he': 'אדום', 'correct': 'a'},
        {'text_es': '¿Mitzvá antes de obra?', 'text_en': 'Mitzvah before work?', 'text_he': 'מצווה לפני המלאכה?', 'a_es': 'Shabat', 'a_en': 'Shabbat', 'a_he': 'שבת', 'b_es': 'Pascua', 'b_en': 'Passover', 'b_he': 'פסח', 'c_es': 'Diezmo', 'c_en': 'Tithes', 'c_he': 'מעשר', 'correct': 'a'},
        {'text_es': '¿Aceite de unción para?', 'text_en': 'Anointing oil for?', 'text_he': 'שמן המשחה למה?', 'a_es': 'Consagrar', 'a_en': 'Consecrate', 'a_he': 'קידוש', 'b_es': 'Comer', 'b_en': 'Eat', 'b_he': 'אכילה', 'c_es': 'Lavar', 'c_en': 'Wash', 'c_he': 'רחיצה', 'correct': 'a'},
        {'text_es': '¿Quién ayudó a Bezalel?', 'text_en': 'Helped Bezalel?', 'text_he': 'עוזר בצלאל?', 'a_es': 'Oholiav', 'a_en': 'Oholiav', 'a_he': 'אהליאב', 'b_es': 'Joshua', 'b_en': 'Joshua', 'b_he': 'יהושע', 'c_es': 'Levi', 'c_en': 'Levi', 'c_he': 'לוי', 'correct': 'a'}
    ])

    # VAYAKHEL
    add_questions('Vayakhel', [
        {'text_es': '¿Día de descanso?', 'text_en': 'Day of rest?', 'text_he': 'יום חופש?', 'a_es': 'Shabat', 'a_en': 'Shabbat', 'a_he': 'שבת', 'b_es': 'Domingo', 'b_en': 'Sunday', 'b_he': 'ראשון', 'c_es': 'Viernes', 'c_en': 'Friday', 'c_he': 'שישי', 'correct': 'a'},
        {'text_es': '¿Ofrendas de quién?', 'text_en': 'Offerings from?', 'text_he': 'ממי הנדבה?', 'a_es': 'Corazón generoso', 'a_en': 'Generous heart', 'a_he': 'נדבת לב', 'b_es': 'Obligatorias', 'b_en': 'Mandatory', 'b_he': 'חובה', 'c_es': 'Extranjeros', 'c_en': 'Foreigners', 'c_he': 'זרים', 'correct': 'a'},
        {'text_es': '¿Las mujeres hilaron?', 'text_en': 'Women spun?', 'text_he': 'הנשים טוו?', 'a_es': 'Pelo de cabra', 'a_en': 'Goat hair', 'a_he': 'שיער עיזים', 'b_es': 'Lana de oveja', 'b_en': 'Sheep wool', 'b_he': 'צמר', 'c_es': 'Lino', 'c_en': 'Linen', 'c_he': 'פשתן', 'correct': 'a'},
        {'text_es': '¿Ofrendas sobraron?', 'text_en': 'Excess offerings?', 'text_he': 'יותר מדי נדבה?', 'a_es': 'Sí', 'a_en': 'Yes', 'a_he': 'כן', 'b_es': 'No', 'b_en': 'No', 'b_he': 'לא', 'c_es': 'Faltaron', 'c_en': 'Missing', 'c_he': 'היה חסר', 'correct': 'a'},
        {'text_es': '¿Moisés detuvo?', 'text_en': 'Moses stopped?', 'text_he': 'משה הפסיק?', 'a_es': 'Las ofrendas', 'a_en': 'The offerings', 'a_he': 'את הנדבה', 'b_es': 'La lluvia', 'b_en': 'The rain', 'b_he': 'את הגשם', 'c_es': 'El sol', 'c_en': 'The sun', 'c_he': 'את השמש', 'correct': 'a'},
        {'text_es': '¿Material de cortinas?', 'text_en': 'Curtains material?', 'text_he': 'חומר היריעות?', 'a_es': 'Lino y lana', 'a_en': 'Linen & wool', 'a_he': 'פשתן וצמר', 'b_es': 'Seda', 'b_en': 'Silk', 'b_he': 'משי', 'c_es': 'Plástico', 'c_en': 'Plastic', 'c_he': 'פלסטיק', 'correct': 'a'},
        {'text_es': '¿Columnas hechas de?', 'text_en': 'Pillars made of?', 'text_he': 'חומר העמודים?', 'a_es': 'Madera acacia', 'a_en': 'Acacia wood', 'a_he': 'עצי שיטים', 'b_es': 'Roble', 'b_en': 'Oak', 'b_he': 'אלון', 'c_es': 'Cedro', 'c_en': 'Cedar', 'c_he': 'ארז', 'correct': 'a'},
        {'text_es': '¿Basas hechas de?', 'text_en': 'Bases made of?', 'text_he': 'חומר האדנים?', 'a_es': 'Plata', 'a_en': 'Silver', 'a_he': 'כסף', 'b_es': 'Hierro', 'b_en': 'Iron', 'b_he': 'ברזל', 'c_es': 'Barro', 'c_en': 'Clay', 'c_he': 'חמר', 'correct': 'a'},
        {'text_es': '¿Anillos para?', 'text_en': 'Rings for?', 'text_he': 'טבעות למה?', 'a_es': 'Transportar barras', 'a_en': 'Carry bars', 'a_he': 'נשיאת הבריחים', 'b_es': 'Decoración', 'b_en': 'Decoration', 'b_he': 'קישוט', 'c_es': 'Uso personal', 'c_en': 'Personal use', 'c_he': 'שימוש אישי', 'correct': 'a'},
        {'text_es': '¿El Arca cubierta con?', 'text_en': 'Ark covered with?', 'text_he': 'הארון מצופה ב?', 'a_es': 'Oro puro', 'a_en': 'Pure gold', 'a_he': 'זהב טהור', 'b_es': 'Broce', 'b_en': 'Bronze', 'b_he': 'נחושת', 'c_es': 'Pintura', 'c_en': 'Paint', 'c_he': 'צבע', 'correct': 'a'}
    ])

    # PEKUDE (Accounting)
    add_questions('Pekudé', [
        {'text_es': '¿Qué significa Pekudé?', 'text_en': 'Pekudei meaning?', 'text_he': 'משמעות פקודי?', 'a_es': 'Contabilidades', 'a_en': 'Accountings', 'a_he': 'חשבונות', 'b_es': 'Viajes', 'b_en': 'Travels', 'b_he': 'מסעות', 'c_es': 'Sacrificios', 'c_en': 'Sacrifices', 'c_he': 'קורבנות', 'correct': 'a'},
        {'text_es': '¿Quién dirigió el recuento?', 'text_en': 'Who led accounting?', 'text_he': 'מי ניהל החשבון?', 'a_es': 'Itamar', 'a_en': 'Itamar', 'a_he': 'איתמר', 'b_es': 'Eleazar', 'b_en': 'Eleazar', 'b_he': 'אלעזר', 'c_es': 'Phinehas', 'c_en': 'Phinehas', 'c_he': 'פנחס', 'correct': 'a'},
        {'text_es': '¿Cuánta plata del censo?', 'text_en': 'Silver from census?', 'text_he': 'כמה כסף מהמפקד?', 'a_es': '100 talentos', 'a_en': '100 talents', 'a_he': '100 כיכר', 'b_es': '1 talento', 'b_en': '1 talent', 'b_he': '1 כיכר', 'c_es': '50 talentos', 'c_en': '50 talents', 'c_he': '50 כיכר', 'correct': 'a'},
        {'text_es': '¿Inauguración del Mishkán?', 'text_en': 'Inauguration day?', 'text_he': 'יום חנוכת המשכן?', 'a_es': '1 de Nisán', 'a_en': '1st of Nissan', 'a_he': 'א\' ניסן', 'b_es': '1 de Shvat', 'b_en': '1st of Shvat', 'b_he': 'א\' שבט', 'c_es': '1 de Elul', 'c_en': '1st of Elul', 'c_he': 'א\' אלול', 'correct': 'a'},
        {'text_es': '¿Moisés bendijo?', 'text_en': 'Moses blessed?', 'text_he': 'משה בירך?', 'a_es': 'Sí', 'a_en': 'Yes', 'a_he': 'כן', 'b_es': 'No', 'b_en': 'No', 'b_he': 'לא', 'c_es': 'Solo a los jefes', 'c_en': 'Princes only', 'c_he': 'רק נשיאים', 'correct': 'a'},
        {'text_es': '¿La nube llenó?', 'text_en': 'Cloud filled?', 'text_he': 'הענן מילא?', 'a_es': 'El Tabernáculo', 'a_en': 'The Tabernacle', 'a_he': 'את המשכן', 'b_es': 'El campamento', 'b_en': 'The camp', 'b_he': 'את המחנה', 'c_es': 'El mar', 'c_en': 'The sea', 'c_he': 'את הים', 'correct': 'a'},
        {'text_es': '¿Cómo guiaba la nube?', 'text_en': 'How cloud guided?', 'text_he': 'איך הנחה הענן?', 'a_es': 'Si se elevaba, viajaban', 'a_en': 'If rose, traveled', 'a_he': 'כשנעלה - נסעו', 'b_es': 'Si brillaba más', 'b_en': 'If shone more', 'b_he': 'כשהאיר יותר', 'c_es': 'Por dirección de viento', 'c_en': 'Wind direction', 'c_he': 'כיוון הרוח', 'correct': 'a'},
        {'text_es': '¿Fuego sobre Mishkán?', 'text_en': 'Fire over Mishkan?', 'text_he': 'אש על המשכן?', 'a_es': 'De noche', 'a_en': 'At night', 'a_he': 'בלילה', 'b_es': 'De día', 'b_en': 'By day', 'b_he': 'ביום', 'c_es': 'Nunca', 'c_en': 'Never', 'c_he': 'אף פעם', 'correct': 'a'},
        {'text_es': '¿Qué libro termina?', 'text_en': 'Which book ends?', 'text_he': 'איזה ספר מסתיים?', 'a_es': 'Éxodo (Shemot)', 'a_en': 'Exodus', 'a_he': 'שמות', 'b_es': 'Génesis', 'b_en': 'Genesis', 'b_he': 'בראשית', 'c_es': 'Levítico', 'c_en': 'Leviticus', 'c_he': 'ויקרא', 'correct': 'a'},
        {'text_es': '¿Quién erigió el Mishkán?', 'text_en': 'Who erected Mishkan?', 'text_he': 'מי הקים המשכן?', 'a_es': 'Moisés', 'a_en': 'Moses', 'a_he': 'משה', 'b_es': 'Aharón', 'b_en': 'Aaron', 'b_he': 'אהרן', 'c_es': 'El pueblo unido', 'c_en': 'All the people', 'c_he': 'כל העם', 'correct': 'a'}
    ])

    # VAYIKRA
    add_questions('Vayikrá', [
        {'text_es': '¿Sacrificio que se eleva?', 'text_en': 'Ascending offering?', 'text_he': 'מהו קורבן עולה?', 'a_es': 'Olá', 'a_en': 'Olah', 'a_he': 'עולה', 'b_es': 'Jatat', 'b_en': 'Chatat', 'b_he': 'חטאת', 'c_es': 'Asham', 'c_en': 'Asham', 'c_he': 'אשם', 'correct': 'a'},
        {'text_es': '¿Ofrenda vegetal?', 'text_en': 'Plant offering?', 'text_he': 'קורבן צמחוני?', 'a_es': 'Minjá', 'a_en': 'Mincha', 'a_he': 'מנחה', 'b_es': 'Zevaj', 'b_en': 'Zevach', 'b_he': 'זבח', 'c_es': 'Neder', 'c_en': 'Neder', 'c_he': 'נדר', 'correct': 'a'},
        {'text_es': '¿Prohibido en Minjá?', 'text_en': 'Forbidden in Mincha?', 'text_he': 'אסור במנחה?', 'a_es': 'Levadura y miel', 'a_en': 'Leaven & honey', 'a_he': 'שאור ודבש', 'b_es': 'Agua', 'b_en': 'Water', 'b_he': 'מים', 'c_es': 'Aceituna', 'c_en': 'Olive', 'c_he': 'זית', 'correct': 'a'},
        {'text_es': '¿Obligatorio en ofrendas?', 'text_en': 'Mandatory in offerings?', 'text_he': 'חובה בכל קורבן?', 'a_es': 'Sal', 'a_en': 'Salt', 'a_he': 'מלח', 'b_es': 'Azúcar', 'b_en': 'Sugar', 'b_he': 'סוכר', 'c_es': 'Pimienta', 'c_en': 'Pepper', 'c_he': 'פלפל', 'correct': 'a'},
        {'text_es': '¿Sacrificio de paz?', 'text_en': 'Peace offering?', 'text_he': 'קורבן שלום?', 'a_es': 'Shelamim', 'a_en': 'Shelamim', 'a_he': 'שלמים', 'b_es': 'Olá', 'b_en': 'Olah', 'b_he': 'עולה', 'c_es': 'Jatat', 'c_en': 'Chatat', 'c_he': 'חטאת', 'correct': 'a'},
        {'text_es': '¿Ofrenda por pecado?', 'text_en': 'Sin offering?', 'text_he': 'קורבן על חטא?', 'a_es': 'Jatat', 'a_en': 'Chatat', 'a_he': 'חטאת', 'b_es': 'Zevaj', 'b_en': 'Zevach', 'b_he': 'זבח', 'c_es': 'Minjá', 'c_en': 'Mincha', 'c_he': 'מנחה', 'correct': 'a'},
        {'text_es': '¿Ofrenda por culpa?', 'text_en': 'Guilt offering?', 'text_he': 'קורבן אשם?', 'a_es': 'Asham', 'a_en': 'Asham', 'a_he': 'אשם', 'b_es': 'Olá', 'b_en': 'Olah', 'b_he': 'עולה', 'c_es': 'Todá', 'c_en': 'Todah', 'c_he': 'תודה', 'correct': 'a'},
        {'text_es': '¿Grasa prohibida?', 'text_en': 'Forbidden fat?', 'text_he': 'שומן אסור?', 'a_es': 'Jelev', 'a_en': 'Chelev', 'a_he': 'חלב', 'b_es': 'Shuman', 'b_en': 'Shuman', 'b_he': 'שומן', 'c_es': 'Basar', 'c_en': 'Basar', 'c_he': 'בשר', 'correct': 'a'},
        {'text_es': '¿Ofrenda de pobre?', 'text_en': 'Poors offering?', 'text_he': 'קורבן עני?', 'a_es': 'Aves', 'a_en': 'Birds', 'a_he': 'עופות', 'b_es': 'Buey', 'b_en': 'Ox', 'b_he': 'שור', 'c_es': 'Oro', 'c_en': 'Gold', 'c_he': 'זהב', 'correct': 'a'},
        {'text_es': '¿Sangre prohibida?', 'text_en': 'Blood forbidden?', 'text_he': 'דם אסור?', 'a_es': 'Sí', 'a_en': 'Yes', 'a_he': 'כן', 'b_es': 'No', 'b_en': 'No', 'b_he': 'לא', 'c_es': 'Solo de aves', 'c_en': 'Only birds', 'c_he': 'רק עוף', 'correct': 'a'}
    ])

    # TZAV
    add_questions('Tzav', [
        {'text_es': '¿A quién ordenó Moisés?', 'text_en': 'Who did Moses command?', 'text_he': 'אל מי ציווה משה?', 'a_es': 'Aharón e hijos', 'a_en': 'Aaron & sons', 'a_he': 'אהרן ובניו', 'b_es': 'A los jefes', 'b_en': 'To princes', 'b_he': 'לנשיאים', 'c_es': 'A las mujeres', 'c_en': 'To women', 'c_he': 'לנשים', 'correct': 'a'},
        {'text_es': '¿Fuego del altar?', 'text_en': 'Altar fire?', 'text_he': 'אש המזבח?', 'a_es': 'Continuo (Tamid)', 'a_en': 'Continuous', 'a_he': 'תמיד', 'b_es': 'Solo de día', 'b_en': 'Only day', 'b_he': 'רק ביום', 'c_es': 'Solar', 'c_en': 'Solar', 'c_he': 'שמש', 'correct': 'a'},
        {'text_es': '¿Quién comía la Minjá?', 'text_en': 'Who ate Mincha?', 'text_he': 'מי אכל המנחה?', 'a_es': 'Kohanim', 'a_en': 'Kohanim', 'a_he': 'כהנים', 'b_es': 'Donantes', 'b_en': 'Donors', 'b_he': 'תורמים', 'c_es': 'Animales', 'c_en': 'Animals', 'c_he': 'חיות', 'correct': 'a'},
        {'text_es': '¿Tipo de pan en Todá?', 'text_en': 'Todah bread?', 'text_he': 'חם בנדבת תודה?', 'a_es': 'Lindo y Jametz', 'a_en': 'Linen & Chamez', 'a_he': 'פשתן וחמץ', 'b_es': 'Solo Mazá', 'b_en': 'Matzah only', 'b_he': 'רק מצה', 'c_es': 'Solo Trigo', 'c_en': 'Wheat only', 'c_he': 'רק חיטה', 'correct': 'a'},
        {'text_es': '¿Dónde comer Jatat?', 'text_en': 'Where eat Chatat?', 'text_he': 'איפה אוכלים חטאת?', 'a_es': 'Lugar santo (Mishkán)', 'a_en': 'Holy place', 'a_he': 'מקום קדוש', 'b_es': 'En casa', 'b_en': 'At home', 'b_he': 'בבית', 'c_es': 'En el campo', 'c_en': 'In field', 'c_he': 'בשדה', 'correct': 'a'},
        {'text_es': '¿Ropa sacerdotal?', 'text_en': 'Priestly clothes?', 'text_he': 'בגדי כהונה?', 'a_es': 'Lino', 'a_en': 'Linen', 'a_he': 'פשתן', 'b_es': 'Cuero', 'b_en': 'Leather', 'b_he': 'עור', 'c_es': 'Papel', 'c_en': 'Paper', 'c_he': 'נייר', 'correct': 'a'},
        {'text_es': '¿Quién lavó a Kohanim?', 'text_en': 'Who washed Kohanim?', 'text_he': 'מי רחץ הכהנים?', 'a_es': 'Moisés', 'a_en': 'Moses', 'a_he': 'משה', 'b_es': 'Nadie', 'b_en': 'No one', 'b_he': 'אף אחד', 'c_es': 'Ellos mismos', 'c_en': 'Themselves', 'c_he': 'הם בעצמם', 'correct': 'a'},
        {'text_es': '¿Ungieron el Mishkán?', 'text_en': 'Anointed Mishkan?', 'text_he': 'משחו את המשכן?', 'a_es': 'Sí', 'a_en': 'Yes', 'a_he': 'כן', 'b_es': 'No', 'b_en': 'No', 'b_he': 'לא', 'c_es': 'Solo el Arca', 'c_en': 'Ark only', 'c_he': 'רק הארון', 'correct': 'a'},
        {'text_es': '¿Cuántos días de espera?', 'text_en': 'Days of waiting?', 'text_he': 'ימי המתנה?', 'a_es': '7', 'a_en': '7', 'a_he': '7', 'b_es': '3', 'b_en': '3', 'b_he': '3', 'c_es': '1', 'c_en': '1', 'c_he': '1', 'correct': 'a'},
        {'text_es': '¿Ofrenda de consagración?', 'text_en': 'Consecration offering?', 'text_he': 'קורבן מילואים?', 'a_es': 'Carnero', 'a_en': 'Ram', 'a_he': 'איל', 'b_es': 'Vaca', 'b_en': 'Cow', 'b_he': 'פרה', 'c_es': 'Perro', 'c_en': 'Dog', 'c_he': 'כלב', 'correct': 'a'}
    ])

    db.session.commit()
    print("Batch 1 completed.")
