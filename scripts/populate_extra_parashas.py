from app import create_app, db
from app.models import Parasha, Question
from datetime import datetime, date
import random

def add_parasha_with_questions(name_es, name_en, name_he, start_date, end_date, questions):
    # Check if parasha exists
    p = Parasha.query.filter_by(name_es=name_es).first()
    if not p:
        p = Parasha(
            name_es=name_es,
            name_en=name_en,
            name_he=name_he,
            week_start=start_date,
            week_end=end_date
        )
        db.session.add(p)
        db.session.flush() # Get ID
        print(f"Created Parasha: {name_es}")
    else:
        print(f"Parasha {name_es} already exists, clearing old questions and adding new ones...")
        # Clear existing questions for this parasha to avoid duplicates if re-running
        Question.query.filter_by(parasha_id=p.id).delete()

    # Randomize questions order
    random.shuffle(questions)

    for q_data in questions:
        # Prepare options and randomize them
        # Note: input data must have a_es, a_en, a_he, b_es, b_en, b_he, c_es, c_en, c_he
        options = [
            {'es': q_data['a_es'], 'en': q_data['a_en'], 'he': q_data['a_he'], 'orig': 'a'},
            {'es': q_data['b_es'], 'en': q_data['b_en'], 'he': q_data['b_he'], 'orig': 'b'},
            {'es': q_data['c_es'], 'en': q_data['c_en'], 'he': q_data['c_he'], 'orig': 'c'}
        ]
        random.shuffle(options)
        
        # Map back to a, b, c and find which one is the correct one
        # In our input data, 'a' is always correct
        final_correct = 'a'
        for i, letter in enumerate(['a', 'b', 'c']):
            if options[i]['orig'] == 'a':
                final_correct = letter

        q = Question(
            parasha_id=p.id,
            text_es=q_data['t_es'], text_en=q_data['t_en'], text_he=q_data['t_he'],
            option_a_es=options[0]['es'], option_a_en=options[0]['en'], option_a_he=options[0]['he'],
            option_b_es=options[1]['es'], option_b_en=options[1]['en'], option_b_he=options[1]['he'],
            option_c_es=options[2]['es'], option_c_en=options[2]['en'], option_c_he=options[2]['he'],
            correct_option=final_correct
        )
        db.session.add(q)
    
    db.session.commit()
    print(f"Added {len(questions)} questions to {name_es}")

# --- DATA ---

tzav_qs = [
    {
        't_es': '¿Cuál es la ley de "Pigul" en un sacrificio?',
        't_en': 'What is the law of "Pigul" in a sacrifice?',
        't_he': 'מהו דין "פיגול" בקורבן?',
        'a_es': 'Cuando se tiene la intención de comerlo fuera del tiempo permitido', 'a_en': 'When there is an intention to eat it outside the permitted time', 'a_he': 'מחשבת חוץ לזמנו - כוונה לאכול מהזבח לאחר הזמן המותר',
        'b_es': 'Cuando el animal tiene un defecto físico leve', 'b_en': 'When the animal has a minor physical defect', 'b_he': 'כשהבהמה בעלת מום קל',
        'c_es': 'Cuando el sacerdote no está vestido correctamente', 'c_en': 'When the priest is not dressed correctly', 'c_he': 'כשהכהן אינו לבוש בבגדי כהונה כראוי',
    },
    {
        't_es': '¿Qué es la "Terumat Hadeshen" que se realizaba cada mañana?',
        't_en': 'What is the "Terumat Hadeshen" performed every morning?',
        't_he': 'מהי "תרומת הדשן" הנעשית בכל בוקר?',
        'a_es': 'Retirar una pequeña cantidad de cenizas del altar y ponerlas a un lado', 'a_en': 'Removing a small amount of ashes from the altar and placing them aside', 'a_he': 'הרמת כמות קטנה של דשן (אפר) מהמזבח והנחתה בצד',
        'b_es': 'Traer leña nueva para el fuego del Santuario', 'b_en': 'Bringing new wood for the Sanctuary fire', 'b_he': 'הבאת עצים חדשים למערכה',
        'c_es': 'Lavar las vasijas del Templo con agua pura', 'c_en': 'Washing the Temple vessels with pure water', 'c_he': 'שטיפת כלי המקדש במים טהורים',
    },
    {
        't_es': '¿Cuánto tiempo debe arder el fuego sobre el altar del Tabernáculo?',
        't_en': 'How long must the fire burn on the Tabernacle altar?',
        't_he': 'כמה זמן צריכה אש המזבח לדלוק במשכן?',
        'a_es': 'Continuamente, nunca debe apagarse', 'a_en': 'Continuously, it must never be extinguished', 'a_he': 'אש תמיד תוקד על המזבח לא תכבה',
        'b_es': 'Solo durante las horas del día', 'b_en': 'Only during daylight hours', 'b_he': 'רק בשעות היום',
        'c_es': 'Solo mientras haya sacrificios presentes', 'c_en': 'Only while sacrifices are present', 'c_he': 'רק בזמן שיש עליו קורבנות',
    },
    {
        't_es': '¿Cuál es la diferencia en la aplicación de la sangre entre la Chatat y la Asham?',
        't_en': 'What is the difference in blood application between Chatat and Asham?',
        't_he': 'מהו ההבדל בנתינת הדם בין קורבן חטאת לקורבן אשם?',
        'a_es': 'En la Chatat se pone en los cuernos del altar; en la Asham se rocía en la base', 'a_en': 'In Chatat it is placed on the altar horns; in Asham it is sprinkled on the base', 'a_he': 'חטאת על קרנות המזבח, ואשם בזריקה על היסוד',
        'b_es': 'No hay diferencia, ambas se aplican igual', 'b_en': 'There is no difference, both are applied the same', 'b_he': 'אין הבדל, שניהם נתנים באותה צורה',
        'c_es': 'La sangre de la Asham se quema totalmente', 'c_en': 'The Asham blood is completely burned', 'c_he': 'דם האשם נשרף כולו במערכה',
    },
    {
        't_es': '¿Quiénes tienen permitido comer de la ofrenda de agradecimiento (Korban Todá)?',
        't_en': 'Who is permitted to eat from the thanksgiving offering (Korban Todah)?',
        't_he': 'מי רשאי לאכול מקורבן התודה?',
        'a_es': 'El dueño, su familia y amigos, durante un día y una noche', 'a_en': 'The owner, their family, and friends, for one day and one night', 'a_he': 'הבעלים, משפחתו ואורחיו, ליום ולילה',
        'b_es': 'Únicamente los Cohanim (Sacerdotes)', 'b_en': 'Only the Kohanim (Priests)', 'b_he': 'רק הכהנים ובני משפחתם',
        'c_es': 'Cualquier persona que pase por el Tabernáculo', 'c_en': 'Anyone passing by the Tabernacle', 'c_he': 'כל אדם שנמצא בעזרה באותו זמן',
    },
    {
        't_es': '¿Qué sucedió durante los "Siete Días de la Iniciación" (Shivat Yemei HaMiluim)?',
        't_en': 'What happened during the "Seven Days of Initiation" (Shivat Yemei HaMiluim)?',
        't_he': 'מה אירע במהלך "שבעת ימי המילואים"?',
        'a_es': 'Aarón y sus hijos permanecieron en la entrada del Tabernáculo preparándose', 'a_en': 'Aaron and his sons remained at the Tabernacle entrance preparing', 'a_he': 'אהרן ובניו שהו בפתח אוהל מועד לצורך חניכתם לכהונה',
        'b_es': 'Moisés escribió el primer rollo de la Torá', 'b_en': 'Moses wrote the first Torah scroll', 'b_he': 'משה רבנו כתב את ספר התורה הראשון',
        'c_es': 'El pueblo ayunó para purificar sus corazones', 'c_en': 'The people fasted to purify their hearts', 'c_he': 'כל עם ישראל צם לצורך טהרת הלב',
    },
    {
        't_es': '¿Qué tipos de madera estaban excluidos para el fuego del Altar?',
        't_en': 'Which types of wood were excluded for the Altar fire?',
        't_he': 'אילו סוגי עצים היו פסולים למערכה על המזבח?',
        'a_es': 'Vid y Olivo', 'a_en': 'Vine and Olive', 'a_he': 'עץ גפן ועץ זית',
        'b_es': 'Cedro y Pino', 'b_en': 'Cedar and Pine', 'b_he': 'ארז ואורן',
        'c_es': 'Roble y Acacia', 'c_en': 'Oak and Acacia', 'c_he': 'אלון ושיטה',
    },
    {
        't_es': '¿Cuántos panes en total se traían con el Korban Todá?',
        't_en': 'How many loaves of bread in total were brought with the Korban Todah?',
        't_he': 'כמה לחמים סך הכל הובאו עם קורבן התודה?',
        'a_es': '40 panes (10 de cuatro tipos diferentes)', 'a_en': '40 loaves (10 of four different types)', 'a_he': 'ארבעים לחמים (עשרה מכל סוג)',
        'b_es': '12 panes (uno por cada tribu)', 'b_en': '12 loaves (one for each tribe)', 'b_he': 'שנים עשר לחמים כנגד השבטים',
        'c_es': 'Solo un pan grande de masa pura', 'c_en': 'Only one large loaf of pure dough', 'c_he': 'כיכר לחם אחת גדולה וקדושה',
    },
    {
        't_es': '¿Qué nombre recibe la parte del sacrificio que sobra después del tiempo permitido?',
        't_en': 'What is the name of the part of the sacrifice left over after the permitted time?',
        't_he': 'איך נקרא בשר קורבן שנותר לאחר זמן אכילתו?',
        'a_es': 'Notar', 'a_en': 'Notar', 'a_he': 'נותר',
        'b_es': 'Kodesh', 'b_en': 'Kodesh', 'b_he': 'קודש',
        'c_es': 'Tamei', 'c_en': 'Tamei', 'c_he': 'טמא',
    },
    {
        't_es': '¿Qué buscaba simbolizar el sacrificio de "Chatat Miluim"?',
        't_en': 'What did the "Chatat Miluim" sacrifice aim to symbolize?',
        't_he': 'מה סימל קורבן "חטאת המילואים"?',
        'a_es': 'La expiación y pureza necesaria de los sacerdotes antes de su labor', 'a_en': 'The atonement and purity necessary for the priests before their work', 'a_he': 'כפרה וטהרה לכהנים קודם שהתחילו בעבודתם',
        'b_es': 'La alegría por la construcción del Tabernáculo', 'b_en': 'The joy for the construction of the Tabernacle', 'b_he': 'שמחה על סיום בניית המשכן',
        'c_es': 'Un regalo general de todo el pueblo a Dios', 'c_en': 'A general gift from all the people to God', 'c_he': 'מתנה כללית של כל עם ישראל לה\'',
    },
]

shemini_qs = [
    {
        't_es': '¿En qué fecha culminó la inauguración del Tabernáculo?',
        't_en': 'On what date did the Tabernacle inauguration culminate?',
        't_he': 'באיזה תאריך הגיע לשיאו חנוכת המשכן (יום השמיני)?',
        'a_es': '1 de Nisán', 'a_en': '1st of Nisan', 'a_he': 'א\' בניסן',
        'b_es': '15 de Nisán', 'b_en': '15th of Nisan', 'b_he': 'ט"ו בניסן',
        'c_es': '1 de Tishrei', 'c_en': '1st of Tishrei', 'c_he': 'א\' בתשרי',
    },
    {
        't_es': '¿Por qué murieron Nadav y Avihu según el texto bíblico?',
        't_en': 'Why did Nadav and Avihu die according to the biblical text?',
        't_he': 'מדוע מתו נדב ואביהוא על פי פשט הכתוב?',
        'a_es': 'Por ofrecer un "fuego extraño" que Dios no había pedido', 'a_en': 'For offering an "alien fire" that God had not commanded', 'a_he': 'כי הקריבו אש זרה אשר לא ציווה ה\' אותם',
        'b_es': 'Por entrar al Santuario sin lavarse las manos', 'b_en': 'For entering the Sanctuary without washing their hands', 'b_he': 'כי נכנסו למקדש בלא רחיצת ידים ורגלים',
        'c_es': 'Por olvidar encender la Menorá', 'c_en': 'For forgetting to light the Menorah', 'c_he': 'כי שכחו להדליק את המנורה',
    },
    {
        't_es': '¿Cuál fue la respuesta de Aarón ante la pérdida de sus hijos?',
        't_en': 'What was Aaron\'s response to the loss of his sons?',
        't_he': 'מה הייתה תגובת אהרן על מות בניו?',
        'a_es': 'Permaneció en silencio (Vayidom Aharon)', 'a_en': 'He remained silent (Vayidom Aharon)', 'a_he': 'וידום אהרן - קיבל את הדין בשתיקה',
        'b_es': 'Gritó amargamente ante todo el pueblo', 'b_en': 'He cried out bitterly before all the people', 'b_he': 'צעקה גדולה ומרה לפני כל העם',
        'c_es': 'Compuso una canción de duelo de inmediato', 'c_en': 'He composed a mourning song immediately', 'c_he': 'חיבר קינה ושר אותה מיד',
    },
    {
        't_es': '¿Cuáles son las dos señales de un mamífero kosher?',
        't_en': 'What are the two signs of a kosher mammal?',
        't_he': 'מהם שני הסימנים של בהמה טהורה?',
        'a_es': 'Pezuña partida y que rumie su comida', 'a_en': 'Split hooves and chewing its cud', 'a_he': 'מפרסת פרסה ומעלה גירה',
        'b_es': 'Que tenga cuernos y sea herbívoro', 'b_en': 'That it has horns and is a herbivore', 'b_he': 'שיש לה קרניים והיא אוכלת עשב בלבד',
        'c_es': 'Que sea de color blanco o marrón claro', 'c_en': 'That it is white or light brown in color', 'c_he': 'צבע עור לבן או חום בהיר',
    },
    {
        't_es': 'Nombre un animal mencionado que solo tiene una señal de pureza.',
        't_en': 'Name a mentioned animal that has only one purity sign.',
        't_he': 'ציין חיה המוזכרת שיש לה רק סימן טהרה אחד.',
        'a_es': 'Camello (rumia pero no tiene pezuña partida)', 'a_en': 'Camel (chews cud but has no split hoof)', 'a_he': 'הגמל (מעלה גירה אך פרסתו אינה שסועה)',
        'b_es': 'León (ni rumia ni tiene pezuña)', 'b_en': 'Lion (neither chews cud nor has split hooves)', 'b_he': 'אריה (אין לו אף סימן טהרה)',
        'c_es': 'Ciervo (tiene ambas señales)', 'c_en': 'Deer (has both signs)', 'c_he': 'איל (יש לו את שני הסימנים)',
    },
    {
        't_es': '¿Qué señales deben tener los peces para ser permitidos?',
        't_en': 'What signs must fish have to be permitted?',
        't_he': 'אילו סימנים צריכים להיות בדגים כדי שיהיו מותרים באכילה?',
        'a_es': 'Aletas y escamas', 'a_en': 'Fins and scales', 'a_he': 'סנפיר וקשקשת',
        'b_es': 'Branquias y cola larga', 'b_en': 'Gills and a long tail', 'b_he': 'זימים וזנב ארוך',
        'c_es': 'Dientes pequeños y ojos redondos', 'c_en': 'Small teeth and round eyes', 'c_he': 'שיניים קטנות ועיניים עגולות',
    },
    {
        't_es': '¿Cuántos tipos de langostas/saltamontes se mencionan como posibles de ser kosher?',
        't_en': 'How many types of locusts/grasshoppers are mentioned as potentially kosher?',
        't_he': 'כמה סוגי חגבים מוזכרים כטהורים?',
        'a_es': '4 tipos principales', 'a_en': '4 main types', 'a_he': 'ארבעה סוגים (ארבה, סלעם, חרגול וחגב)',
        'b_es': 'Solo 1 tipo específico', 'b_en': 'Only 1 specific type', 'b_he': 'סוג אחד בלבד',
        'c_es': 'Ninguno, todos están prohibidos', 'c_en': 'None, all are forbidden', 'c_he': 'אף אחד, כולם אסורים',
    },
    {
        't_es': '¿Cuál es el estado de impureza de quien toca el cadáver de un animal no puro?',
        't_en': 'What is the state of impurity of someone who touches the carcass of a non-pure animal?',
        't_he': 'מה דין אדם הנוגע בנבלת בהמה טמאה?',
        'a_es': 'Queda impuro hasta el anochecer', 'a_en': 'Remains impure until evening', 'a_he': 'טמא עד הערב',
        'b_es': 'Debe permanecer fuera del campamento 7 días', 'b_en': 'Must remain outside the camp for 7 days', 'b_he': 'צריך לשבת מחוץ למחנה שבעה ימים',
        'c_es': 'No le sucede nada si se lava las manos', 'c_en': 'Nothing happens if they wash their hands', 'c_he': 'אינו נטמא כלל אם רחץ ידיו',
    },
    {
        't_es': '¿Por qué se prohibió el luto a Aarón y sus hijos sobrevivientes?',
        't_en': 'Why was mourning forbidden for Aaron and his surviving sons?',
        't_he': 'מדוע נאסר על אהרן ובניו הנותרים להתאבל על מות נדב ואביהוא?',
        'a_es': 'Porque estaban consagrados con el aceite de unción y el gozo del Tabernáculo primaba', 'a_en': 'Because they were consecrated with anointing oil and Tabernacle joy took precedence', 'a_he': 'משום ששמן משחת ה\' עליהם ועבודת המקדש אינה נדחית',
        'b_es': 'Porque sus hijos no eran considerados dignos de luto', 'b_en': 'Because their sons were not considered worthy of mourning', 'b_he': 'כי בניהם לא היו ראויים שיתאבלו עליהם',
        'c_es': 'Fue un castigo adicional por el pecado familiar', 'c_en': 'It was an additional punishment for the family sin', 'c_he': 'זה היה עונש נוסף על חטא העגל',
    },
    {
        't_es': '¿Qué animal simboliza la expiación por el error de los hijos de Israel en el día octavo?',
        't_en': 'Which animal symbolizes atonement for the Israelites\' error on the eighth day?',
        't_he': 'איזה בעל חיים הוקרב כחטאת עבור עם ישראל ביום השמיני?',
        'a_es': 'Un macho cabrío (Seir Isim)', 'a_en': 'A he-goat (Seir Izim)', 'a_he': 'שעיר עזים לחטאת',
        'b_es': 'Un cordero de un año', 'b_en': 'A year-old lamb', 'b_he': 'כבש בן שנתו',
        'c_es': 'Una paloma blanca', 'c_en': 'A white dove', 'c_he': 'תור או בן יונה',
    },
]

tazria_qs = [
    {
        't_es': '¿A los cuántos días se debe realizar el Brit Milá (circuncisión)?',
        't_en': 'After how many days should the Brit Milah (circumcision) be performed?',
        't_he': 'באיזה יום מלים את הבן?',
        'a_es': 'Al octavo día', 'a_en': 'On the eighth day', 'a_he': 'ביום השמיני',
        'b_es': 'Al nacer', 'b_en': 'At birth', 'b_he': 'ביום הלידה',
        'c_es': 'A los treinta días', 'c_en': 'After thirty days', 'c_he': 'לאחר שלושים יום',
    },
    {
        't_es': '¿Cuál es el periodo total de purificación tras el nacimiento de un niño?',
        't_en': 'What is the total purification period after the birth of a boy?',
        't_he': 'כמה ימי טהרה יש לאישה היולדת בן (בסך הכל)?',
        'a_es': '40 días', 'a_en': '40 days', 'a_he': 'ארבעים יום (7 + 33)',
        'b_es': '7 días', 'b_en': '7 days', 'b_he': 'שבעה ימים',
        'c_es': '14 días', 'c_en': '14 days', 'c_he': 'ארבעה עשר יום',
    },
    {
        't_es': '¿Y tras el nacimiento de una niña?',
        't_en': 'And after the birth of a girl?',
        't_he': 'וכמה ימי טהרה יש ליולדת בת?',
        'a_es': '80 días', 'a_en': '80 days', 'a_he': 'שמונים יום (14 + 66)',
        'b_es': '40 días', 'b_en': '40 days', 'b_he': 'ארבעים יום',
        'c_es': '120 días', 'c_en': '120 days', 'c_he': 'מאה ועשרים יום',
    },
    {
        't_es': '¿Qué es esencialmente la "Tzara\'at" según la tradición?',
        't_en': 'What is essentially "Tzara\'at" according to tradition?',
        't_he': 'מהי מהות הצרעת על פי המסורת?',
        'a_es': 'Una manifestación física de un mal espiritual', 'a_en': 'A physical manifestation of a spiritual malady', 'a_he': 'נגע רוחני המתבטא בגוף באופן פיזי',
        'b_es': 'Una infección contagiosa común', 'b_en': 'A common contagious infection', 'b_he': 'מחלה מדבקת רגילה',
        'c_es': 'Una reacción alérgica a ciertos alimentos', 'c_en': 'An allergic reaction to certain foods', 'c_he': 'תגובה אלרגית למאכלים מסוימים',
    },
    {
        't_es': '¿Quién tiene la autoridad de declarar a alguien como "Metzora" (impuro)?',
        't_en': 'Who has the authority to declare someone as "Metzora" (impure)?',
        't_he': 'ביד מי הכוח להחליט אם הנגע טמא או טהור?',
        'a_es': 'El Kohen (Sacerdote)', 'a_en': 'The Kohen (Priest)', 'a_he': 'הכהן',
        'b_es': 'El médico del campamento', 'b_en': 'The camp doctor', 'b_he': 'רופא המחנה',
        'c_es': 'Cualquier sabio de la Torá', 'c_en': 'Any Torah scholar', 'c_he': 'כל חכם מחכמי התורה',
    },
    {
        't_es': '¿Qué sucede si la mancha de Tzara\'at cubre totalmente el cuerpo?',
        't_en': 'What happens if the Tzara\'at spot covers the entire body?',
        't_he': 'מה הדין אם הפרחה הצרעת ומילאה את כל עורו של האדם?',
        'a_es': 'Paradójicamente, se declara puro (Tahor)', 'a_en': 'Paradoxically, they are declared pure (Tahor)', 'a_he': 'הכל טהור',
        'b_es': 'Se considera en estado crítico de impureza', 'b_en': 'It is considered a critical state of impurity', 'b_he': 'טמא בדרגה חמורה ביותר',
        'c_es': 'Debe ser expulsado definitivamente', 'c_en': 'Must be permanently expelled', 'c_he': 'מורחק מהמחנה לצמיתות',
    },
    {
        't_es': '¿Cuánto tiempo dura la cuarentena inicial para una mancha sospechosa?',
        't_en': 'How long does the initial quarantine for a suspicious spot last?',
        't_he': 'כמה זמן נמשך ההסגר הראשון של בעל הנגע?',
        'a_es': 'Siete días', 'a_en': 'Seven days', 'a_he': 'שבעה ימים',
        'b_es': 'Tres días', 'b_en': 'Three days', 'b_he': 'שלושה ימים',
        'c_es': 'Un mes entero', 'c_en': 'An entire month', 'c_he': 'חודש ימים',
    },
    {
        't_es': '¿Sobre qué materiales puede aparecer la Tzara\'at en objetos?',
        't_en': 'On which materials can Tzara\'at appear on objects?',
        't_he': 'באילו חומרים יכול להופיע נגע הצרעת?',
        'a_es': 'Lana, lino o cuero', 'a_en': 'Wool, linen, or leather', 'a_he': 'צמר, פשתן או עור',
        'b_es': 'Oro y plata', 'b_en': 'Gold and silver', 'b_he': 'זהב וכסף',
        'c_es': 'Piedra y cristal', 'c_en': 'Stone and glass', 'c_he': 'אבן וזכוכית',
    },
    {
        't_es': '¿Cuáles son los nombres de las manchas mencionadas en la Torá?',
        't_en': 'What are the names of the spots mentioned in the Torah?',
        't_he': 'מהם שמות הנגעים המוזכרים בפרשה?',
        'a_es': 'Se\'et, Sapachat y Baheret', 'a_en': 'Se\'et, Sapachat, and Baheret', 'a_he': 'שאת, ספחת ובהרת',
        'b_es': 'Adom, Tsaj e Yarok', 'b_en': 'Adom, Tsach, and Yarok', 'b_he': 'אדום, צח וירוק',
        'c_es': 'Joshek, Or y Mayim', 'c_en': 'Choshek, Or, and Mayim', 'c_he': 'חושך, אור ומים',
    },
    {
        't_es': '¿Con qué transgresión se vincula tradicionalmente al Metzora?',
        't_en': 'With which transgression is the Metzora traditionally linked?',
        't_he': 'עם איזה חטא מקשרים חז"ל את נגע הצרעת?',
        'a_es': 'Lashón Hará (Habla maliciosa)', 'a_en': 'Lashon Hara (Malicious speech)', 'a_he': 'לשון הרע (שורש המילה מצורע: מוציא רע)',
        'b_es': 'Robo y engaño', 'b_en': 'Robbery and deceit', 'b_he': 'גזל ומרמה',
        'c_es': 'Idolatría', 'c_en': 'Idolatry', 'c_he': 'עבודה זרה',
    },
]

metzora_qs = [
    {
        't_es': '¿Qué se hace con las dos aves en la purificación del Metzora?',
        't_en': 'What is done with the two birds in the Metzora\'s purification?',
        't_he': 'מה עושים עם שתי הציפורים בטהרת המצורע?',
        'a_es': 'Una se sacrifica y la otra se libera al campo', 'a_en': 'One is sacrificed and the other is released into the field', 'a_he': 'האחת נשחטת והשנייה משולחת על פני השדה',
        'b_es': 'Ambas se queman totalmente', 'b_en': 'Both are burned completely', 'b_he': 'שתיהן נשרפות כליל',
        'c_es': 'Se regalan a los pobres del campamento', 'c_en': 'They are given as gifts to the camp\'s poor', 'c_he': 'ניתנות במתנה לעניי המחנה',
    },
    {
        't_es': '¿Qué otros elementos se usan en el ritual de las aves?',
        't_en': 'What other elements are used in the bird ritual?',
        't_he': 'אילו פריטים נוספים דרושים לטקס הציפורים?',
        'a_es': 'Madera de cedro, lana carmesí e hisopo', 'a_en': 'Cedar wood, crimson wool, and hyssop', 'a_he': 'עץ ארז, שני תולעת ואזוב',
        'b_es': 'Oro, incienso y mirra', 'b_en': 'Gold, frankincense, and myrrh', 'b_he': 'זהב, לבונה ומר',
        'c_es': 'Aceitunas y ramas de palma', 'c_en': 'Olives and palm branches', 'c_he': 'זיתים וכפות תמרים',
    },
    {
        't_es': '¿Dónde debe permanecer el Metzora en los primeros 7 días de su purificación?',
        't_en': 'Where must the Metzora remain during the first 7 days of their purification?',
        't_he': 'היכן שוהה המצורע בשבעת הימים הראשונים לטהרתו?',
        'a_es': 'Fuera de su propia tienda', 'a_en': 'Outside their own tent', 'a_he': 'מחוץ לאוהלו',
        'b_es': 'Dentro del Santuario', 'b_en': 'Inside the Sanctuary', 'b_he': 'בתוך המשכן',
        'c_es': 'En el techo de su casa', 'c_en': 'On the roof of their house', 'c_he': 'על גג ביתו',
    },
    {
        't_es': '¿Dónde más puede aparecer la plaga de Tzara\'at además del cuerpo y ropa?',
        't_en': 'Where else can the Tzara\'at plague appear besides the body and clothes?',
        't_he': 'היכן עוד יכול להופיע נגע הצרעת מלבד גוף האדם ובגדיו?',
        'a_es': 'En las paredes de las casas', 'a_en': 'On the walls of the houses', 'a_he': 'בכתלי הבתים',
        'b_es': 'En el cauce de los ríos', 'b_en': 'In the riverbeds', 'b_he': 'באפיקי הנחלים',
        'c_es': 'En las herramientas de hierro', 'c_en': 'On iron tools', 'c_he': 'בכלי הברזל',
    },
    {
        't_es': '¿Qué se debe hacer con una casa si la mancha persiste tras la limpieza?',
        't_en': 'What should be done with a house if the spot persists after cleaning?',
        't_he': 'מה דין בית שהנגע חזר ופשׂה בו לאחר הניקוי?',
        'a_es': 'Demolerla y sacar los materiales fuera de la ciudad', 'a_en': 'Demolish it and take the materials outside the city', 'a_he': 'נתיצת הבית והוצאת העצים והאבנים אל מחוץ לעיר',
        'b_es': 'Pintarla de blanco totalmente', 'b_en': 'Paint it completely white', 'b_he': 'לסייד אותו בלבן מחדש',
        'c_es': 'Venderla a un extranjero', 'c_en': 'Sell it to a foreigner', 'c_he': 'למכור אותו לנכרי',
    },
    {
        't_es': '¿Quiénes son definidos como "Zav" o "Zavá"?',
        't_en': 'Who are defined as "Zav" or "Zava"?',
        't_he': 'מי הם ה"זב" וה"זבה"?',
        'a_es': 'Personas con un flujo corporal específico e irregular', 'a_en': 'People with a specific and irregular bodily discharge', 'a_he': 'אנשים שיש להם הפרשה חריגה מגופם המטמאת אותם',
        'b_es': 'Personas que han nacido con defectos', 'b_en': 'People born with defects', 'b_he': 'אנשים שנולדו עם מום',
        'c_es': 'Sacerdotes que han perdido su cargo', 'c_en': 'Priests who have lost their position', 'c_he': 'כהנים שהודחו מתפקידם',
    },
    {
        't_es': '¿Cuántos días deben esperar el Zav o la Zavá tras detenerse el flujo?',
        't_en': 'How many days must a Zav or Zava wait after the discharge stops?',
        't_he': 'כמה ימים נקיים צריכים הזב והזבה לספור?',
        'a_es': 'Siete días limpios', 'a_en': 'Seven clean days', 'a_he': 'שבעה ימים נקיים',
        'b_es': 'Tres días', 'b_en': 'Three days', 'b_he': 'שלושה ימים',
        'c_es': 'Catorce días', 'c_en': 'Fourteen days', 'c_he': 'ארבעה עשר יום',
    },
    {
        't_es': '¿Cómo se purifica alguien en estado de "Keri"?',
        't_en': 'How does someone in a state of "Keri" purify themselves?',
        't_he': 'כיצד נטהר מי שראה קרי?',
        'a_es': 'Inmersión en Mikve y esperar al anochecer', 'a_en': 'Immersion in Mikvah and waiting until evening', 'a_he': 'טבילה במקווה והערב שמש',
        'b_es': 'Ayunando durante 24 horas', 'b_en': 'Fasting for 24 hours', 'b_he': 'תענית של עשרים וארבע שעות',
        'c_es': 'Saliendo al desierto por un día', 'c_en': 'Going out to the desert for one day', 'c_he': 'יציאה למדבר ליום אחד',
    },
    {
        't_es': '¿Qué beneficio espiritual o material traía a veces la Tzara\'at de las casas?',
        't_en': 'What spiritual or material benefit did house Tzara\'at sometimes bring?',
        't_he': 'איזו טובה צמחה לישראל לפעמים מנגעי בתים (לפי המדרש)?',
        'a_es': 'Revelaba tesoros escondidos por los cananeos en las paredes', 'a_en': 'It revealed treasures hidden by Canaanites in the walls', 'a_he': 'גילוי אוצרות שהטמינו כנענים בתוך הכתלים',
        'b_es': 'Indicaba que la casa era de gran valor', 'b_en': 'It indicated the house was of great value', 'b_he': 'סימן שהבית היה חשוב וקדוש',
        'c_es': 'Obligaba a las personas a mudarse a mejores lugares', 'c_en': 'It forced people to move to better places', 'c_he': 'גרם לאנשים לעבור לבתים מפוארים יותר',
    },
    {
        't_es': '¿Qué ofrenda trae el Metzora pobre en su purificación?',
        't_en': 'What offering does the poor Metzora bring in their purification?',
        't_he': 'מהו קורבנו של מצורע עני?',
        'a_es': 'Dos tórtolas o dos pichones de paloma', 'a_en': 'Two turtledoves or two young pigeons', 'a_he': 'שתי תורים או שני בני יונה',
        'b_es': 'Un poco de harina fina solamente', 'b_en': 'Only a bit of fine flour', 'b_he': 'מעט סולת בלבד',
        'c_es': 'Nada, su arrepentimiento es suficiente', 'c_en': 'Nothing, their repentance is enough', 'c_he': 'אינו מביא דבר, תשובתו מכפרת',
    },
]

# --- EXECUTION ---

app = create_app()
with app.app_context():
    # TZAV: March 29 - April 4
    add_parasha_with_questions(
        'Tzav', 'Tzav', 'צו',
        datetime(2026, 3, 29), datetime(2026, 4, 4),
        tzav_qs
    )

    # SHMINI: April 5 - April 11
    add_parasha_with_questions(
        'Sheminí', 'Shemini', 'שמיני',
        datetime(2026, 4, 5), datetime(2026, 4, 11), # Note: Dates are set for 2026
        shemini_qs
    )

    # TAZRIA: April 12 - April 18
    add_parasha_with_questions(
        'Tazría', 'Tazria', 'תזריע',
        datetime(2026, 4, 12), datetime(2026, 4, 18),
        tazria_qs
    )

    # METZORA: April 19 - April 25
    add_parasha_with_questions(
        'Metzorá', 'Metzora', 'מצורע',
        datetime(2026, 4, 19), datetime(2026, 4, 25),
        metzora_qs
    )

    print("Success: 4 Parashot and 40 questions added with randomized options.")
