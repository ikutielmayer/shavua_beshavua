from app import create_app, db
from app.models import Parasha, Question

def add_q(p_name, qs):
    p = Parasha.query.filter_by(name_es=p_name).first()
    if not p: return
    for d in qs:
        q = Question(
            parasha_id=p.id,
            text_es=d['t_es'], text_en=d['t_en'], text_he=d['t_he'],
            option_a_es=d['a_es'], option_a_en=d['a_en'], option_a_he=d['a_he'],
            option_b_es=d['b_es'], option_b_en=d['b_en'], option_b_he=d['b_he'],
            option_c_es=d['c_es'], option_c_en=d['c_en'], option_c_he=d['c_he'],
            correct_option=d['corr']
        )
        db.session.add(q)
    print(f"Added {len(qs)} to {p_name}")

app = create_app()
with app.app_context():
    # VAYIKRA (Nivel Medio-Alto)
    add_q('Vayikrá', [
        {
            't_es': '¿Cuál es el significado espiritual detrás de la palabra inicial "Vayikrá" con la letra "Alef" pequeña?',
            't_en': 'What is the spiritual meaning behind the initial word "Vayikra" with a small "Aleph"?',
            't_he': 'מהו המשמעות הרוחנית של פתיחת ספר ויקרא באות א\' קטנה?',
            'a_es': 'Simboliza la humildad extrema de Moisés', 'a_en': 'It symbolizes the extreme humility of Moses', 'a_he': 'סמל לענווה היתרה של משה רבנו',
            'b_es': 'Fue un error de los escribas antiguos', 'b_en': 'It was an error by ancient scribes', 'b_he': 'טעות סופר קדומה',
            'c_es': 'Para ahorrar espacio en el pergamino inicial', 'c_en': 'To save space on the initial parchment', 'c_he': 'כדי לחסוך מקום בקלף',
            'corr': 'a'
        },
        {
            't_es': '¿Qué distingue al sacrificio "Olá" de otros tipos de sacrificios animales?',
            't_en': 'What distinguishes the "Olah" sacrifice from other types of animal sacrifices?',
            't_he': 'מה מייחד את קורבן העולה מבין שאר הקורבנות?',
            'a_es': 'Se quema en su totalidad en el altar, sin que los sacerdotes coman de él', 'a_en': 'It is burned entirely on the altar, with no portion eaten by the priests', 'a_he': 'הוא מועלה כולו באש ואינו נאכל לכהנים',
            'b_es': 'Solo se ofrece en casos de pecados graves', 'b_en': 'It is only offered in cases of severe sins', 'b_he': 'הוא קרב רק על חטאים חמורים',
            'c_es': 'Se ofrece únicamente fuera del Santuario', 'c_en': 'It is offered solely outside the Sanctuary', 'c_he': 'הוא נאכל לבעליו מחוץ לעזרה',
            'corr': 'a'
        },
        {
            't_es': '¿Por qué la ofrenda de harina (Minjá) es comparada simbólicamente con el alma de quien la ofrece?',
            't_en': 'Why is the flour offering (Mincha) symbolically compared to the soul of the offerer?',
            't_he': 'מדוע קורבן מנחה נחשב כהקרבת נפש מצד המביא אותו?',
            'a_es': 'Porque suele ser la ofrenda del pobre, quien entrega su sustento vital', 'a_en': 'Because it is usually the offering of the poor person, who gives their vital sustenance', 'a_he': 'כי מנחה היא בדרך כלל קורבנו של העני המקריב את נפשו',
            'b_es': 'Porque la harina es blanca como la pureza del alma', 'b_en': 'Because flour is white like the soul\'s purity', 'b_he': 'כי הסולת לבנה כמו טוהר הנשמה',
            'c_es': 'Porque tiene un sabor dulce a los ojos de Dios', 'c_en': 'Because it has a sweet taste in God\'s eyes', 'c_he': 'כי היא מתוקה ונעימה לה\'',
            'corr': 'a'
        },
        {
            't_es': '¿Qué dos ingredientes estaban estrictamente prohibidos en cualquier ofrenda que se quemara?',
            't_en': 'Which two ingredients were strictly forbidden in any burnt offering?',
            't_he': 'אילו שני מרכיבים נאסרו לחלוטין בהקרבה על המזבח?',
            'a_es': 'Levadura (Seor) y Miel (Devash)', 'a_en': 'Leaven (Seor) and Honey (Devash)', 'a_he': 'שאור ודבש',
            'b_es': 'Aceitunas frescas y uvas', 'b_en': 'Fresh olives and grapes', 'b_he': 'זיתים טריים וענבים',
            'c_es': 'Agua de río y ramas secas', 'c_en': 'River water and dry branches', 'c_he': 'מי נהר וענפים יבשים',
            'corr': 'a'
        },
        {
            't_es': '¿Qué simbolizaba la obligación de poner sal en todas las ofrendas del Tabernáculo?',
            't_en': 'What did the obligation to put salt on all offerings in the Tabernacle symbolize?',
            't_he': 'מה סימל החיוב להקריב מלח על כל קורבן?',
            'a_es': 'El "Pacto de Sal", que es eterno e incorruptible como la Torá', 'a_en': 'The "Covenant of Salt," which is eternal and incorruptible like the Torah', 'a_he': 'ברית מלח עולם, שאינו נפסד לעולם',
            'b_es': 'Simplemente para mejorar el sabor de las carnes', 'b_en': 'Simply to improve the flavor of the meats', 'b_he': 'למתק את טעם הבשר בקורבן',
            'c_es': 'Para evitar que el fuego se apagara', 'c_en': 'To prevent the fire from burning out', 'c_he': 'כדי למנוע מהאש לכבות',
            'corr': 'a'
        },
        {
            't_es': '¿Cuál es la diferencia fundamental entre el sacrificio de "Paz" (Shelamim) y los demás?',
            't_en': 'What is the fundamental difference between the "Peace" (Shelamim) offering and others?',
            't_he': 'מה המאפיין הייחודי של קורבן שלמים לעומת האחרים?',
            'a_es': 'Lo comparten Dios, los sacerdotes y el propio dueño del animal', 'a_en': 'It is shared by God, the priests, and the owner of the animal themselves', 'a_he': 'הוא נאכל בשותפות על ידי המזבח, הכהן והבעלים',
            'b_es': 'Solo se ofrece en tiempos de guerra', 'b_en': 'It is only offered during times of war', 'b_he': 'הוא קרב רק בזמן מלחמה',
            'c_es': 'No requiere derramamiento de sangre', 'c_en': 'It does not require blood shedding', 'c_he': 'אין בו זריקת דמים',
            'corr': 'a'
        },
        {
            't_es': '¿En qué caso se debía traer el sacrificio de "Culpa" (Asham)?',
            't_en': 'In what case was the "Guilt" (Asham) offering brought?',
            't_he': 'באיזה מקרה הובא קורבן "אשם"?',
            'a_es': 'Cuando hubo una duda real sobre si se cometió un pecado o por robo', 'a_en': 'When there was a real doubt about whether a sin was committed or due to robbery', 'a_he': 'במקרים של ספק חטא או גזל ומעילה בקודש',
            'b_es': 'Se traía cada mañana sin motivo aparente', 'b_en': 'It was brought every morning for no apparent reason', 'b_he': 'הוא הובא בכל בוקר ללא סיבה מיוחדת',
            'c_es': 'Solo cuando el Templo estaba en construcción', 'c_en': 'Only when the Temple was under construction', 'c_he': 'הוא הובא רק בזמן בניין המקדש',
            'corr': 'a'
        },
        {
            't_es': '¿Qué parte animal se prohibía comer bajo pena de extinción (Karet) además de la sangre?',
            't_en': 'Which animal part was forbidden to be eaten under the penalty of excision (Karet) besides blood?',
            't_he': 'איזה חלק מהבהמה נאסר באכילה באיסור כרת מלבד הדם?',
            'a_es': 'Ciertas grasas específicas (Jelev)', 'a_en': 'Certain specific fats (Chelev)', 'a_he': 'חלב שעל החלבים (חלקים פנימיים)',
            'b_es': 'Solo el corazón del animal', 'b_en': 'Only the heart of the animal', 'b_he': 'רק את לב החיה',
            'c_es': 'La piel y los huesos', 'c_en': 'The skin and the bones', 'c_he': 'את העור והעצמות',
            'corr': 'a'
        },
        {
            't_es': '¿Cómo se sacrificaban las aves para que se consideraran como una ofrenda sagrada?',
            't_en': 'How were birds sacrificed for them to be considered a sacred offering?',
            't_he': 'כיצד הוקרבו העופות על המזבח?',
            'a_es': 'Mediante la "Meliká" (cortar la nuca con la uña del sacerdote)', 'a_en': 'Through "Melikah" (severing the back of the neck with the priest\'s fingernail)', 'a_he': 'על ידי מליקה בציפורנו של הכהן',
            'b_es': 'Se les dejaba libres en el Santuario', 'b_en': 'They were set free in the Sanctuary', 'b_he': 'הם שולחו לחופשי בתוך המשכן',
            'c_es': 'Se sumergían en aceite caliente primero', 'c_en': 'They were dipped in hot oil first', 'c_he': 'הוקרבו בתוך שמן רותח',
            'corr': 'a'
        },
        {
            't_es': '¿Cuál es el propósito central de los sacrificios según el inicio de Levítico?',
            't_en': 'What is the central purpose of the sacrifices according to the start of Leviticus?',
            't_he': 'מהי המטרה המרכזית של הקורבנות על פי סדר ויקרא?',
            'a_es': 'Acercar al ser humano a la Divinidad (Korbán viene de Karev - Acercar)', 'a_en': 'To draw the human being closer to Divinity (Korban comes from Karev - To draw near)', 'a_he': 'קירוב האדם לקדוש ברוך הוא',
            'b_es': 'Servir de alimento para Dios', 'b_en': 'To serve as food for God', 'b_he': 'לשמש "אוכל" כביכול לה\'',
            'c_es': 'Simplemente mantener el orden social', 'c_en': 'Simply to maintain social order', 'c_he': 'לשמור על סדר חברתי בלבד',
            'corr': 'a'
        }
    ])

    db.session.commit()
