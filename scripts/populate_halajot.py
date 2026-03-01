import sys
import os
sys.path.append(os.getcwd())
from app import create_app, db
from app.models import HalajaCategory, HalajaQuestion
import random

def populate_halajot():
    app = create_app()
    with app.app_context():
        # Define Categories
        categories_data = [
            {'es': 'Shabat', 'en': 'Shabbat', 'he': 'שבת', 'icon': '🕯️'},
            {'es': 'Kashrut (Carne y Leche)', 'en': 'Kashrut (Meat & Milk)', 'he': 'כשרות (בשר וחלב)', 'icon': '🍷'},
            {'es': 'Tefilá', 'en': 'Prayer', 'he': 'תפילה', 'icon': '🙏'},
            {'es': 'Festividades', 'en': 'Holidays', 'he': 'חגים', 'icon': '🎉'},
            {'es': 'Leyes Generales', 'en': 'General Laws', 'he': 'הלכות כלליות', 'icon': '📜'}
        ]

        categories = {}
        for c_data in categories_data:
            cat = HalajaCategory.query.filter_by(name_es=c_data['es']).first()
            if not cat:
                cat = HalajaCategory(
                    name_es=c_data['es'],
                    name_en=c_data['en'],
                    name_he=c_data['he'],
                    icon=c_data['icon']
                )
                db.session.add(cat)
                db.session.flush()
            categories[c_data['es']] = cat

        # 5 High-Level Questions
        questions_data = [
            {
                'cat': 'Shabat',
                't_es': '¿Cuál es la regla de "Borer" (seleccionar) respecto a un objeto que se desea usar de inmediato?',
                't_en': 'What is the rule of "Borer" (selecting) regarding an object one wishes to use immediately?',
                't_he': 'מהו הכלל במלאכת "בורר" לגבי חפץ שרוצים להשתמש בו מיד?',
                'a_es': 'Se permite si es "Ojel mitoj Psolet" (el bueno del malo) y para uso inmediato', 'a_en': 'Permitted if it is "Ochel mi-toch Psolet" (the good from the bad) and for immediate use', 'a_he': 'מותר בבורר אוכל מתוך פסולת, ביד, ולאלתר',
                'b_es': 'Está prohibido seleccionar incluso con la mano si los objetos están mezclados', 'b_en': 'It is forbidden to select even by hand if the objects are mixed', 'b_he': 'אסור לברור אפילו ביד אם החפצים מעורבבים',
                'c_es': 'Se permite solo si se usa un colador o herramienta específica', 'c_en': 'Permitted only if a strainer or specific tool is used', 'c_he': 'מותר רק אם משתמשים בכלי המיועד לכך (מסננת וכדו\')',
            },
            {
                'cat': 'Kashrut (Carne y Leche)',
                't_es': 'Según la Halajá, ¿cuánto tiempo debe pasar tras comer carne antes de consumir lácteos?',
                't_en': 'According to Halacha, how much time must pass after eating meat before consuming dairy?',
                't_he': 'כמה זמן יש להמתין לאחר אכילת בשר לפני אכילת חלב?',
                'a_es': '6 horas completas (según la costumbre mayoritaria)', 'a_en': '6 full hours (following majority custom)', 'a_he': 'שש שעות מלאות (כמנהג רוב קהילות ישראל)',
                'b_es': '3 horas son suficientes si se limpia la boca adecuadamente', 'b_en': '3 hours are sufficient if the mouth is cleaned properly', 'b_he': 'שלוש שעות מספיקות אם מנקים את הפה היטב',
                'c_es': 'Solo hasta la siguiente comida, no hay tiempo fijo', 'c_en': 'Only until the next meal, there is no fixed time', 'c_he': 'רק עד הסעודה הבאה, אין זמן קצוב',
            },
            {
                'cat': 'Tefilá',
                't_es': '¿Qué debe hacer una persona que olvidó decir "Yaalé VeYavó" en la Amidá de Rosh Jodesh?',
                't_en': 'What should a person do if they forgot to say "Yaaleh VeYavo" in the Amidah of Rosh Chodesh?',
                't_he': 'מי ששכח לומר "יעלה ויבוא" בתפילת עמידה של ראש חודש, מה דינו?',
                'a_es': 'Si terminó la Amidá, debe repetirla desde el principio', 'a_en': 'If they finished the Amidah, they must repeat it from the beginning', 'a_he': 'אם סיים את התפילה, חייב לחזור לראש',
                'b_es': 'Puede decir una oración corta al final sin repetir', 'b_en': 'They can say a short prayer at the end without repeating', 'b_he': 'יכול לומר תפילה קצרה בסיום (ללא חזרה)',
                'c_es': 'No debe repetir, se considera compensado con el Halel', 'c_en': 'They should not repeat, it is considered compensated by Hallel', 'c_he': 'אינו חוזר, שכן תפילת ההלל משלימה זאת',
            },
            {
                'cat': 'Leyes Generales',
                't_es': '¿Cuál es la jerarquía de prioridad en "Birkat HaNehenín" (bendiciones por comida)?',
                't_en': 'What is the priority hierarchy in "Birkat HaNehenin" (blessings for food)?',
                't_he': 'מהו סדר הקדימות בברכות הנהנין (מג"ע א"ש)?',
                'a_es': 'Mezonot, Guefen, Etz, Adamá, Shehakol', 'a_en': 'Mezonot, Gefen, Etz, Adama, Shehakol', 'a_he': 'מזונות, גפן, עץ, אדמה, שהכל (מג"ע א"ש)',
                'b_es': 'Etz, Adamá, Mezonot, Shehakol, Guefen', 'b_en': 'Etz, Adama, Mezonot, Shehakol, Gefen', 'b_he': 'עץ, אדמה, מזונות, שהכל, גפן',
                'c_es': 'Primero lo que más le guste a la persona, sin orden fijo', 'c_en': 'First what the person likes most, with no fixed order', 'c_he': 'מברך קודם כל על מה שחביב עליו, ללא סדר קבוע',
            },
            {
                'cat': 'Shabat',
                't_es': '¿Se permite abrir un paraguas en Shabat según el Shulján Aruj?',
                't_en': 'Is it permitted to open an umbrella on Shabbat according to the Shulchan Aruch?',
                't_he': 'האם מותר לפתוח מטריה בשבת לפי השולחן ערוך?',
                'a_es': 'Está prohibido por la prohibición de crear una tienda (Ohel)', 'a_en': 'It is forbidden due to the prohibition of creating a tent (Ohel)', 'a_he': 'אסור משום עשיית אוהל (ואף משום מראית עין)',
                'b_es': 'Se permite si no llueve fuerte', 'b_en': 'It is permitted if it is not raining heavily', 'b_he': 'מותר אם הגשם אינו חזק מדי',
                'c_es': 'Se permite si ya estaba un poco abierto antes de Shabat', 'c_en': 'It is permitted if it was already slightly open before Shabbat', 'c_he': 'מותר אם היה פתוח מעט מערב שבת',
            }
        ]

        for q_data in questions_data:
            # Randomize options
            options = [
                {'es': q_data['a_es'], 'en': q_data['a_en'], 'he': q_data['a_he'], 'orig': 'a'},
                {'es': q_data['b_es'], 'en': q_data['b_en'], 'he': q_data['b_he'], 'orig': 'b'},
                {'es': q_data['c_es'], 'en': q_data['c_en'], 'he': q_data['c_he'], 'orig': 'c'}
            ]
            random.shuffle(options)
            
            final_correct = 'a'
            for i, letter in enumerate(['a', 'b', 'c']):
                if options[i]['orig'] == 'a':
                    final_correct = letter

            cat = categories[q_data['cat']]
            q = HalajaQuestion(
                category_id=cat.id,
                text_es=q_data['t_es'], text_en=q_data['t_en'], text_he=q_data['t_he'],
                option_a_es=options[0]['es'], option_a_en=options[0]['en'], option_a_he=options[0]['he'],
                option_b_es=options[1]['es'], option_b_en=options[1]['en'], option_b_he=options[1]['he'],
                option_c_es=options[2]['es'], option_c_en=options[2]['en'], option_c_he=options[2]['he'],
                correct_option=final_correct
            )
            db.session.add(q)
        
        db.session.commit()
        print("Halajot categories and questions added successfully.")

if __name__ == "__main__":
    populate_halajot()
