from app import create_app, db
from app.models import Parasha, Question

def add_questions(n_es, qs):
    p = Parasha.query.filter_by(name_es=n_es).first()
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
    print(f"Added {len(qs)} to {n_es}")

app = create_app()
with app.app_context():
    # SHEMINI
    add_questions('Sheminí', [
        {'text_es': '¿Hijos de Aharón que murieron?', 'text_en': 'Aaron\'s sons who died?', 'text_he': 'בני אהרן שמתו?', 'a_es': 'Nadav y Abiú', 'a_en': 'Nadav & Avihu', 'a_he': 'נדב ואביהוא', 'b_es': 'Eleazar e Itamar', 'b_en': 'Eleazar & Itamar', 'b_he': 'אלעזר ואיתמר', 'c_es': 'Gershon y Merari', 'c_en': 'Gershon & Merari', 'c_he': 'גרשון ומררי', 'correct': 'a'},
        {'text_es': '¿Causa de muerte?', 'text_en': 'Cause of death?', 'text_he': 'סיבת המוות?', 'a_es': 'Fuego extraño', 'a_en': 'Strange fire', 'a_he': 'אש זרה', 'b_es': 'Diluvio', 'b_en': 'Flood', 'b_he': 'מבול', 'c_es': 'Guerra', 'c_en': 'War', 'c_he': 'מלחמה', 'correct': 'a'},
        {'text_es': '¿Animales terrestres kosher?', 'text_en': 'Kosher land animals?', 'text_he': 'חיות כשרות?', 'a_es': 'Pezuña partida y rumian', 'a_en': 'Split hoof & chew cud', 'a_he': 'מפריס פרסה ומעלה גרה', 'b_es': 'Solo pezuña', 'b_en': 'Hoof only', 'b_he': 'רק פרסה', 'c_es': 'Rapaces', 'c_en': 'Predators', 'c_he': 'טורפים', 'correct': 'a'},
        {'text_es': '¿Cerdo es kosher?', 'text_en': 'Pig is kosher?', 'text_he': 'חזיר כשר?', 'a_es': 'No', 'a_en': 'No', 'a_he': 'לא', 'b_es': 'Sí', 'b_en': 'Yes', 'b_he': 'כן', 'c_es': 'Solo en Shabat', 'c_en': 'Only on Shabbat', 'c_he': 'רק בשבת', 'correct': 'a'},
        {'text_es': '¿Peces kosher?', 'text_en': 'Kosher fish?', 'text_he': 'דגים כשרים?', 'a_es': 'Aletas y escamas', 'a_en': 'Fins & scales', 'a_he': 'סנפיר וקשקשת', 'b_es': 'Solo aletas', 'b_en': 'Fins only', 'b_he': 'רק סנפיר', 'c_es': 'Cualquiera', 'c_en': 'Any', 'c_he': 'הכל', 'correct': 'a'},
        {'text_es': '¿Camello es kosher?', 'text_en': 'Camel is kosher?', 'text_he': 'גמל כשר?', 'a_es': 'No', 'a_en': 'No', 'a_he': 'לא', 'b_es': 'Sí', 'b_en': 'Yes', 'b_he': 'כן', 'c_es': 'A veces', 'c_en': 'Sometimes', 'c_he': 'לפעמים', 'correct': 'a'},
        {'text_es': '¿Langostas kosher?', 'text_en': 'Kosher locusts?', 'text_he': 'חגבים כשרים?', 'a_es': 'Algunos tipos', 'a_en': 'Some types', 'a_he': 'סוגים מסוימים', 'b_es': 'Todas', 'b_en': 'All', 'b_he': 'הכל', 'c_es': 'Ninguna', 'c_en': 'None', 'c_he': 'אף אחד', 'correct': 'a'},
        {'text_es': '¿Tocar cadáver impuro?', 'text_en': 'Touch impure carcass?', 'text_he': 'נגיעה בנבלה?', 'a_es': 'Queda impuro', 'a_en': 'Becomes impure', 'a_he': 'נטמא', 'b_es': 'No pasa nada', 'b_en': 'Nothing happens', 'b_he': 'לא קורה כלום', 'c_es': 'Se limpia solo', 'c_en': 'Cleans self', 'c_he': 'ניקוי עצמי', 'correct': 'a'},
        {'text_es': '¿Moisés instruyó a?', 'text_en': 'Moses instructed?', 'text_he': 'משה הורה ל?', 'a_es': 'Aharón', 'a_en': 'Aaron', 'a_he': 'אהרן', 'b_es': 'Egipto', 'b_en': 'Egypt', 'b_he': 'מצרים', 'c_es': 'Koraj', 'c_en': 'Korach', 'c_he': 'קורח', 'correct': 'a'},
        {'text_es': '¿El Shabat es de?', 'text_en': 'Shabbat is?', 'text_he': 'שבת היא?', 'a_es': 'Santo', 'a_en': 'Holy', 'a_he': 'קודש', 'b_es': 'Trabajo', 'b_en': 'Work', 'b_he': 'עבודה', 'c_es': 'Común', 'c_en': 'Common', 'c_he': 'חול', 'correct': 'a'}
    ])

    # TAZRIA-METZORA
    add_questions('Tazría-Metzorá', [
        {'text_es': '¿Circuncisión qué día?', 'text_en': 'Circumcision day?', 'text_he': 'ברית מילה ביום?', 'a_es': '8vo', 'a_en': '8th', 'a_he': 'שמיני', 'b_es': '1ro', 'b_en': '1st', 'b_he': 'ראשון', 'c_es': '13ro', 'c_en': '13th', 'c_he': '13', 'correct': 'a'},
        {'text_es': '¿Quién diagnostica Tzaraat?', 'text_en': 'Who diagnoses Tzaraat?', 'text_he': 'מי מאבחן צרעת?', 'a_es': 'Kohén', 'a_en': 'Kohen', 'a_he': 'כהן', 'b_es': 'Médico', 'b_en': 'Doctor', 'b_he': 'רופא', 'c_es': 'Juez', 'c_en': 'Judge', 'c_he': 'שופט', 'correct': 'a'},
        {'text_es': '¿Metzorá vive?', 'text_en': 'Metzora lives?', 'text_he': 'מצורע גר?', 'a_es': 'Fuera del campo', 'a_en': 'Outside camp', 'a_he': 'מחוץ למחנה', 'b_es': 'En su tienda', 'b_en': 'In his tent', 'b_he': 'באוהל', 'c_es': 'En la ciudad', 'c_en': 'In city', 'c_he': 'בעיר', 'correct': 'a'},
        {'text_es': '¿Tzaraat en la ropa?', 'text_en': 'Tzaraat in clothes?', 'text_he': 'צרעת בבגדים?', 'a_es': 'Sí', 'a_en': 'Yes', 'a_he': 'כן', 'b_es': 'No', 'b_en': 'No', 'b_he': 'לא', 'c_es': 'Solo de seda', 'c_en': 'Silk only', 'c_he': 'רק משי', 'correct': 'a'},
        {'text_es': '¿Tzaraat en casas?', 'text_en': 'Tzaraat in houses?', 'text_he': 'צרעת בבתים?', 'a_es': 'Sí', 'a_en': 'Yes', 'a_he': 'כן', 'b_es': 'No', 'b_en': 'No', 'b_he': 'לא', 'c_es': 'Solo palacios', 'c_en': 'Palaces only', 'c_he': 'רק ארמון', 'correct': 'a'},
        {'text_es': '¿Purificación con qué?', 'text_en': 'Purification with?', 'text_he': 'טהרה עם?', 'a_es': 'Aves e Hisopo', 'a_en': 'Birds & Hyssop', 'a_he': 'ציפורים ואזוב', 'b_es': 'Vino', 'b_en': 'Wine', 'b_he': 'יין', 'c_es': 'Aceite solo', 'c_en': 'Oil only', 'c_he': 'שמן', 'correct': 'a'},
        {'text_es': '¿Madre trae ofrenda?', 'text_en': 'Mother brings offering?', 'text_he': 'יולדת מביאה קורבן?', 'a_es': 'Sí', 'a_en': 'Yes', 'a_he': 'כן', 'b_es': 'No', 'b_en': 'No', 'b_he': 'לא', 'c_es': 'Solo si es niño', 'c_en': 'Boy only', 'c_he': 'רק לבן', 'correct': 'a'},
        {'text_es': '¿Número de aves purificación?', 'text_en': 'Number of birds?', 'text_he': 'כמה ציפורים?', 'a_es': '2', 'a_en': '2', 'a_he': '2', 'b_es': '1', 'b_en': '1', 'b_he': '1', 'c_es': '10', 'c_en': '10', 'c_he': '10', 'correct': 'a'},
        {'text_es': '¿Metzorá grita?', 'text_en': 'Metzora yells?', 'text_he': 'מצורע קורא?', 'a_es': 'Impuro, Impuro', 'a_en': 'Impure, Impure', 'a_he': 'טמא, טמא', 'b_es': '¡Ayuda!', 'b_en': 'Help!', 'b_he': 'עזרה!', 'c_es': 'Shalom', 'c_en': 'Shalom', 'c_he': 'שלום', 'correct': 'a'},
        {'text_es': '¿Agua viva para?', 'text_en': 'Living water for?', 'text_he': 'מים חיים למה?', 'a_es': 'Purificar', 'a_en': 'Purify', 'a_he': 'טהרה', 'b_es': 'Beber solo', 'b_en': 'Drinking only', 'b_he': 'שתייה', 'c_es': 'Cocinar', 'c_en': 'Cook', 'c_he': 'בישול', 'correct': 'a'}
    ])

    # AJAREI MOT-KEDOSHIM
    add_questions('Ajarei Mot-Kedoshim', [
        {'text_es': '¿Yom Kippur quién entra?', 'text_en': 'Yom Kippur entry?', 'text_he': 'מי נכנס ביוה"כ?', 'a_es': 'Sumo Sacerdote', 'a_en': 'High Priest', 'a_he': 'כהן גדול', 'b_es': 'Cualquiera', 'b_en': 'Anyone', 'b_he': 'כל אחד', 'c_es': 'Moisés', 'c_en': 'Moses', 'c_he': 'משה', 'correct': 'a'},
        {'text_es': '¿Chivo para?', 'text_en': 'Goat for?', 'text_he': 'שעיר לעזאזל?', 'a_es': 'Azazel', 'a_en': 'Azazel', 'a_he': 'עזאזל', 'b_es': 'Comer', 'b_en': 'Eating', 'b_he': 'אכילה', 'c_es': 'Ofrenda vegetal', 'c_en': 'Veggie off', 'c_he': 'מנחה', 'correct': 'a'},
        {'text_es': '¿Amarás a tu prójimo como...?', 'text_en': 'Love neighbor as...?', 'text_he': 'ואהבת לרעך כמו?', 'a_es': 'A ti mismo', 'a_en': 'Yourself', 'a_he': 'כמוך', 'b_es': 'A Dios', 'b_en': 'As God', 'b_he': 'כה\'', 'c_es': 'Al rey', 'c_en': 'The king', 'c_he': 'כמלך', 'correct': 'a'},
        {'text_es': '¿Prohibido tatuarse?', 'text_en': 'Forbidden tattoos?', 'text_he': 'אסור קעקע?', 'a_es': 'Sí', 'a_en': 'Yes', 'a_he': 'כן', 'b_es': 'No', 'b_en': 'No', 'b_he': 'לא', 'c_es': 'Solo en la cara', 'c_en': 'Face only', 'c_he': 'רק פנים', 'correct': 'a'},
        {'text_es': '¿Respetar a los ancianos?', 'text_en': 'Respect elders?', 'text_he': 'כבוד זקנים?', 'a_es': 'Es mandamiento', 'a_en': 'Is command', 'a_he': 'מצווה', 'b_es': 'Es opcional', 'b_en': 'Optional', 'b_he': 'רשות', 'c_es': 'Prohibido', 'c_en': 'Forbidden', 'c_he': 'אסור', 'correct': 'a'},
        {'text_es': '¿No pongas tropiezo al...?', 'text_en': 'Don\'t block the...?', 'text_he': 'לפני עיוור לא תתן?', 'a_es': 'Ciego', 'a_en': 'Blind', 'a_he': 'מכשול', 'b_es': 'Rey', 'b_en': 'King', 'b_he': 'מלך', 'c_es': 'Sacerdote', 'c_en': 'Priest', 'c_he': 'כהן', 'correct': 'a'},
        {'text_es': '¿Día de expiación?', 'text_en': 'Day of atonement?', 'text_he': 'יום הכיפורים?', 'a_es': '10 de Tishrei', 'a_en': '10th Tishrei', 'a_he': 'י\' תשרי', 'b_es': '1 de Nisán', 'b_en': '1st Nissan', 'b_he': 'א\' ניסן', 'c_es': '15 de Adar', 'c_en': '15th Adar', 'c_he': 'ט"ו אדר', 'correct': 'a'},
        {'text_es': '¿Sangre se puede comer?', 'text_en': 'Can eat blood?', 'text_he': 'אכילת דם?', 'a_es': 'Prohibido', 'a_en': 'Forbidden', 'a_he': 'אסור', 'b_es': 'Permitido', 'b_en': 'Permitted', 'b_he': 'מותר', 'c_es': 'Opcional', 'c_en': 'Optional', 'c_he': 'רשות', 'correct': 'a'},
        {'text_es': '¿Sé santo porque...?', 'text_en': 'Be holy because...?', 'text_he': 'קדושים תהיו כי?', 'a_es': 'Yo soy santo', 'a_en': 'I am holy', 'a_he': 'אני קדוש', 'b_es': 'Es bueno', 'b_en': 'It is good', 'b_he': 'זה טוב', 'c_es': 'Moisés dice', 'c_en': 'Moses says', 'c_he': 'משה אמר', 'correct': 'a'},
        {'text_es': '¿Dejar las esquinas del campo?', 'text_en': 'Leave corners of field?', 'text_he': 'פאת השדה?', 'a_es': 'Para el pobre', 'a_en': 'For poor', 'a_he': 'לעני', 'b_es': 'Para quemar', 'b_en': 'For burning', 'b_he': 'לשריפה', 'c_es': 'Para el rey', 'c_en': 'For king', 'c_he': 'למלך', 'correct': 'a'}
    ])

    # EMOR
    add_questions('Emor', [
        {'text_es': '¿Kohén con muertos?', 'text_en': 'Kohen & dead?', 'text_he': 'כהן ומתים?', 'a_es': 'Solo familiares directos', 'a_en': 'Only direct family', 'a_he': 'שרק קרובים', 'b_es': 'Con cualquiera', 'b_en': 'With anyone', 'b_he': 'כל אחד', 'c_es': 'Prohibido siempre', 'c_en': 'Always forbidden', 'c_he': 'תמיד אסור', 'correct': 'a'},
        {'text_es': '¿Kohen Gadol con muertos?', 'text_en': 'Kohen Gadol & dead?', 'text_he': 'כהן גדול ומתים?', 'a_es': 'Prohibido incluso directos', 'a_en': 'Forbidden even direct', 'a_he': 'אפילו לא קרובים', 'b_es': 'Permitido', 'b_en': 'Permitted', 'b_he': 'מותר', 'c_es': 'Solo padres', 'c_en': 'Parents only', 'c_he': 'רק הורים', 'correct': 'a'},
        {'text_es': '¿Cuántas fiestas anuales?', 'text_en': 'Annual festivals?', 'text_he': 'מועדי ה\'?', 'a_es': 'Shabat, Pesach, Shavuot...', 'a_en': 'Shabbat, Pesach...', 'a_he': 'שבת, פסח...', 'b_es': 'Solo una', 'b_en': 'Only one', 'b_he': 'רק אחד', 'c_es': 'Diez mil', 'c_en': 'Ten thousand', 'c_he': 'עשרת אלפים', 'correct': 'a'},
        {'text_es': '¿Pesach qué día?', 'text_en': 'Pesach day?', 'text_he': 'פסח ביום?', 'a_es': '15 de Nisán', 'a_en': '15th Nissan', 'a_he': 'ט"ו ניסן', 'b_es': '1 de Tishrei', 'b_en': '1st Tishrei', 'b_he': 'א\' תשרי', 'c_es': '10 de Tevet', 'c_en': '10th Tevet', 'c_he': 'י\' טבת', 'correct': 'a'},
        {'text_es': '¿Omer por cuántos días?', 'text_en': 'Omer for how many days?', 'text_he': 'ספירת העומר?', 'a_es': '49', 'a_en': '49', 'a_he': '49', 'b_es': '30', 'b_en': '30', 'b_he': '30', 'c_es': '7', 'c_en': '7', 'c_he': '7', 'correct': 'a'},
        {'text_es': '¿Sukkót habitas en?', 'text_en': 'Sukkot live in?', 'text_he': 'בסוכות תשבו ב?', 'a_es': 'Sukká (Cabañas)', 'a_en': 'Sukkah', 'a_he': 'סוכות', 'b_es': 'Casas de piedra', 'b_en': 'Stone houses', 'b_he': 'בית אבן', 'c_es': 'Cuevas', 'c_en': 'Caves', 'c_he': 'מערות', 'correct': 'a'},
        {'text_es': '¿Lulav cuántas especies?', 'text_en': 'Lulav species?', 'text_he': 'ארבעת המינים?', 'a_es': '4', 'a_en': '4', 'a_he': '4', 'b_es': '1', 'b_en': '1', 'b_he': '1', 'c_es': '7', 'c_en': '7', 'c_he': '7', 'correct': 'a'},
        {'text_es': '¿Panes de la proposición?', 'text_en': 'Showbread count?', 'text_he': 'לחם הפנים?', 'a_es': '12', 'a_en': '12', 'a_he': '12', 'b_es': '2', 'b_en': '2', 'b_he': '2', 'c_es': '10', 'c_en': '10', 'c_he': '10', 'correct': 'a'},
        {'text_es': '¿Castigo al blasfemo?', 'text_en': 'Blasphemer punishment?', 'text_he': 'עונש המקלל?', 'a_es': 'Muerte', 'a_en': 'Death', 'a_he': 'מוות', 'b_es': 'Multa', 'b_en': 'Fine', 'b_he': 'קנס', 'c_es': 'Exilio', 'c_en': 'Exile', 'c_he': 'גלות', 'correct': 'a'},
        {'text_es': '¿Ojo por ojo?', 'text_en': 'Eye for an eye?', 'text_he': 'עין תחת עין?', 'a_es': 'Compensación equitativa', 'a_en': 'Fair compensation', 'a_he': 'פיצוי הולם', 'b_es': 'Literal', 'b_en': 'Literal', 'b_he': 'ממש', 'c_es': 'Perdonar siempre', 'c_en': 'Forgive always', 'c_he': 'סליחה', 'correct': 'a'}
    ])

    # BEHAR-BEJUKOTAI
    add_questions('Behar-Bejukotai', [
        {'text_es': '¿Shmitá cada cuánto?', 'text_en': 'Shmita frequency?', 'text_he': 'שמיטה כל?', 'a_es': '7 años', 'a_en': '7 years', 'a_he': '7 שנים', 'b_es': '1 año', 'b_en': '1 year', 'b_he': 'שנה אחת', 'c_es': '50 años', 'c_en': '50 years', 'c_he': '50 שנה', 'correct': 'a'},
        {'text_es': '¿Yovel (Jubileo) año?', 'text_en': 'Jubilee year?', 'text_he': 'שנת היובל?', 'a_es': '50', 'a_en': '50', 'a_he': '50', 'b_es': '10', 'b_en': '10', 'b_he': '10', 'c_es': '100', 'c_en': '100', 'c_he': '100', 'correct': 'a'},
        {'text_es': '¿Esclavos en Yovel?', 'text_en': 'Slaves in Jubilee?', 'text_he': 'עבדים ביובל?', 'a_es': 'Quedan libres', 'a_en': 'Go free', 'a_he': 'יוצאים לחופשי', 'b_es': 'Siguen igual', 'b_en': 'Stay same', 'b_he': 'נשארים', 'c_es': 'Se venden', 'c_en': 'Are sold', 'c_he': 'נמכרים', 'correct': 'a'},
        {'text_es': '¿Tierras en Yovel?', 'text_en': 'Lands in Jubilee?', 'text_he': 'קרקעות ביובל?', 'a_es': 'Vuelven al dueño original', 'a_en': 'Return to owner', 'a_he': 'חוזרות לבעלים', 'b_es': 'Se pierden', 'b_en': 'Are lost', 'b_he': 'אובדות', 'c_es': 'Se queman', 'c_en': 'Are burned', 'c_he': 'נשרפות', 'correct': 'a'},
        {'text_es': '¿Bendiciones por cumplir?', 'text_en': 'Blessings for obeying?', 'text_he': 'ברכות הציות?', 'a_es': 'Lluvia y paz', 'a_en': 'Rain & peace', 'a_he': 'גשם ושלום', 'b_es': 'Solo oro', 'b_en': 'Gold only', 'b_he': 'רק זהב', 'c_es': 'Volar', 'c_en': 'Flying', 'c_he': 'תעופה', 'correct': 'a'},
        {'text_es': '¿Advertencias (Tojejá)?', 'text_en': 'Warnings (Tochacha)?', 'text_he': 'התוכחה?', 'a_es': 'Consecuencias por desobediencia', 'a_en': 'Results of disobeying', 'a_he': 'קללות על אי ציות', 'b_es': 'Fiestas', 'b_en': 'Festivals', 'b_he': 'חגים', 'c_es': 'Premios', 'c_en': 'Prizes', 'c_he': 'פרסים', 'correct': 'a'},
        {'text_es': '¿Diezmo de ganado?', 'text_en': 'Tithes of cattle?', 'text_he': 'מעשר בהמה?', 'a_es': 'Cada décimo es santo', 'a_en': '10th is holy', 'a_he': 'העשירי קדש', 'b_es': 'El primero', 'b_en': 'The first', 'b_he': 'הראשון', 'c_es': 'Solo ovejas negras', 'c_en': 'Black sheep only', 'c_he': 'רק שחורות', 'correct': 'a'},
        {'text_es': '¿Redimir una ofrenda?', 'text_en': 'Redeem offering?', 'text_he': 'פדיון קודש?', 'a_es': 'Añadir un quinto', 'a_en': 'Add a fifth', 'a_he': 'הוספת חומש', 'b_es': 'Gratis', 'b_en': 'Free', 'b_he': 'חינם', 'c_es': 'Imposible', 'c_en': 'Impossible', 'c_he': 'בלתי אפשרי', 'correct': 'a'},
        {'text_es': '¿Votos (Arjin)?', 'text_en': 'Vows value?', 'text_he': 'ערכין?', 'a_es': 'Valores fijos', 'a_en': 'Fixed values', 'a_he': 'ערכים קבועים', 'b_es': 'Sorteo', 'b_en': 'Lottery', 'b_he': 'גורל', 'c_es': 'Subasta', 'c_en': 'Auction', 'c_he': 'מכירה', 'correct': 'a'},
        {'text_es': '¿Libro que termina?', 'text_en': 'Book that ends?', 'text_he': 'איזה ספר מסתיים?', 'a_es': 'Levítico (Vayikrá)', 'a_en': 'Leviticus', 'a_he': 'ויקרא', 'b_es': 'Éxodo', 'b_en': 'Exodus', 'b_he': 'שמות', 'c_es': 'Números', 'c_en': 'Numbers', 'c_he': 'במדבר', 'correct': 'a'}
    ])

    # BEMIDBAR
    add_questions('Bemidbar', [
        {'text_es': '¿Dónde estaban?', 'text_en': 'Where were they?', 'text_he': 'איפה היו?', 'a_es': 'Desierto del Sinaí', 'a_en': 'Sinai Desert', 'a_he': 'מדבר סיני', 'b_es': 'Egipto', 'b_en': 'Egypt', 'b_he': 'מצרים', 'c_es': 'Canaán', 'c_en': 'Canaan', 'c_he': 'כנען', 'correct': 'a'},
        {'text_es': '¿Censo de quiénes?', 'text_en': 'Census of whom?', 'text_he': 'מפקד של?', 'a_es': 'Hombres para la guerra', 'a_en': 'Men for war', 'a_he': 'יוצאי צבא', 'b_es': 'Solo niños', 'b_en': 'Only children', 'b_he': 'רק ילדים', 'c_es': 'Toda la creación', 'c_en': 'All creation', 'c_he': 'כל היצורים', 'correct': 'a'},
        {'text_es': '¿Hijos de Israel?', 'text_en': 'Sons of Israel?', 'text_he': 'בני ישראל?', 'a_es': '12 tribus principales', 'a_en': '12 main tribes', 'a_he': '12 שבטים', 'b_es': '100 tribus', 'b_en': '100 tribes', 'b_he': '100 שבטים', 'c_es': 'Solo una', 'c_en': 'Only one', 'c_he': 'שבט אחד', 'correct': 'a'},
        {'text_es': '¿Quiénes rodean el Mishkán?', 'text_en': 'Who surround Mishkan?', 'text_he': 'חונים סביב למשכן?', 'a_es': 'Levitas', 'a_en': 'Levites', 'a_he': 'לוויים', 'b_es': 'Egipto', 'b_en': 'Egyptians', 'b_he': 'מצרים', 'c_es': 'Animales', 'c_en': 'Animals', 'c_he': 'חיות', 'correct': 'a'},
        {'text_es': '¿Sustitutos de primogénitos?', 'text_en': 'Substitutes for firstborns?', 'text_he': 'במקום הבכורות?', 'a_es': 'Levitas', 'a_en': 'Levites', 'a_he': 'לוויים', 'b_es': 'Kohanim solo', 'b_en': 'Kohanim only', 'b_he': 'רק כהנים', 'c_es': 'Ovejas', 'c_en': 'Sheep', 'c_he': 'כבשים', 'correct': 'a'},
        {'text_es': '¿Tribu de Judá dónde?', 'text_en': 'Judah tribe where?', 'text_he': 'שבט יהודה?', 'a_es': 'Al Este', 'a_en': 'East', 'a_he': 'מזרח', 'b_es': 'Oeste', 'b_en': 'West', 'b_he': 'מערב', 'c_es': 'Norte', 'c_en': 'North', 'c_he': 'צפון', 'correct': 'a'},
        {'text_es': '¿Quién cargaba el Arca?', 'text_en': 'Who carried Ark?', 'text_he': 'מי נשא את הארון?', 'a_es': 'Hijos de Kehat', 'a_en': 'Sons of Kehat', 'a_he': 'בני קהת', 'b_es': 'Animales', 'b_en': 'Animals', 'b_he': 'חיות', 'c_es': 'Los príncipes', 'c_en': 'Princes', 'c_he': 'נשיאים', 'correct': 'a'},
        {'text_es': '¿Edad para servicio?', 'text_en': 'Age for service?', 'text_he': 'גיל לעבודה?', 'a_es': '30 a 50 años', 'a_en': '30 to 50 years', 'a_he': '30-50', 'b_es': '10 a 20', 'b_en': '10 to 20', 'b_he': '10-20', 'c_es': 'Cualquiera', 'c_en': 'Any', 'c_he': 'כל גיל', 'correct': 'a'},
        {'text_es': '¿Estandartes (Degalim)?', 'text_en': 'Flags (Degalim)?', 'text_he': 'דגלים?', 'a_es': 'Cada grupo tenía uno', 'a_en': 'Each group had one', 'a_he': 'לכל מחנה דגל', 'b_es': 'No había', 'b_en': 'None', 'b_he': 'אין', 'c_es': 'Eran invisibles', 'c_en': 'Invisible', 'c_he': 'שקוף', 'correct': 'a'},
        {'text_es': '¿Líder de Kehat?', 'text_en': 'Kehat leader?', 'text_he': 'נשיא קהת?', 'a_es': 'Elizafán', 'a_en': 'Elizaphan', 'a_he': 'אליצפן', 'b_es': 'Moisés', 'b_en': 'Moses', 'b_he': 'משה', 'c_es': 'Yona', 'c_en': 'Jonah', 'c_he': 'יונה', 'correct': 'a'}
    ])

    db.session.commit()
    print("Batch 2 completed.")
