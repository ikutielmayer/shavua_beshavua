from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from flask_login import login_required, current_user
from ..models import Parasha, Question, Participation, User, Donation, UserAnswer, HalajaCategory, HalajaQuestion, HalajaAnswer
from .. import db
from datetime import datetime, time, timedelta
from ..translations import translate

user_routes = Blueprint('user', __name__)

def get_current_parasha_internal():
    now = datetime.now()
    weekday = now.weekday()
    # From Motzei Shabbat (Saturday 20:30) until Friday, we show the coming Shabbat's Parasha
    days_to_saturday = (5 - weekday) % 7
    if weekday == 5 and now.time() >= time(20, 30):
        days_to_saturday = 7
    target_saturday = (now + timedelta(days=days_to_saturday)).date()
    parasha = Parasha.query.filter(Parasha.week_end >= target_saturday).order_by(Parasha.week_end.asc()).first()
    return parasha

@user_routes.route('/participate')
@login_required
def participate():
    import random
    # Get current week's parasha
    parasha = get_current_parasha_internal()
    
    if not parasha:
        # If no parasha is active, try to fetch the internal current one
        parasha = get_current_parasha_internal()
        if not parasha:
            # If still none, create a placeholder for the current week so we can attach questions
            from datetime import timedelta
            now = datetime.now()
            # Find next Saturday
            days_until_saturday = (5 - now.weekday()) % 7
            saturday = now + timedelta(days=days_until_saturday)
            
            # Use bank to find a name if possible or default to "Parasha Semanal"
            from ..parasha_bank import PARASHA_BANK
            available_names = list(PARASHA_BANK.keys())
            name_es = available_names[0] if available_names else "Parasha de la Semana"
            
            parasha = Parasha(
                name_es=name_es, name_en=name_es, name_he=name_es,
                week_start=now.date(), week_end=saturday.date()
            )
            db.session.add(parasha)
            db.session.commit()
            db.session.refresh(parasha)

    # Daily Generation Check for Parasha (Limit: 5 questions total per day)
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_parasha_answers = UserAnswer.query.join(Question).filter(
        UserAnswer.user_id == current_user.id,
        Question.parasha_id == parasha.id,
        UserAnswer.timestamp >= today_start
    ).count()

    # Calculate unanswered count
    unanswered_q = Question.query.filter_by(parasha_id=parasha.id).filter(
        ~Question.id.in_(db.session.query(UserAnswer.question_id).filter_by(user_id=current_user.id))
    ).all()
    unanswered_count = len(unanswered_q)

    # DYNAMIC GENERATION: Ensure at least 5 questions exist for this user IF they haven't reached daily limit
    if unanswered_count < 5 and today_parasha_answers < 5:
        from ..parasha_bank import PARASHA_BANK
        seed_pool = PARASHA_BANK.get(parasha.name_es) or PARASHA_BANK.get(parasha.name_en) or []
        
        if not seed_pool:
            # Fallback to any available parasha bank if current not found
            for p_name in PARASHA_BANK:
                seed_pool = PARASHA_BANK[p_name]
                break

        if seed_pool:
            # Add up to 5 fresh questions from bank
            # We don't filter existing_texts here to allow "reuse" across DB but new instances to keep user sets unique
            to_add = random.sample(seed_pool, min(5, len(seed_pool)))
            for q_data in to_add:
                new_q = Question(
                    parasha_id=parasha.id,
                    text_es=q_data['t_es'], text_en=q_data['t_en'], text_he=q_data['t_he'],
                    option_a_es=q_data['a_es'], option_a_en=q_data['a_en'], option_a_he=q_data['a_he'],
                    option_b_es=q_data['b_es'], option_b_en=q_data['b_en'], option_b_he=q_data['b_he'],
                    option_c_es=q_data['c_es'], option_c_en=q_data['c_en'], option_c_he=q_data['c_he'],
                    correct_option='a'
                )
                db.session.add(new_q)
            db.session.commit()
            db.session.refresh(parasha)

    # Fetch fresh questions after DB update
    questions = Question.query.filter_by(parasha_id=parasha.id).filter(
        ~Question.id.in_(db.session.query(UserAnswer.question_id).filter_by(user_id=current_user.id))
    ).all()
    
    if not questions:
        # Check if they have a Participation record, if not, create it as they just finished everything
        existing_p = Participation.query.filter_by(user_id=current_user.id, parasha_id=parasha.id).first()
        if not existing_p:
            # Re-calculate score to create the summary record
            all_answers = UserAnswer.query.join(Question).filter(
                UserAnswer.user_id == current_user.id,
                Question.parasha_id == parasha.id
            ).all()
            total_score = sum(1 for a in all_answers if a.is_correct)
            total_questions = len(parasha.questions)
            percentage = (total_score / total_questions * 100) if total_questions > 0 else 0
            
            p = Participation(
                user_id=current_user.id,
                parasha_id=parasha.id,
                score=total_score,
                is_eligible=percentage >= 70
            )
            db.session.add(p)
            db.session.commit()
            
        flash(translate('already_participated', g.locale), 'info')
        # TODO: Instead of index, maybe a result/status page
        return redirect(url_for('main.index'))
    
    # Shuffle and pick a random sample (e.g., 5 questions)
    # If there are fewer than 5, show all.
    num_to_show = 5
    if len(questions) > num_to_show:
        questions = random.sample(questions, num_to_show)
    else:
        random.shuffle(questions)
    
    # For each question, prepare a shuffled list of options
    shuffled_questions = []
    for q in questions:
        options = [
            {'id': 'a', 'text_es': q.option_a_es, 'text_en': q.option_a_en, 'text_he': q.option_a_he},
            {'id': 'b', 'text_es': q.option_b_es, 'text_en': q.option_b_en, 'text_he': q.option_b_he},
            {'id': 'c', 'text_es': q.option_c_es, 'text_en': q.option_c_en, 'text_he': q.option_c_he}
        ]
        random.shuffle(options)
        shuffled_questions.append({
            'id': q.id,
            'text_es': q.text_es,
            'text_en': q.text_en,
            'text_he': q.text_he,
            'options': options
        })
    
    # Get donations for this parasha to show dedications
    dedications = Donation.query.filter_by(parasha_id=parasha.id, status='confirmed').all()
    
    today_remaining = max(0, 5 - today_parasha_answers)
    
    return render_template('user/participate.html', 
                          parasha=parasha, 
                          questions=shuffled_questions, 
                          dedications=dedications,
                          today_remaining=today_remaining)

@user_routes.route('/submit_quiz', methods=['POST'])
@login_required
def submit_quiz():
    parasha_id = request.form.get('parasha_id')
    parasha = Parasha.query.get(parasha_id)
    questions = parasha.questions
    
    new_correct_count = 0
    results_detail = []
    
    for q in questions:
        user_answer_id = request.form.get(f'q_{q.id}')
        if not user_answer_id:
            continue  # Skip unanswered in this session
            
        # Check if already answered (safety)
        already = UserAnswer.query.filter_by(user_id=current_user.id, question_id=q.id).first()
        if already: continue

        is_correct = False
        if user_answer_id and q.correct_option and user_answer_id.strip().lower() == q.correct_option.strip().lower():
            is_correct = True
            new_correct_count += 1
            current_user.points += 1 # ADD POINTS
        
        # Save individual answer
        ua = UserAnswer(
            user_id=current_user.id,
            question_id=q.id,
            is_correct=is_correct
        )
        db.session.add(ua)
        
        # Feedback data
        correct_text_es = getattr(q, f'option_{q.correct_option}_es')
        correct_text_en = getattr(q, f'option_{q.correct_option}_en')
        correct_text_he = getattr(q, f'option_{q.correct_option}_he')
        
        user_text_es = getattr(q, f'option_{user_answer_id}_es')
        user_text_en = getattr(q, f'option_{user_answer_id}_en')
        user_text_he = getattr(q, f'option_{user_answer_id}_he')

        results_detail.append({
            'question_es': q.text_es,
            'question_en': q.text_en,
            'question_he': q.text_he,
            'is_correct': is_correct,
            'user_answer_es': user_text_es,
            'user_answer_en': user_text_en,
            'user_answer_he': user_text_he,
            'correct_answer_es': correct_text_es,
            'correct_answer_en': correct_text_en,
            'correct_answer_he': correct_text_he
        })
    
    db.session.commit()

    # Check how many total answered now
    total_answered = UserAnswer.query.join(Question).filter(
        UserAnswer.user_id == current_user.id,
        Question.parasha_id == parasha.id
    ).count()
    
    total_parasha_q = len(parasha.questions)
    
    if total_answered == total_parasha_q:
        # Finished all! Create/Update participation record
        all_ans = UserAnswer.query.join(Question).filter(
            UserAnswer.user_id == current_user.id,
            Question.parasha_id == parasha.id
        ).all()
        total_score = sum(1 for a in all_ans if a.is_correct)
        percentage = (total_score / total_parasha_q * 100)
        is_eligible = percentage >= 70
        
        participation = Participation.query.filter_by(user_id=current_user.id, parasha_id=parasha.id).first()
        if not participation:
            participation = Participation(
                user_id=current_user.id,
                parasha_id=parasha_id,
                score=total_score,
                is_eligible=is_eligible
            )
            db.session.add(participation)
        else:
            participation.score = total_score
            participation.is_eligible = is_eligible
            
        db.session.commit()
        
        return render_template('user/result.html', 
                               score=total_score, 
                               total=total_parasha_q, 
                               percentage=percentage, 
                               is_eligible=is_eligible,
                               results_detail=results_detail,
                               finished=True)
    flash(f"¡Has respondido {len(results_detail)} preguntas! Tus puntos se han guardado. Vuelve luego para completar el resto.", "success")
    return redirect(url_for('main.index'))

@user_routes.route('/halajot')
@login_required
def halajot():
    from ..halaja_bank import HALAJA_BANK
    import random
    
    # Ensure categories exist with full data (icons and translations)
    default_cats = [
        {'es': 'Shabat', 'en': 'Shabbat', 'he': 'שבת', 'icon': '🕯️'},
        {'es': 'Kashrut (Carne y Leche)', 'en': 'Kashrut (Meat & Milk)', 'he': 'כשרות', 'icon': '🍷'},
        {'es': 'Tefilá', 'en': 'Prayer', 'he': 'תפילה', 'icon': '🙏'},
        {'es': 'Festividades', 'en': 'Holidays', 'he': 'חגים', 'icon': '🍷'},
        {'es': 'Leyes Generales', 'en': 'General Laws', 'he': 'הלכות כלליות', 'icon': '📜'}
    ]

    for cat_data in default_cats:
        cat = HalajaCategory.query.filter_by(name_es=cat_data['es']).first()
        if not cat:
            cat = HalajaCategory(
                name_es=cat_data['es'], 
                name_en=cat_data['en'], 
                name_he=cat_data['he'], 
                icon=cat_data['icon']
            )
            db.session.add(cat)
        else:
            # Update icons/names if they are missing
            if not cat.icon: cat.icon = cat_data['icon']
            if not cat.name_he: cat.name_he = cat_data['he']
            if not cat.name_en: cat.name_en = cat_data['en']
    
    db.session.commit()
    categories = HalajaCategory.query.all()

    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # DYNAMIC GENERATION: Ensure each user has 2 new questions available
    for cat in categories:
        # How many questions has this user answered in this category TODAY?
        today_cat_answers = HalajaAnswer.query.join(HalajaQuestion).filter(
            HalajaAnswer.user_id == current_user.id,
            HalajaQuestion.category_id == cat.id,
            HalajaAnswer.timestamp >= today_start
        ).count()

        # How many questions has this user NOT answered in this category?
        unanswered_count = HalajaQuestion.query.filter_by(category_id=cat.id).filter(
            ~HalajaQuestion.id.in_(db.session.query(HalajaAnswer.question_id).filter_by(user_id=current_user.id))
        ).count()
        
        if unanswered_count < 2 and today_cat_answers < 2:
            # Generate 2 NEW instances from Bank
            seed_pool = [q for q in HALAJA_BANK if q['category'] == cat.name_es or q['category'] == cat.name_en]
            if not seed_pool: seed_pool = HALAJA_BANK
            
            # Filter out questions already in the DB for this category (answered or not)
            existing_texts = db.session.query(HalajaQuestion.text_es).filter_by(category_id=cat.id).all()
            existing_texts = [et[0] for et in existing_texts]
            
            fresh_seeds = [s for s in seed_pool if s['t_es'] not in existing_texts]
            if not fresh_seeds: fresh_seeds = seed_pool # Recycle bank if all have been used at least once
            
            # Add exactly what's needed to reach 2 unanswered
            needed = 2 - unanswered_count
            to_add = random.sample(fresh_seeds, min(needed, len(fresh_seeds)))
            
            for q_data in to_add:
                new_q = HalajaQuestion(
                    category_id=cat.id,
                    text_es=q_data['t_es'], text_en=q_data['t_en'], text_he=q_data['t_he'],
                    option_a_es=q_data['a_es'], option_a_en=q_data['a_en'], option_a_he=q_data['a_he'],
                    option_b_es=q_data['b_es'], option_b_en=q_data['b_en'], option_b_he=q_data['b_he'],
                    option_c_es=q_data['c_es'], option_c_en=q_data['c_en'], option_c_he=q_data['c_he'],
                    correct_option='a'
                )
                db.session.add(new_q)
    
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # Refetch categories and stats
    categories = HalajaCategory.query.all()
    # Count progress for each category
    stats = []
    for cat in categories:
        total_q = HalajaQuestion.query.filter_by(category_id=cat.id).count()
        answered_q = HalajaAnswer.query.join(HalajaQuestion).filter(
            HalajaAnswer.user_id == current_user.id,
            HalajaQuestion.category_id == cat.id
        ).count()
        
        # Daily limit count
        today_cat_answers = HalajaAnswer.query.join(HalajaQuestion).filter(
            HalajaAnswer.user_id == current_user.id,
            HalajaQuestion.category_id == cat.id,
            HalajaAnswer.timestamp >= today_start
        ).count()
        
        stats.append({
            'cat': cat,
            'total': total_q,
            'answered': answered_q,
            'percentage': (answered_q / total_q * 100) if total_q > 0 else 0,
            'today_remaining': max(0, 2 - today_cat_answers)
        })
    return render_template('user/halajot_list.html', stats=stats)

@user_routes.route('/halajot/<int:category_id>')
@login_required
def halajot_quiz(category_id):
    import random
    category = HalajaCategory.query.get_or_404(category_id)
    
    # Check daily limit for this category
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_cat_answers = HalajaAnswer.query.join(HalajaQuestion).filter(
        HalajaAnswer.user_id == current_user.id,
        HalajaQuestion.category_id == category_id,
        HalajaAnswer.timestamp >= today_start
    ).count()

    if today_cat_answers >= 2:
        flash("Ya has respondido tus 2 preguntas diarias para esta categoría. ¡Vuelve mañana!", "info")
        return redirect(url_for('user.halajot'))

    # Get questions not already answered
    answered_ids = [ha.question_id for ha in HalajaAnswer.query.filter_by(user_id=current_user.id).all()]
    questions = HalajaQuestion.query.filter_by(category_id=category_id).filter(HalajaQuestion.id.notin_(answered_ids)).all()
    
    if not questions:
        flash(translate('already_participated', g.locale), 'info')
        return redirect(url_for('user.halajot'))
    
    # Shuffle and prepare
    random.shuffle(questions)
    shuffled_questions = []
    for q in questions[:2]: # Limit to 2 per category as requested
        opts = [
            {'id': 'a', 'text_es': q.option_a_es, 'text_en': q.option_a_en, 'text_he': q.option_a_he},
            {'id': 'b', 'text_es': q.option_b_es, 'text_en': q.option_b_en, 'text_he': q.option_b_he},
            {'id': 'c', 'text_es': q.option_c_es, 'text_en': q.option_c_en, 'text_he': q.option_c_he}
        ]
        random.shuffle(opts)
        shuffled_questions.append({
            'id': q.id,
            'text_es': q.text_es,
            'text_en': q.text_en,
            'text_he': q.text_he,
            'options': opts
        })
        
    return render_template('user/halajot_quiz.html', category=category, questions=shuffled_questions)

@user_routes.route('/submit_halaja', methods=['POST'])
@login_required
def submit_halaja():
    category_id = request.form.get('category_id')
    category = HalajaCategory.query.get(category_id)
    
    results_detail = []
    correct_in_this_run = 0
    total_in_this_run = 0
    
    for key in request.form:
        if key.startswith('q_'):
            q_id = int(key.split('_')[1])
            user_answer_id = request.form.get(key)
            
            q = HalajaQuestion.query.get(q_id)
            if not q: continue
            
            # Double check if already answered
            already = HalajaAnswer.query.filter_by(user_id=current_user.id, question_id=q_id).first()
            if already: continue
            
            is_correct = (user_answer_id == q.correct_option)
            total_in_this_run += 1
            if is_correct:
                correct_in_this_run += 1
                current_user.points += 2
            
            ans = HalajaAnswer(user_id=current_user.id, question_id=q_id, is_correct=is_correct)
            db.session.add(ans)
            
            # Feedback data
            correct_text_es = getattr(q, f'option_{q.correct_option}_es')
            correct_text_en = getattr(q, f'option_{q.correct_option}_en')
            correct_text_he = getattr(q, f'option_{q.correct_option}_he')
            
            user_text_es = getattr(q, f'option_{user_answer_id}_es')
            user_text_en = getattr(q, f'option_{user_answer_id}_en')
            user_text_he = getattr(q, f'option_{user_answer_id}_he')

            results_detail.append({
                'question_es': q.text_es,
                'question_en': q.text_en,
                'question_he': q.text_he,
                'is_correct': is_correct,
                'user_answer_es': user_text_es,
                'user_answer_en': user_text_en,
                'user_answer_he': user_text_he,
                'correct_answer_es': correct_text_es,
                'correct_answer_en': correct_text_en,
                'correct_answer_he': correct_text_he
            })
            
    db.session.commit()
    
    return render_template('user/result.html', 
                            score=correct_in_this_run, 
                            total=total_in_this_run, 
                            percentage=(correct_in_this_run/total_in_this_run*100) if total_in_this_run > 0 else 0,
                            is_eligible=True,
                            results_detail=results_detail,
                            finished=True,
                            is_halaja=True)

@user_routes.route('/profile')
@login_required
def profile():
    # Points breakdown
    parasha_answers = UserAnswer.query.filter_by(user_id=current_user.id, is_correct=True).count()
    halaja_answers = HalajaAnswer.query.filter_by(user_id=current_user.id, is_correct=True).count()
    
    # History of points
    history = []
    
    # Parasha points (1 pt each)
    p_answers = UserAnswer.query.filter_by(user_id=current_user.id).order_by(UserAnswer.timestamp.desc()).all()
    for a in p_answers:
        history.append({
            'date': a.timestamp,
            'type': 'Parashá',
            'detail': a.question.parasha.name_es,
            'points': 1 if a.is_correct else 0,
            'status': 'Correcta' if a.is_correct else 'Incorrecta'
        })
        
    # Halaja points (2 pts each)
    h_answers = HalajaAnswer.query.filter_by(user_id=current_user.id).order_by(HalajaAnswer.timestamp.desc()).all()
    for ha in h_answers:
        history.append({
            'date': ha.timestamp,
            'type': 'Halajá',
            'detail': ha.question.category.name_es,
            'points': 2 if ha.is_correct else 0,
            'status': 'Correcta' if ha.is_correct else 'Incorrecta'
        })
        
    # Sort history by date desc
    history.sort(key=lambda x: x['date'], reverse=True)
    
    return render_template('user/profile.html', 
                           parasha_points=parasha_answers, 
                           halaja_points=halaja_answers * 2,
                           history=history[:50]) # Show last 50 events
