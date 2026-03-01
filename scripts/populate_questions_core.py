import sys
import os
sys.path.append(os.getcwd())
from app import create_app, db
from app.models import Parasha, Question

def add_q(p_name, qs):
    p = Parasha.query.filter_by(name_es=p_name).first()
    if not p:
        print(f"Parasha {p_name} not found.")
        return
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
    db.session.commit()
    print(f"Added {len(qs)} complex questions to {p_name}")

app = create_app()
with app.app_context():
    # TETZAVE (Nivel Medio-Alto)
    add_q('Tetzavé', [
        {
            't_es': '¿Por qué Moisés no es mencionado por su nombre en toda la Parashá Tetzavé?',
            't_en': 'Why is Moses not mentioned by name throughout Parashat Tetzave?',
            't_he': 'מדוע שמו של משה רבנו לא מוזכר בכל פרשת תצוה?',
            'a_es': 'Por su petición: "Bórrame de Tu libro"', 'a_en': 'Due to his request: "Erase me from Your book"', 'a_he': 'בגלל בקשתו: "מחני נא מספרך אשר כתבת"',
            'b_es': 'Porque el enfoque es exclusivamente en Aharón', 'b_en': 'Because the focus is exclusively on Aaron', 'b_he': 'כי המיקוד הוא בלעדית באהרון',
            'c_es': 'Como castigo por dudar en la zarza ardiente', 'c_en': 'As punishment for hesitating at the burning bush', 'c_he': 'כעונש על סירובו בסנה הבוער',
            'corr': 'a'
        },
        {
            't_es': '¿Qué función particular cumplían las "Campanillas de Oro" según el texto bíblico?',
            't_en': 'What specific function did the "Golden Bells" serve according to the biblical text?',
            't_he': 'איזו מטרה מוגדרת שירתו פעמוני הזהב על פי הפסוקים?',
            'a_es': 'Para que se oyera su sonido al entrar al Santuario y no muriera', 'a_en': 'So his sound would be heard when entering the Sanctuary, lest he die', 'a_he': 'ונשמע קולו בבואו אל הקודש... ולא ימות',
            'b_es': 'Para espantar las energías espirituales negativas', 'b_en': 'To ward off negative spiritual energies', 'b_he': 'כדי לגרש אנרגיות רוחניות שליליות',
            'c_es': 'Como símbolo de la música celestial', 'c_en': 'As a symbol of celestial music', 'c_he': 'כסמל למוזיקה שמימית',
            'corr': 'a'
        },
        {
            't_es': '¿Qué grabados únicos llevaban las piedras de Ónix en las hombreras del Efod?',
            't_en': 'What unique engravings did the Onyx stones on the Ephod\'s shoulder straps bear?',
            't_he': 'אילו פיתוחים מיוחדים היו על אבני השוהם בכתפות האפוד?',
            'a_es': 'Los nombres de las tribus por orden de nacimiento', 'a_en': 'The names of the tribes in order of their birth', 'a_he': 'שמות השבטים כתולדותם',
            'b_es': 'Los nombres de los tres Patriarcas', 'b_en': 'The names of the three Patriarchs', 'b_he': 'שמות שלושת האבות',
            'c_es': 'Las 13 atributos de misericordia', 'c_en': 'The 13 attributes of mercy', 'c_he': 'י"ג מידות הרחמים',
            'corr': 'a'
        },
        {
            't_es': '¿Cuál es la diferencia entre el incienso (Ketoret) y los sacrificios animales en cuanto a su ubicación?',
            't_en': 'What is the difference between the incense (Ketoret) and animal sacrifices regarding their location?',
            't_he': 'מה ההבדל בין הקטרת הקטורת לקורבן הבהמה מבחינת מיקום המזבח?',
            'a_es': 'El incienso se ofrecía en el Altar de Oro (Interior)', 'a_en': 'The incense was offered on the Golden Altar (Inner)', 'a_he': 'הקטורת הוקטרה על מזבח הזהב (הפנימי)',
            'b_es': 'Ambos se ofrecían en el patio exterior', 'b_en': 'Both were offered in the outer courtyard', 'b_he': 'שניהם הוקטרו בחצר החיצונית',
            'c_es': 'El incienso solo se ofrecía fuera del Tabernáculo', 'c_en': 'Incense was only offered outside the Tabernacle', 'c_he': 'הקטורת הוקטרה רק מחוץ למשכן',
            'corr': 'a'
        },
        {
            't_es': '¿Qué representaba el "Tzitz" (Lmina de oro) sobre la frente del Cohen Gadol?',
            't_en': 'What did the "Tzitz" (Golden Plate) represent on the High Priest\'s forehead?',
            't_he': 'מה סימל הציץ על מצחו של הכהן הגדול?',
            'a_es': 'Expiación por la desfachatez y pecados del pensamiento', 'a_en': 'Atonement for arrogance and sins of thought', 'a_he': 'כפרה על עזות מצח וחטאי המחשבה',
            'b_es': 'Simplemente un adorno real', 'b_en': 'Simply a royal ornament', 'b_he': 'קישוט מלכותי בלבד',
            'c_es': 'La corona de la sabiduría humana', 'c_en': 'The crown of human wisdom', 'c_he': 'כתר החוכמה האנושית',
            'corr': 'a'
        },
        {
            't_es': '¿Cómo se describe la unión de las piedras en el Joshen (Pectoral)?',
            't_en': 'How is the setting of the stones in the Choshen (Breastplate) described?',
            't_he': 'כיצד מתוארת קביעת האבנים בחושן?',
            'a_es': 'Engastadas en marcos de oro (Mishbetzot)', 'a_en': 'Set in gold frames (Mishbetzot)', 'a_he': 'משובצים משבצות זהב',
            'b_es': 'Pegadas con resina especial', 'b_en': 'Glued with special resin', 'b_he': 'מודבקות בשרף מיוחד',
            'c_es': 'Atadas con hilos de seda purpúrea', 'c_en': 'Tied with purple silk threads', 'c_he': 'קשורות בחוטי משי ארגמן',
            'corr': 'a'
        },
        {
            't_es': '¿Qué simbolizaba la "Menorá" encendida continuamente (Ner Tamid)?',
            't_en': 'What did the continuously lit "Menorah" (Ner Tamid) symbolize?',
            't_he': 'מה סימלה המנורה הדולקת תמיד (נר תמיד)?',
            'a_es': 'Testimonio de que la Presencia Divina mora en Israel', 'a_en': 'Testimony that the Divine Presence dwells in Israel', 'a_he': 'עדות שהשכינה שורה בישראל',
            'b_es': 'Una fuente de luz física para el Santuario', 'b_en': 'A physical light source for the Sanctuary', 'b_he': 'מקור אור פיזי למקדש',
            'c_es': 'El sol y los planetas', 'c_en': 'The sun and the planets', 'c_he': 'השמש והפלנטות',
            'corr': 'a'
        },
        {
            't_es': '¿En qué consistía la "Miluim" (Consagración) mencionada en la Parashá?',
            't_en': 'What did the "Miluim" (Consecration) mentioned in the Parasha consist of?',
            't_he': 'מה כללו ימי המילואים המוזכרים בפרשה?',
            'a_es': 'Siete días de ofrendas y permanencia en el Santuario', 'a_en': 'Seven days of offerings and staying in the Sanctuary', 'a_he': 'שבעת ימי חניכת הכהנים והמשכן',
            'b_es': 'Un censo de los sacerdotes', 'b_en': 'A census of the priests', 'b_he': 'מפקד של הכהנים',
            'c_es': 'La construcción de las paredes del Tabernáculo', 'c_en': 'The construction of the Tabernacle walls', 'c_he': 'בניית קירות המשכן',
            'corr': 'a'
        },
        {
            't_es': '¿De dónde se obtenía el tinte "Tejelet" para las vestiduras?',
            't_en': 'From where was the "Techelet" dye for the garments obtained?',
            't_he': 'מנין הופק צבע התכלת לבגדי הכהונה?',
            'a_es': 'Del caracol marino conocido como Jilazón', 'a_en': 'From the sea snail known as Chilazon', 'a_he': 'מחילזון ימי',
            'b_es': 'De una planta del desierto', 'b_en': 'From a desert plant', 'b_he': 'מצמח מדברי',
            'c_es': 'De minerales volcánicos', 'c_en': 'From volcanic minerals', 'c_he': 'ממינרלים וולקניים',
            'corr': 'a'
        },
        {
            't_es': '¿Qué relación tiene el Altar de Incienso con la purificación del Sumo Sacerdote?',
            't_en': 'How is the Incense Altar related to the High Priest\'s purification?',
            't_he': 'מה הקשר בין מזבח הקטורת לטהרת הכהן הגדול?',
            'a_es': 'Se ponía sangre sobre sus cuernos una vez al año (Yom Kippur)', 'a_en': 'Blood was placed on its horns once a year (Yom Kippur)', 'a_he': 'נתינת דם על קרנותיו פעם בשנה ביום הכיפורים',
            'b_es': 'No tiene relación con la sangre', 'b_en': 'It has no relation to blood', 'b_he': 'אין לו קשר לדם',
            'c_es': 'Debía lavarse allí las manos', 'c_en': 'He had to wash his hands there', 'c_he': 'היה צריך לרחוץ שם את ידיו',
            'corr': 'a'
        }
    ])

    # Kİ TİSA (Nivel Medio-Alto)
    add_q('Ki Tisá', [
        {
            't_es': '¿Por qué se exigía precisamente "medio" shekel y no uno entero?',
            't_en': 'Why was exactly "half" a shekel required instead of a whole one?',
            't_he': 'מדוע נדרשה דווקא "מחצית" השקל ולא שקל שלם?',
            'a_es': 'Para indicar que cada judío es incompleto sin el otro', 'a_en': 'To indicate that every Jew is incomplete without the other', 'a_he': 'לרמוז שכל יהודי אינו שלם ללא חברו',
            'b_es': 'Porque la plata era muy escasa en el desierto', 'b_en': 'Because silver was very scarce in the desert', 'b_he': 'כי הכסף היה נדיר מאוד במדבר',
            'c_es': 'Era el impuesto estándar de Egipto', 'c_en': 'It was the standard Egyptian tax', 'c_he': 'זה היה המס הסטנדרטי במצרים',
            'corr': 'a'
        },
        {
            't_es': '¿Qué componente del Incienso (Ketoret) simbolizaba a los pecadores de Israel?',
            't_en': 'Which component of the Incense (Ketoret) symbolized the sinners of Israel?',
            't_he': 'איזה רכיב בקטורת סימל את פושעי ישראל?',
            'a_es': 'La Jelbená (Gálbano), de olor desagradable por sí sola', 'a_en': 'Chelbenah (Galbanum), which has an unpleasant smell on its own', 'a_he': 'החלבנה, שריחה רע כשהיא לעצמה',
            'b_es': 'El incienso puro', 'b_en': 'Pure frankincense', 'b_he': 'הלבונה הזכה',
            'c_es': 'La canela', 'c_en': 'The cinnamon', 'c_he': 'הקינמון',
            'corr': 'a'
        },
        {
            't_es': '¿Cuál fue el razonamiento erróneo del pueblo para crear el Becerro de Oro?',
            't_en': 'What was the people\'s erroneous reasoning for creating the Golden Calf?',
            't_he': 'מה היה החישוב המוטעה של העם שהוביל לחטא העגל?',
            'a_es': 'Pensaron que Moisés había muerto al pasar 6 horas de retraso', 'a_en': 'They thought Moses had died because he was 6 hours late', 'a_he': 'חשבו שמשה מת לאחר איחור של שש שעות',
            'b_es': 'Querían volver a la cultura de Egipto', 'b_en': 'They wanted to return to Egyptian culture', 'b_he': 'רצו לחזור לתרבות מצרים',
            'c_es': 'Dios se los ordenó en un sueño', 'c_en': 'God commanded them in a dream', 'c_he': 'ה\' ציווה אותם בחלום',
            'corr': 'a'
        },
        {
            't_es': '¿Qué atributo de Dios reveló Él a Moisés después del pecado del becerro?',
            't_en': 'What attribute of God did He reveal to Moses after the sin of the calf?',
            't_he': 'איזו מידה של ה\' נחשפה למשה לאחר חטא העגל?',
            'a_es': 'Los 13 Atributos de Misericordia', 'a_en': 'The 13 Attributes of Mercy', 'a_he': 'י"ג מידות הרחמים',
            'b_es': 'El atributo de Justicia estricta', 'b_en': 'The attribute of strict Justice', 'b_he': 'מידת הדין',
            'c_es': 'La omnipotencia creadora', 'c_en': 'Creative omnipotence', 'c_he': 'הכל-יכולת הבוראת',
            'corr': 'a'
        },
        {
            't_es': '¿Qué nombre recibe el día en que Moisés bajó con las segundas tablas, marcando el perdón?',
            't_en': 'What is the name of the day Moses descended with the second tablets, marking forgiveness?',
            't_he': 'מהו היום בו ירד משה עם הלוחות השניים, יום המחילה?',
            'a_es': 'Yom Kippur', 'a_en': 'Yom Kippur', 'a_he': 'יום הכיפורים',
            'b_es': 'Rosh Hashaná', 'b_en': 'Rosh Hashanah', 'b_he': 'ראש השנה',
            'c_es': 'Shavuot', 'c_en': 'Shavuot', 'c_he': 'שבועות',
            'corr': 'a'
        },
        {
            't_es': '¿Bajo qué condición aceptó Dios seguir acompañando al pueblo en su viaje?',
            't_en': 'Under what condition did God agree to continue accompanying the people on their journey?',
            't_he': 'תחת איזה תנאי הסכים ה\' להמשיך ללוות את העם במסעם?',
            'a_es': 'Tras la intensa intercesión y rezos de Moisés', 'a_en': 'Following the intense intercession and prayers of Moses', 'a_he': 'לאחר תחינותיו ותפילותיו העזות של משה',
            'b_es': 'Si entregaban todo su oro', 'b_en': 'If they gave up all their gold', 'b_he': 'אם ימסרו את כל הזהב שלהם',
            'c_es': 'Si castigaban a Aharón', 'c_en': 'If they punished Aaron', 'c_he': 'אם יענישו את אהרון',
            'corr': 'a'
        },
        {
            't_es': '¿Qué simbolizaba la Fuente de Bronce (Kior) hecha de los espejos de las mujeres?',
            't_en': 'What did the Bronze Washbasin (Kior) made from the women\'s mirrors symbolize?',
            't_he': 'מה סימל הכיור שנעשה ממראות הנשים הצובאות?',
            'a_es': 'La santidad de la familia y el deseo de continuidad en Egipto', 'a_en': 'The holiness of family and the desire for continuity in Egypt', 'a_he': 'קדושת המשפחה והרצון להמשכיות במצרים',
            'b_es': 'La vanidad humana que debe ser lavada', 'b_en': 'Human vanity that must be washed away', 'b_he': 'היהירות האנושית שיש לרחוץ אותה',
            'c_es': 'La luz del sol reflejada', 'c_en': 'Reflected sunlight', 'c_he': 'אור השמש המשתקף',
            'corr': 'a'
        },
        {
            't_es': '¿Qué le prohibió Dios ver a Moisés cuando pasó ante él?',
            't_en': 'What did God forbid Moses from seeing when He passed before him?',
            't_he': 'מה אסר ה\' על משה לראות כשעבר על פניו?',
            'a_es': 'Su rostro (Panim)', 'a_en': 'His face (Panim)', 'a_he': 'את פניו',
            'b_es': 'Su espalda (Ajor)', 'b_en': 'His back (Achor)', 'b_he': 'את אחוריו',
            'c_es': 'Sus manos', 'c_en': 'His hands', 'c_he': 'את ידיו',
            'corr': 'a'
        },
        {
            't_es': '¿Qué hizo Moisés con el Becerro de Oro después de destruirlo?',
            't_en': 'What did Moses do with the Golden Calf after destroying it?',
            't_he': 'מה עשה משה לעגל הזהב לאחר שהשמידו?',
            'a_es': 'Lo molió hasta hacerlo polvo y lo dio a beber al pueblo', 'a_en': 'Ground it into powder and made the people drink it', 'a_he': 'טחן אותו לעפר והשקה בו את בני ישראל',
            'b_es': 'Lo enterró bajo el monte', 'b_en': 'Buried it under the mountain', 'b_he': 'קבר אותו תחת ההר',
            'c_es': 'Lo envió de vuelta a Egipto', 'c_en': 'Sent it back to Egypt', 'c_he': 'שלח אותו חזרה למצרים',
            'corr': 'a'
        },
        {
            't_es': '¿Por qué Moisés tuvo que usar un velo (Masvé) después de bajar del monte?',
            't_en': 'Why did Moses have to wear a veil (Masveh) after coming down from the mountain?',
            't_he': 'מדוע נאלץ משה לשים מסווה על פניו?',
            'a_es': 'Porque su rostro irradiaba una luz divina insoportable para el pueblo', 'a_en': 'Because his face radiated a divine light unbearable for the people', 'a_he': 'כי קרן עור פניו והעם יראו מגשת אליו',
            'b_es': 'Para protegerse del polvo del desierto', 'b_en': 'To protect himself from desert dust', 'b_he': 'כדי להגן על עצמו מאבק המדבר',
            'c_es': 'Como señal de duelo por el becerro', 'c_en': 'As a sign of mourning for the calf', 'c_he': 'כסימן אבל על העגל',
            'corr': 'a'
        }
    ])
