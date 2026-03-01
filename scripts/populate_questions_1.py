from app import create_app, db
from app.models import Parasha, Question

def add_questions(parasha_name_es, questions_list):
    parasha = Parasha.query.filter_by(name_es=parasha_name_es).first()
    if not parasha:
        print(f"Parasha {parasha_name_es} not found.")
        return

    # Remove existing questions for this parasha
    Question.query.filter_by(parasha_id=parasha.id).delete()
    
    for q_data in questions_list:
        q = Question(
            parasha_id=parasha.id,
            text_es=q_data['text_es'],
            text_en=q_data['text_en'],
            text_he=q_data['text_he'],
            option_a_es=q_data['a_es'],
            option_a_en=q_data['a_en'],
            option_a_he=q_data['a_he'],
            option_b_es=q_data['b_es'],
            option_b_en=q_data['b_en'],
            option_b_he=q_data['b_he'],
            option_c_es=q_data['c_es'],
            option_c_en=q_data['c_en'],
            option_c_he=q_data['c_he'],
            correct_option=q_data['correct']
        )
        db.session.add(q)
    print(f"Added {len(questions_list)} questions to {parasha_name_es}")

app = create_app()
with app.app_context():
    # TETZAVÉ
    tetzave_q = [
        {'text_es': '¿Tipo de aceite para la Menorá?', 'text_en': 'Type of oil for Menorah?', 'text_he': 'סוג שמן למנורה?', 'a_es': 'Puro de oliva', 'a_en': 'Pure olive', 'a_he': 'זית זך', 'b_es': 'De nuez', 'b_en': 'Nut', 'b_he': 'אגוז', 'c_es': 'Maíz', 'c_en': 'Corn', 'c_he': 'תירס', 'correct': 'a'},
        {'text_es': '¿Quiénes eran los Kohanim?', 'text_en': 'Who were the Kohanim?', 'text_he': 'מי היו הכהנים?', 'a_es': 'Moisés y sus hijos', 'a_en': 'Moses and sons', 'a_he': 'משה ובניו', 'b_es': 'Aharón y sus hijos', 'b_en': 'Aaron and sons', 'b_he': 'אהרן ובניו', 'c_es': 'Levi y sus hijos', 'c_en': 'Levi and sons', 'c_he': 'לוי ובניו', 'correct': 'b'},
        {'text_es': '¿Cuántas piedras en el Joshen?', 'text_en': 'How many stones in Choshen?', 'text_he': 'כמה אבנים בחושן?', 'a_es': '12', 'a_en': '12', 'a_he': '12', 'b_es': '10', 'b_en': '10', 'b_he': '10', 'c_es': '7', 'c_en': '7', 'c_he': '7', 'correct': 'a'},
        {'text_es': '¿Qué color era el Meíl?', 'text_en': 'What color was the Meil?', 'text_he': 'מה צבע המעיל?', 'a_es': 'Blanco', 'a_en': 'White', 'a_he': 'לבן', 'b_es': 'Carmesí', 'b_en': 'Crimson', 'b_he': 'תולעת שני', 'c_es': 'Azul (Tejelet)', 'c_en': 'Blue (Techelet)', 'c_he': 'תכלת', 'correct': 'c'},
        {'text_es': '¿Qué había en el borde del Meíl?', 'text_en': 'What was on the rim of the Meil?', 'text_he': 'מה היה בשולי המעיל?', 'a_es': 'Campanas y granadas', 'a_en': 'Bells and pomegranates', 'a_he': 'פעמונים ורימונים', 'b_es': 'Flecos', 'b_en': 'Fringes', 'b_he': 'ציצית', 'c_es': 'Botones', 'c_en': 'Buttons', 'c_he': 'כפתורים', 'correct': 'a'},
        {'text_es': '¿Texto grabado en el Tzitz?', 'text_en': 'Text on the Tzitz?', 'text_he': 'מה כתוב על הציץ?', 'a_es': 'Kodesh L\'Hashem', 'a_en': 'Holy to God', 'a_he': 'קדש לה\'', 'b_es': 'Shma Israel', 'b_en': 'Shma Israel', 'a_he': 'שמע ישראל', 'c_es': 'Torat Emet', 'c_en': 'Torah Emet', 'c_he': 'תורת אמת', 'correct': 'a'},
        {'text_es': '¿Para qué servía el Altar de Oro?', 'text_en': 'Golden Altar purpose?', 'text_he': 'מזבח הזהב למה?', 'a_es': 'Incienso (Ketoret)', 'a_en': 'Incense', 'a_he': 'קטורת', 'b_es': 'Animales', 'b_en': 'Animals', 'b_he': 'זבחים', 'c_es': 'Vino', 'c_en': 'Wine', 'c_he': 'יין', 'correct': 'a'},
        {'text_es': '¿Qué se ponía en el Joshen?', 'text_en': 'What inside Choshen?', 'text_he': 'מה בתוך החושן?', 'a_es': 'Urim y Tumim', 'a_en': 'Urim and Thummim', 'a_he': 'אורים ותומים', 'b_es': 'Maná', 'b_en': 'Manna', 'b_he': 'מן', 'c_es': 'Las Tablas', 'c_en': 'The Tablets', 'c_he': 'לוחות הברית', 'correct': 'a'},
        {'text_es': '¿Quién supervisó la Menorá?', 'text_en': 'Who supervised the Menorah?', 'text_he': 'מי השגיח על המנורה?', 'a_es': 'Aharón', 'a_en': 'Aaron', 'a_he': 'אהרן', 'b_es': 'Moisés', 'b_en': 'Moses', 'b_he': 'משה', 'c_es': 'Eleazar', 'c_en': 'Eleazar', 'c_he': 'אלעזר', 'correct': 'a'},
        {'text_es': '¿Días de consagración de Kohanim?', 'text_en': 'Days of Kohanim consecration?', 'text_he': 'ימי המילואים?', 'a_es': '7', 'a_en': '7', 'a_he': '7', 'b_es': '3', 'b_en': '3', 'b_he': '3', 'c_es': '40', 'c_en': '40', 'c_he': '40', 'correct': 'a'}
    ]
    add_questions('Tetzavé', tetzave_q)

    # KI TISÁ
    kitisa_q = [
        {'text_es': '¿Qué daban para el censo?', 'text_en': 'What given for census?', 'text_he': 'מה ניתן למפקד?', 'a_es': 'Medio Shekel plata', 'a_en': 'Half Shekel silver', 'a_he': 'מחצית השקל', 'b_es': 'Un cordero', 'b_en': 'A lamb', 'b_he': 'כבש', 'c_es': 'Oro', 'c_en': 'Gold', 'c_he': 'זהב', 'correct': 'a'},
        {'text_es': '¿Material de la fuente (Kior)?', 'text_en': 'Kior material?', 'text_he': 'חומר הכיור?', 'a_es': 'Bronce', 'a_en': 'Bronze', 'a_he': 'נחושת', 'b_es': 'Plata', 'b_en': 'Silver', 'b_he': 'כסף', 'c_es': 'Oro', 'c_en': 'Gold', 'c_he': 'זהב', 'correct': 'a'},
        {'text_es': '¿Artesano principal?', 'text_en': 'Chief artisan?', 'text_he': 'האומן הראשי?', 'a_es': 'Bezalel', 'a_en': 'Bezalel', 'a_he': 'בצלאל', 'b_es': 'Oholiav', 'b_en': 'Oholiav', 'b_he': 'אהליאב', 'c_es': 'Joshua', 'c_en': 'Joshua', 'c_he': 'יהושע', 'correct': 'a'},
        {'text_es': '¿El gran pecado?', 'text_en': 'The great sin?', 'text_he': 'החטא הגדול?', 'a_es': 'Becerro de oro', 'a_en': 'Golden calf', 'a_he': 'עגל הזהב', 'b_es': 'Murmuración', 'b_en': 'Grumbling', 'b_he': 'תלונה', 'c_es': 'Idolatría de Baal', 'c_en': 'Baal worship', 'c_he': 'עבודה זרה לבעל', 'correct': 'a'},
        {'text_es': '¿Qué hizo Moisés con las tablas?', 'text_en': 'What Moses did with tablets?', 'text_he': 'מה משה עשה ללוחות?', 'a_es': 'Las rompió', 'a_en': 'Broke them', 'a_he': 'שיבר אותם', 'b_es': 'Las escondió', 'b_en': 'Hid them', 'b_he': 'החביא', 'c_es': 'Las bendijo', 'c_en': 'Blessed them', 'c_he': 'בירך', 'correct': 'a'},
        {'text_es': '¿Cuántos días estuvo Moisés en el monte?', 'text_en': 'Days Moses on mountain?', 'text_he': 'ימים משה בהר?', 'a_es': '40', 'a_en': '40', 'a_he': '40', 'b_es': '7', 'b_en': '7', 'b_he': '7', 'c_es': '10', 'c_en': '10', 'c_he': '10', 'correct': 'a'},
        {'text_es': '¿Qué irradiaba el rostro de Moisés?', 'text_en': 'Moses face radiated?', 'text_he': 'מה קרן מפני משה?', 'a_es': 'Luz', 'a_en': 'Light', 'a_he': 'אור', 'b_es': 'Agua', 'b_en': 'Water', 'b_he': 'מים', 'c_es': 'Fuego', 'c_en': 'Fire', 'c_he': 'אש', 'correct': 'a'},
        {'text_es': '¿Qué mandamiento antecede a la obra?', 'text_en': 'Which mitzvah before work?', 'text_he': 'איזו מצווה לפני המלאכה?', 'a_es': 'Shabat', 'a_en': 'Shabbat', 'a_he': 'שבת', 'b_es': 'Kashrut', 'b_en': 'Kashrut', 'b_he': 'כשרות', 'c_es': 'Tzedaká', 'c_en': 'Tzedakah', 'c_he': 'צדקה', 'correct': 'a'},
        {'text_es': '¿Quién ayudó a Bezalel?', 'text_en': 'Who helped Bezalel?', 'text_he': 'מי עזר לבצלאל?', 'a_es': 'Oholiav', 'a_en': 'Oholiav', 'a_he': 'אהליאב', 'b_es': 'Eleazar', 'b_en': 'Eleazar', 'b_he': 'אלעזר', 'c_es': 'Nadav', 'c_en': 'Nadav', 'c_he': 'נדב', 'correct': 'a'},
        {'text_es': '¿Para qué se usaba el aceite de unción?', 'text_en': 'Purpose of anointing oil?', 'text_he': 'למה שימן שמן המשחה?', 'a_es': 'Consagrar objetos', 'a_en': 'Consecrate objects', 'a_he': 'קידוש כלים', 'b_es': 'Cocinar', 'b_en': 'Cooking', 'b_he': 'בישול', 'c_es': 'Iluminación', 'c_en': 'Lighting', 'c_he': 'תאורה', 'correct': 'a'}
    ]
    add_questions('Ki Tisá', kitisa_q)

    # VAYAKHEL
    vayakhel_q = [
        {'text_es': '¿Qué día no se debía encender fuego?', 'text_en': 'Day not to light fire?', 'text_he': 'באיזה יום אסור להבעיר אש?', 'a_es': 'Shabat', 'a_en': 'Shabbat', 'a_he': 'שבת', 'b_es': 'Yom Kippur', 'b_en': 'Yom Kippur', 'b_he': 'יום כיפור', 'c_es': 'Lunes', 'c_en': 'Monday', 'c_he': 'שני', 'correct': 'a'},
        {'text_es': '¿Quiénes trajeron ofrendas?', 'text_en': 'Who brought offerings?', 'text_he': 'מי הביאו נדבה?', 'a_es': 'Hombres y mujeres', 'a_en': 'Men and women', 'a_he': 'הגברים והנשים', 'b_es': 'Solo hombres', 'b_en': 'Only men', 'b_he': 'רק גברים', 'c_es': 'Solo los príncipes', 'c_en': 'Only princes', 'c_he': 'רק נשיאים', 'correct': 'a'},
        {'text_es': '¿Qué trajeron las mujeres sabias?', 'text_en': 'What did wise women bring?', 'text_he': 'מה הביאו הנשים החכמות?', 'a_es': 'Pelo de cabra hilado', 'a_en': 'Spun goat hair', 'a_he': 'שיער עיזים טווי', 'b_es': 'Pan', 'b_en': 'Bread', 'b_he': 'לחם', 'c_es': 'Vino', 'c_en': 'Wine', 'c_he': 'יין', 'correct': 'a'},
        {'text_es': '¿Qué pasó con las ofrendas?', 'text_en': 'What happened with offerings?', 'text_he': 'מה קרה עם הנדבה?', 'a_es': 'Hubo demasiado', 'a_en': 'There was too much', 'a_he': 'היה יותר מדי', 'b_es': 'Faltó material', 'b_en': 'Lacked material', 'b_he': 'היה חסר', 'c_es': 'Se perdieron', 'c_en': 'They were lost', 'c_he': 'אבדו', 'correct': 'a'},
        {'text_es': '¿De qué tribu era Bezalel?', 'text_en': 'What tribe was Bezalel?', 'text_he': 'מאיזה שבט בצלאל?', 'a_es': 'Judá', 'a_en': 'Judah', 'a_he': 'יהודה', 'b_es': 'Dan', 'b_en': 'Dan', 'b_he': 'דן', 'c_es': 'Levi', 'c_en': 'Levi', 'c_he': 'לוי', 'correct': 'a'},
        {'text_es': '¿De qué tribu era Oholiav?', 'text_en': 'What tribe was Oholiav?', 'text_he': 'מאיזה שבט אהליאב?', 'a_es': 'Dan', 'a_en': 'Dan', 'a_he': 'דן', 'b_es': 'Judá', 'b_en': 'Judah', 'b_he': 'יהודה', 'c_es': 'Rubén', 'c_en': 'Reuben', 'c_he': 'ראובן', 'correct': 'a'},
        {'text_es': '¿Qué material cubría el Tabernáculo?', 'text_en': 'Material covering Tabernacle?', 'text_he': 'מה כיסה את המשכן?', 'a_es': 'Pieles y telas', 'a_en': 'Skins and cloths', 'a_he': 'עורות ויריעות', 'b_es': 'Piedra', 'b_en': 'Stone', 'b_he': 'אבן', 'c_es': 'Ladrillo', 'c_en': 'Brick', 'c_he': 'לבנה', 'correct': 'a'},
        {'text_es': '¿Cuántas lámparas tenía la Menorá?', 'text_en': 'Lamps on Menorah?', 'text_he': 'כמה נרות במנורה?', 'a_es': '7', 'a_en': '7', 'a_he': '7', 'b_es': '9', 'b_en': '9', 'b_he': '9', 'c_es': '12', 'c_en': '12', 'c_he': '12', 'correct': 'a'},
        {'text_es': '¿Dónde se ponía el Incienso?', 'text_en': 'Where was Incense?', 'text_he': 'איפה הוקטרה הקטורת?', 'a_es': 'Altar de oro', 'a_en': 'Golden Altar', 'a_he': 'מזבח הזהב', 'b_es': 'Altar de bronce', 'b_en': 'Bronze Altar', 'b_he': 'מזבח הנחושת', 'c_es': 'Afuera', 'c_en': 'Outside', 'c_he': 'בחוץ', 'correct': 'a'},
        {'text_es': '¿Material de la mesa?', 'text_en': 'Table material?', 'text_he': 'חומר השולחן?', 'a_es': 'Madera de acacia y oro', 'a_en': 'Acacia and gold', 'a_he': 'עצי שיטים וזהב', 'b_es': 'Pura plata', 'b_en': 'Pure silver', 'b_he': 'כסף טהור', 'c_es': 'Mármol', 'c_en': 'Marble', 'c_he': 'שיש', 'correct': 'a'}
    ]
    add_questions('Vayakhel', vayakhel_q)

    # PEKUDÉ
    pekude_q = [
        {'text_es': '¿Qué se hizo al final de la obra?', 'text_en': 'What done at end of work?', 'text_he': 'מה נעשה בסוף המלאכה?', 'a_es': 'Un recuento (Pekudé)', 'a_en': 'An accounting (Pekudei)', 'a_he': 'חשבון (פקודי)', 'b_es': 'Una fiesta', 'b_en': 'A party', 'b_he': 'מסיבה', 'c_es': 'Un viaje', 'c_en': 'A trip', 'c_he': 'מסע', 'correct': 'a'},
        {'text_es': '¿Quién hizo el recuento?', 'text_en': 'Who did the accounting?', 'text_he': 'מי ערך את החשבון?', 'a_es': 'Itamar ben Aharón', 'a_en': 'Itamar son of Aaron', 'a_he': 'איתמר בן אהרן', 'b_es': 'Joshua', 'b_en': 'Joshua', 'b_he': 'יהושע', 'c_es': 'Caleb', 'c_en': 'Caleb', 'c_he': 'כלב', 'correct': 'a'},
        {'text_es': '¿Cuánta plata se usó?', 'text_en': 'How much silver used?', 'text_he': 'כמה כסף הוקדש?', 'a_es': '100 talentos aprox.', 'a_en': 'About 100 talents', 'a_he': '100 כיכר בערך', 'b_es': '10 talentos', 'b_en': '10 talents', 'b_he': '10 כיכר', 'c_es': 'Ninguna', 'c_en': 'None', 'c_he': 'כלום', 'correct': 'a'},
        {'text_es': '¿Qué se hizo con la plata del censo?', 'text_en': 'Plata used for?', 'text_he': 'מה עשו עם כסף המפקד?', 'a_es': 'Basas (Adanim)', 'a_en': 'Sockets (Adanim)', 'a_he': 'אדנים', 'b_es': 'Velas', 'b_en': 'Candles', 'b_he': 'נרות', 'c_es': 'Coronas', 'c_en': 'Crowns', 'c_he': 'כתרים', 'correct': 'a'},
        {'text_es': '¿Quién bendijo al pueblo?', 'text_en': 'Who blessed the people?', 'text_he': 'מי בירך את העם?', 'a_es': 'Moisés', 'a_en': 'Moses', 'a_he': 'משה', 'b_es': 'Aharón', 'b_en': 'Aaron', 'b_he': 'אהרן', 'c_es': 'Miriam', 'c_en': 'Miriam', 'c_he': 'מרים', 'correct': 'a'},
        {'text_es': '¿Qué día se erigió el Tabernáculo?', 'text_en': 'Day Tabernacle erected?', 'text_he': 'באיזה יום הוקם המשכן?', 'a_es': '1 de Nisán', 'a_en': '1st of Nissan', 'a_he': 'א\' בניסן', 'b_es': '1 de Tishrei', 'b_en': '1st of Tishrei', 'b_he': 'א\' בתשרי', 'c_es': '15 de Adar', 'c_en': '15th of Adar', 'c_he': 'ט"ו באדר', 'correct': 'a'},
        {'text_es': '¿Qué llenó el Tabernáculo al terminar?', 'text_en': 'What filled Tabernacle?', 'text_he': 'מה מילא את המשכן בסוף?', 'a_es': 'La nube (Gloria de Dios)', 'a_en': 'The cloud (God\'s glory)', 'a_he': 'הענן (כבוד ה\')', 'b_es': 'Agua', 'b_en': 'Water', 'b_he': 'מים', 'c_es': 'Fuego devorador', 'c_en': 'Consuming fire', 'c_he': 'אש אוכלה', 'correct': 'a'},
        {'text_es': '¿Cómo sabía el pueblo cuándo viajar?', 'text_en': 'How knew when to travel?', 'text_he': 'איך ידעו מתי לנסוע?', 'a_es': 'Cuando se elevaba la nube', 'a_en': 'When cloud lifted', 'a_he': 'כשעלה הענן', 'b_es': 'Por trompetas solas', 'b_en': 'By trumpets only', 'b_he': 'רק בחצוצרות', 'c_es': 'Por sorteo', 'c_en': 'By lottery', 'c_he': 'גורל', 'correct': 'a'},
        {'text_es': '¿Qué había sobre el Tabernáculo de noche?', 'text_en': 'What over Tabernacle at night?', 'text_he': 'מה היה על המשכן בלילה?', 'a_es': 'Fuego', 'a_en': 'Fire', 'a_he': 'אש', 'b_es': 'Lluvia', 'b_en': 'Rain', 'b_he': 'גשם', 'c_es': 'Estrellas fugaces', 'c_en': 'Shooting stars', 'c_he': 'כוכבים', 'correct': 'a'},
        {'text_es': '¿Con qué termina el libro de Éxodo?', 'text_en': 'Exodus ends with?', 'text_he': 'במה מסתיים ספר שמות?', 'a_es': 'La nube cubriendo el Mishkán', 'a_en': 'Cloud covering Mishkan', 'a_he': 'הענן מכסה את המשכן', 'b_es': 'La muerte de José', 'b_en': 'Joseph\'s death', 'b_he': 'מות יוסף', 'c_es': 'Cruzando el mar', 'c_en': 'Crossing the sea', 'c_he': 'קריעת ים סוף', 'correct': 'a'}
    ]
    add_questions('Pekudé', pekude_q)

    # VAYIKRÁ
    vayikra_q = [
        {'text_es': '¿A quién llamó Dios desde el Tabernáculo?', 'text_en': 'Who did God call from Tabernacle?', 'text_he': 'אל מי קרא ה\' מהמשכן?', 'a_es': 'Moisés', 'a_en': 'Moses', 'a_he': 'משה', 'b_es': 'Aharón', 'b_en': 'Aaron', 'b_he': 'אהרן', 'c_es': 'Los ancianos', 'c_en': 'Elders', 'c_he': 'הזקנים', 'correct': 'a'},
        {'text_es': '¿Cómo se llama el sacrificio que se eleva?', 'text_en': 'Sacrifice that goes up?', 'text_he': 'איך נקרא הקורבן שעולה?', 'a_es': 'Olá', 'a_en': 'Olah', 'a_he': 'עולה', 'b_es': 'Jatat', 'b_en': 'Chatat', 'b_he': 'חטאת', 'c_es': 'Asham', 'c_en': 'Asham', 'c_he': 'אשם', 'correct': 'a'},
        {'text_es': '¿Qué ofrenda es de harina y aceite?', 'text_en': 'Flour and oil offering?', 'text_he': 'קורבן מנחה עשוי מ...?', 'a_es': 'Minjá', 'a_en': 'Minchah', 'a_he': 'מנחה', 'b_es': 'Olah', 'b_en': 'Olah', 'b_he': 'עולה', 'c_es': 'Asham', 'c_en': 'Asham', 'c_he': 'אשם', 'correct': 'a'},
        {'text_es': '¿Qué ingrediente está prohibido en la Minjá?', 'text_en': 'Ingredient forbidden in Mincha?', 'text_he': 'מה אסור במנחה?', 'a_es': 'Levadura y miel', 'a_en': 'Leaven and honey', 'a_he': 'שאור ודבש', 'b_es': 'Sal', 'b_en': 'Salt', 'b_he': 'מלח', 'c_es': 'Agua', 'c_en': 'Water', 'c_he': 'מים', 'correct': 'a'},
        {'text_es': '¿Qué debe acompañar a todas las ofrendas?', 'text_en': 'What accompanies every offering?', 'text_he': 'מה חייב לבוא בכל קורבן?', 'a_es': 'Sal', 'a_en': 'Salt', 'a_he': 'מלח', 'b_es': 'Incienso', 'b_en': 'Incense', 'b_he': 'לבונה', 'c_es': 'Vino', 'c_en': 'Wine', 'c_he': 'יין', 'correct': 'a'},
        {'text_es': '¿Qué sacrificio es de "paz"?', 'text_en': 'Peace offering?', 'text_he': 'קורבן שלום?', 'a_es': 'Shelamim', 'a_en': 'Shelamim', 'a_he': 'שלמים', 'b_es': 'Olah', 'b_en': 'Olah', 'b_he': 'עולה', 'c_es': 'Chatat', 'c_en': 'Chatat', 'c_he': 'חטאת', 'correct': 'a'},
        {'text_es': '¿Para qué es el sacrificio Jatat?', 'text_en': 'Purpose of Chatat?', 'text_he': 'למה מיועד קורבן חטאת?', 'a_es': 'Expiar pecado involuntario', 'a_en': 'Atone for unintentional sin', 'a_he': 'כפרה על חטא בשוגג', 'b_es': 'Dar gracias', 'b_en': 'Give thanks', 'b_he': 'תודה', 'c_es': 'Celebrar fiesta', 'c_en': 'Celebrate holiday', 'c_he': 'בחג', 'correct': 'a'},
        {'text_es': '¿Qué se hacía con la sangre en el Jatat?', 'text_en': 'Blood in Chatat used for?', 'text_he': 'מה עשו עם הדם בחטאת?', 'a_es': 'Se rociaba ante el velo', 'a_en': 'Sprinkled before veil', 'a_he': 'הזיה מול הפרוכת', 'b_es': 'Se tiraba afuera', 'b_en': 'Thrown outside', 'b_he': 'נשפך בחוץ', 'c_es': 'Se bebía', 'c_en': 'Drunk', 'c_he': 'שתייה', 'correct': 'a'},
        {'text_es': '¿Qué animal podía traer un pobre como Olá?', 'text_en': 'What could a poor person bring?', 'text_he': 'מה יכול עני להביא לעולה?', 'a_es': 'Tórtolas o palominos', 'a_en': 'Turtledoves or pigeons', 'a_he': 'תורים או בני יונה', 'b_es': 'Un buey', 'b_en': 'An ox', 'b_he': 'פר', 'c_es': 'Un camello', 'c_en': 'A camel', 'c_he': 'גמל', 'correct': 'a'},
        {'text_es': '¿Qué parte del animal nunca se comía?', 'text_en': 'Part never eaten?', 'text_he': 'מה אסור לאכול מהקורבן?', 'a_es': 'Grasa (Jelev) y sangre', 'a_en': 'Fat (Chelev) and blood', 'a_he': 'חלב ודם', 'b_es': 'Músculos', 'b_en': 'Muscles', 'b_he': 'בשר', 'c_es': 'Piel', 'c_en': 'Skin', 'c_he': 'עור', 'correct': 'a'}
    ]
    add_questions('Vayikrá', vayikra_q)

    db.session.commit()
