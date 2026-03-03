import sys
import os
sys.path.append(os.getcwd())
from app import create_app, db
from app.models import HalajaCategory, HalajaQuestion
from app.halaja_bank import HALAJA_BANK
import random

def sync_halaja_bank():
    app = create_app()
    with app.app_context():
        # Ensure categories exist
        category_map = {}
        categories = HalajaCategory.query.all()
        for cat in categories:
            category_map[cat.name_es] = cat.id
            category_map[cat.name_en] = cat.id

        added_count = 0
        for q_data in HALAJA_BANK:
            # Avoid direct duplicates by text
            exists = HalajaQuestion.query.filter_by(text_es=q_data['t_es']).first()
            if not exists:
                cat_id = category_map.get(q_data['category'])
                if not cat_id:
                    # Generic or fallback
                    cat_id = category_map.get('Leyes Generales') or categories[0].id
                
                # Randomize options for the static entry too
                opts = [
                    {'es': q_data['a_es'], 'en': q_data['a_en'], 'he': q_data['a_he'], 'correct': True},
                    {'es': q_data['b_es'], 'en': q_data['b_en'], 'he': q_data['b_he'], 'correct': False},
                    {'es': q_data['c_es'], 'en': q_data['c_en'], 'he': q_data['c_he'], 'correct': False}
                ]
                random.shuffle(opts)
                
                corr = 'a'
                for i, letter in enumerate(['a', 'b', 'c']):
                    if opts[i]['correct']: corr = letter

                new_q = HalajaQuestion(
                    category_id=cat_id,
                    text_es=q_data['t_es'], text_en=q_data['t_en'], text_he=q_data['t_he'],
                    option_a_es=opts[0]['es'], option_a_en=opts[0]['en'], option_a_he=opts[0]['he'],
                    option_b_es=opts[1]['es'], option_b_en=opts[1]['en'], option_b_he=opts[1]['he'],
                    option_c_es=opts[2]['es'], option_c_en=opts[2]['en'], option_c_he=opts[2]['he'],
                    correct_option=corr
                )
                db.session.add(new_q)
                added_count += 1
        
        db.session.commit()
        print(f"Sync complete. Added {added_count} new high-level questions to the database.")

if __name__ == "__main__":
    sync_halaja_bank()
