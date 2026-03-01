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
    # VAYAKHEL (Nivel Medio-Alto)
    add_q('Vayakhel', [
        {
            't_es': '¿Por qué la prohibición de encender fuego en Shabat se menciona explícitamente en esta Parashá?',
            't_en': 'Why is the prohibition of lighting fire on Shabbat explicitly mentioned in this Parasha?',
            't_he': 'מדוע האיסור על הבערת אש בשבת מוזכר במפורש בפרשה זו?',
            'a_es': 'Para enseñar que ni siquiera por la construcción del Tabernáculo se debe profanar el Shabat', 'a_en': 'To teach that even for the construction of the Tabernacle, Shabbat should not be desecrated', 'a_he': 'ללמד שאפילו עבור בניית המשכן אסור לחלל שבת',
            'b_es': 'Como recordatorio del fuego destructivo del Becerro de Oro', 'b_en': 'As a reminder of the destructive fire of the Golden Calf', 'b_he': 'כתזכורת לאש המשחיתה של חטא העגל',
            'c_es': 'Solo se prohibía encender fuego dentro del Santuario', 'c_en': 'Fire was only forbidden within the Sanctuary', 'c_he': 'היה אסור להבעיר אש רק בתוך המקדש',
            'corr': 'a'
        },
        {
            't_es': '¿Cuál fue la respuesta del pueblo hebreo al pedido de materiales para el Tabernáculo?',
            't_en': 'What was the response of the Hebrew people to the request for materials for the Tabernacle?',
            't_he': 'מה הייתה תגובת העם לבקשת המלצאים לבניית המשכן?',
            'a_es': 'Trajeron tanto que Moisés tuvo que ordenarles que se detuvieran', 'a_en': 'They brought so much that Moses had to command them to stop', 'a_he': 'הביאו כל כך הרבה עד שמשה נאלץ לצוות עליהם להפסיק',
            'b_es': 'Hubo que imponer un impuesto obligatorio para completar la obra', 'b_en': 'A mandatory tax had to be imposed to complete the work', 'b_he': 'היה צורך להטיל מס חובה כדי להשלים את המלאכה',
            'c_es': 'Solo los príncipes de las tribus contribuyeron', 'c_en': 'Only the princes of the tribes contributed', 'c_he': 'רק נשיאי השבטים תרמו',
            'corr': 'a'
        },
        {
            't_es': '¿Qué distinción especial tuvieron las mujeres en la contribución al Tabernáculo?',
            't_en': 'What special distinction did women have in contributing to the Tabernacle?',
            't_he': 'מה היה הייחוד של הנשים בתרומתן למשכן?',
            'a_es': 'Hilaron el pelo de cabra mientras aún estaba sobre el animal vivo', 'a_en': 'They spun the goat hair while it was still on the living animal', 'a_he': 'טוו את העיזים כשהן מחוברין לחיים',
            'b_es': 'Trajeron solo joyas de oro de Egipto', 'b_en': 'They brought only gold jewelry from Egypt', 'b_he': 'הביאו רק תכשיטי זהב ממצרים',
            'c_es': 'Construyeron las cortinas exteriores solas', 'c_en': 'They built the outer curtains alone', 'c_he': 'הקימו את היריעות החיצוניות לבדן',
            'corr': 'a'
        },
        {
            't_es': '¿Qué simbolizaban las dos tribus de los artesanos principales (Judá y Dan)?',
            't_en': 'What did the two tribes of the main artisans (Judah and Dan) symbolize?',
            't_he': 'מה סימלו שני השבטים של האומנים הראשיים (יהודה ודן)?',
            'a_es': 'La unión entre la tribu más noble y la más humilde en la obra divina', 'a_en': 'The union between the most noble and the most humble tribe in the divine work', 'a_he': 'איחוד בין השבט המפואר ביותר לשפל ביותר במלאכת השמים',
            'b_es': 'Las dos fronteras de la Tierra de Israel', 'b_en': 'The two borders of the Land of Israel', 'b_he': 'שני הגבולות של ארץ ישראל',
            'c_es': 'Los dos tipos de incienso permitidos', 'c_en': 'The two types of permitted incense', 'c_he': 'שני סוגי הקטורת המותרים',
            'corr': 'a'
        },
        {
            't_es': '¿De qué material se hizo el Lavamanos (Kior) y por qué era simbólico?',
            't_en': 'From what material was the Washbasin (Kior) made and why was it symbolic?',
            't_he': 'מאיזה חומר נעשה הכיור ומדוע היה סמלי?',
            'a_es': 'De los espejos de bronce de las mujeres que fomentaron la vida en Egipto', 'a_en': 'From the bronze mirrors of the women who fueled life in Egypt', 'a_he': 'ממראות הנשים הצובאות שקיימו את הדורות במצרים',
            'b_es': 'De plata fundida de los idolos egipcios', 'b_en': 'From silver melted from Egyptian idols', 'b_he': 'מכסף שהותך מפסלים מצריים',
            'c_es': 'De oro puro para reflejar la pureza del alma', 'c_en': 'From pure gold to reflect the purity of the soul', 'c_he': 'מזהב טהור כסמל לטוהר הנשמה',
            'corr': 'a'
        },
        {
            't_es': '¿Cómo se unían las cubiertas exteriores del Tabernáculo?',
            't_en': 'How were the outer covers of the Tabernacle joined?',
            't_he': 'כיצד חוברו היריעות החיצוניות של המשכן?',
            'a_es': 'Mediante lazos y ganchos de oro y bronce', 'a_en': 'Through loops and hooks of gold and bronze', 'a_he': 'על ידי לולאות וקרסים מזהב ומנחושת',
            'b_es': 'Cosidas con hilos de seda invisibles', 'b_en': 'Sewn with invisible silk threads', 'b_he': 'תפורות בחוטי משי בלתי נראים',
            'c_es': 'Simplemente se apoyaban unas sobre otras', 'c_en': 'They just rested on top of each other', 'c_he': 'הן פשוט הונחו אחת על השנייה',
            'corr': 'a'
        },
        {
            't_es': '¿Qué objeto del Tabernáculo contenía únicamente las Tablas del Pacto?',
            't_en': 'What object of the Tabernacle contained only the Tablets of the Covenant?',
            't_he': 'איזה כלי במשכן הכיל רק את לוחות הברית?',
            'a_es': 'El Arca Sagrada (Arón)', 'a_en': 'The Holy Ark (Aron)', 'a_he': 'ארון הקודש',
            'b_es': 'La Mesa (Shulján)', 'b_en': 'The Table (Shulchan)', 'b_he': 'השולחן',
            'c_es': 'El Altar Interior', 'c_en': 'The Inner Altar', 'c_he': 'המזבח הפנימי',
            'corr': 'a'
        },
        {
            't_es': '¿De qué estaba compuesto el techo del Tabernáculo según Vayakhel?',
            't_en': 'What was the Tabernacle\'s roof composed of according to Vayakhel?',
            't_he': 'מה הרכיב את גג המשכן על פי פרשת ויקהל?',
            'a_es': 'Capas de lana, pelo de cabra y pieles de animales teñidas', 'a_en': 'Layers of wool, goat hair, and dyed animal skins', 'a_he': 'יריעות שש, עיזים ועורות אילים ותחשים',
            'b_es': 'Placas de metal ligero', 'b_en': 'Lightweight metal plates', 'b_he': 'לוחות מתכת קלים',
            'c_es': 'Ramas de palma y cedro', 'c_en': 'Palm and cedar branches', 'c_he': 'ענפי תמר וארז',
            'corr': 'a'
        },
        {
            't_es': '¿Qué función cumplían las barras (Brijim) en la estructura del Mishkán?',
            't_en': 'What function did the bars (Brijim) serve in the Mishkan\'s structure?',
            't_he': 'איזה תפקיד מילאו הבריחים במבנה המשכן?',
            'a_es': 'Sujetaban los tablones laterales para formar una pared sólida', 'a_en': 'They held the side planks together to form a solid wall', 'a_he': 'חיזקו את הקרשים ליצירת קיר יציב',
            'b_es': 'Se usaban para colgar las vestiduras', 'b_en': 'They were used to hang the garments', 'b_he': 'שימשו לתליית הבגדים',
            'c_es': 'Eran los escalones para subir a la Menorá', 'c_en': 'They were the steps to reach the Menorah', 'c_he': 'שימשו כמדרגות למנורה',
            'corr': 'a'
        },
        {
            't_es': '¿Quién fue el ayudante principal de Bezalel enviado por Dios?',
            't_en': 'Who was the chief assistant of Bezalel sent by God?',
            't_he': 'מי היה עוזרו הראשי של בצלאל עליו הודיע ה\'?',
            'a_es': 'Oholiav ben Ajisamaj de la tribu de Dan', 'a_en': 'Oholiab son of Ahisamach of the tribe of Dan', 'a_he': 'אהליאב בן אחיסמך למטה דן',
            'b_es': 'Josué de la tribu de Efraín', 'b_en': 'Joshua of the tribe of Ephraim', 'b_he': 'יהושע בן נון',
            'c_es': 'Eleazar el sacerdote', 'c_en': 'Eleazar the priest', 'c_he': 'אלעזר הכהן',
            'corr': 'a'
        }
    ])

    # PEKUDE (Nivel Medio-Alto)
    add_q('Pekudé', [
        {
            't_es': '¿Con qué propósito inició Moisés el recuento detallado de los materiales?',
            't_en': 'For what purpose did Moses initiate the detailed accounting of the materials?',
            't_he': 'לשם מה ערך משה את פירוט החשבון של חומרי המשכן?',
            'a_es': 'Para demostrar transparencia absoluta ante las sospechas de los criticones', 'a_en': 'To demonstrate absolute transparency against the suspicions of critics', 'a_he': 'להראות שקיפות מלאה מול "ליצני הדור"',
            'b_es': 'Porque las leyes de Egipto lo exigían', 'b_en': 'Because the laws of Egypt required it', 'b_he': 'כי כך דרשו חוקי מצרים',
            'c_es': 'Para vender los materiales sobrantes', 'c_en': 'To sell the excess materials', 'c_he': 'כדי למכור את המשאירים',
            'corr': 'a'
        },
        {
            't_es': '¿Qué asombroso milagro ocurrió con la plata del censo según el recuento de Pekudé?',
            't_en': 'What amazing miracle occurred with the census silver according to the Pekude accounting?',
            't_he': 'איזה דיוק מופלא התגלה בחשבון הכסף במפקד בפרשת פקודי?',
            'a_es': 'La cantidad de plata coincidió exactamente con el número de personas censadas', 'a_en': 'The amount of silver exactly matched the number of people counted', 'a_he': 'כמות הכסף התאימה בדיוק למספר המשתתפים במפקד',
            'b_es': 'La plata se multiplicó milagrosamente por diez', 'b_en': 'The silver miraculously multiplied by ten', 'b_he': 'הכסף הכפיל את עצמו עשרת מונים בדרך נס',
            'c_es': 'La plata se convirtió en oro puro', 'c_en': 'The silver turned into pure gold', 'c_he': 'הכסף הפך לזהב טהור',
            'corr': 'a'
        },
        {
            't_es': '¿Cuántos "Adanim" (Basas) se fabricaron de plata para el Tabernáculo?',
            't_en': 'How many "Adanim" (Sockets) were made of silver for the Tabernacle?',
            't_he': 'כמה "אדנים" נעשו מכסף עבור המשכן?',
            'a_es': 'Exactamente 100 basas', 'a_en': 'Exactly 100 sockets', 'a_he': 'מאה אדנים בדיוק',
            'b_es': '70 basas, una por cada nación', 'b_en': '70 sockets, one for each nation', 'b_he': '70 אדנים, אחד לכל אומה',
            'c_es': '12 basas, una por cada tribu', 'c_en': '12 sockets, one for each tribe', 'c_he': '12 אדנים, אחד לכל שבט',
            'corr': 'a'
        },
        {
            't_es': '¿Qué frase se repite constantemente al final de la construcción en Pekudé?',
            't_en': 'What phrase is constantly repeated at the end of the construction in Pekude?',
            't_he': 'איזה משפט חוזר על עצמו שוב ושוב בסיום המלאכה?',
            'a_es': '"Como el Eterno había ordenado a Moisés"', 'a_en': '"As the Eternal had commanded Moses"', 'a_he': '"כאשר ציווה ה\' את משה"',
            'b_es': '"Y el pueblo se alegró mucho"', 'b_en': '"And the people rejoiced greatly"', 'b_he': '"וישמח העם שמחה גדולה"',
            'c_es': '"Que sea hecha con sabiduría"', 'c_en': '"May it be done with wisdom"', 'c_he': '"שתעשה בחוכמה"',
            'corr': 'a'
        },
        {
            't_es': '¿Qué señal visible indicó que Dios aceptó la morada del Tabernáculo?',
            't_en': 'What visible sign indicated that God accepted the Tabernacle\'s dwelling?',
            't_he': 'איזה אות גלוי הראה שהשכינה שרתה במשכן?',
            'a_es': 'La nube cubrió el Tienda del Encuentro y la gloria de Dios llenó el lugar', 'a_en': 'The cloud covered the Tent of Meeting and God\'s glory filled the place', 'a_he': 'הענן כיסה את אוהל מועד וכבוד ה\' מילא את המשכן',
            'b_es': 'Un relámpago cayó del cielo sin lluvia', 'b_en': 'Lightning fell from the sky without rain', 'b_he': 'ברק ירד מהשמים ללא גשם',
            'c_es': 'Todas las lámparas se encendieron solas', 'c_en': 'All the lamps lit themselves', 'c_he': 'כל המנורות נדלקו מאליהן',
            'corr': 'a'
        },
        {
            't_es': '¿Por qué Moisés no pudo entrar en la Tienda del Encuentro inicialmente?',
            't_en': 'Why was Moses unable to enter the Tent of Meeting initially?',
            't_he': 'מדוע לא יכול היה משה להיכנס אל אוהל מועד בתחילה?',
            'a_es': 'Porque la nube posaba sobre él y la Gloria de Dios era demasiado intensa', 'a_en': 'Because the cloud rested upon it and God\'s Glory was too intense', 'a_he': 'כי שכן עליו הענן וכבוד ה\' לא אפשר זאת',
            'b_es': 'Porque Dios se lo prohibió como castigo', 'b_en': 'Because God forbade him as punishment', 'b_he': 'כי ה\' אסר עליו זאת כעונש',
            'c_es': 'Había olvidado la llave del Santuario', 'c_en': 'He had forgotten the key to the Sanctuary', 'c_he': 'הוא שכח את המפתח למקדש',
            'corr': 'a'
        },
        {
            't_es': '¿Qué función cumplían las vestiduras de Aharón en relación con el pueblo?',
            't_en': 'What function did Aaron\'s garments serve in relation to the people?',
            't_he': 'איזה תפקיד מילאו בגדי אהרון כלפי העם?',
            'a_es': 'Llevaba sus nombres sobre su corazón y hombros para recordarlos ante Dios', 'a_en': 'He bore their names on his heart and shoulders to remember them before God', 'a_he': 'נשא את שמותיהם על ליבו ועל כתפיו לזיכרון לפני ה\'',
            'b_es': 'Eran simplemente uniformes de trabajo', 'b_en': 'They were simply work uniforms', 'b_he': 'הם היו מדי עבודה בלבד',
            'c_es': 'Para identificar quién era el más rico', 'c_en': 'To identify who was the wealthiest', 'c_he': 'כדי לזהות מי העשיר ביותר',
            'corr': 'a'
        },
        {
            't_es': '¿Qué sucedió con los excedentes de materiales al finalizar Pekudé?',
            't_en': 'What happened to the surplus materials at the end of Pekude?',
            't_he': 'מה קרה עם שאריות המלצאים בסיום המלאכה?',
            'a_es': 'Moisés hizo un informe final y se usaron para reparaciones futuras', 'a_en': 'Moses made a final report and they were used for future repairs', 'a_he': 'משה ערך דו"ח סופי והם הוקדשו לתחזוקה',
            'b_es': 'Se devolvieron a cada donante', 'b_en': 'They were returned to each donor', 'b_he': 'הם הוחזרו לכל תורם',
            'c_es': 'Fueron quemados para que nadie los usara', 'c_en': 'They were burned so no one would use them', 'c_he': 'הם נשרפו כדי שאיש לא ישתמש בהם',
            'corr': 'a'
        },
        {
            't_es': '¿En qué fecha exacta se completó la erección definitiva del Tabernáculo?',
            't_en': 'On what exact date was the final erection of the Tabernacle completed?',
            't_he': 'באיזה תאריך הוקם המשכן סופית?',
            'a_es': 'El primer día del primer mes (1 de Nisán)', 'a_en': 'The first day of the first month (1st of Nissan)', 'a_he': 'ביום הראשון לחודש הראשון (א\' ניסן)',
            'b_es': 'En Shavuot, tras recibir la Torá', 'b_en': 'On Shavuot, after receiving the Torah', 'b_he': 'בחג השבועות לאחר מתן תורה',
            'c_es': 'Exactamente un año después de salir de Egipto', 'c_en': 'Exactly one year after leaving Egypt', 'c_he': 'בדיוק שנה לאחר היציאה ממצרים',
            'corr': 'a'
        },
        {
            't_es': '¿Qué nombre recibe el fenómeno de la nube subiendo y bajando sobre el Mishkán?',
            't_en': 'What is the phenomenon of the cloud rising and setting over the Mishkan called?',
            't_he': 'איך נקרא המסע המונחה על ידי הענן ששכן על המשכן?',
            'a_es': 'El orden de los viajes de los hijos de Israel', 'a_en': 'The order of the journeys of the children of Israel', 'a_he': 'סדר מסעות בני ישראל',
            'b_es': 'El ciclo de las estaciones terrestres', 'b_en': 'The cycle of the Earth\'s seasons', 'b_he': 'מחזור עונות השנה',
            'c_es': 'El clima milagroso del desierto', 'c_en': 'The miraculous desert weather', 'c_he': 'מזג האוויר הניסי במדבר',
            'corr': 'a'
        }
    ])

    db.session.commit()
