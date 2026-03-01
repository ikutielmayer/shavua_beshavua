from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import User, Parasha, Question, Donation, GlobalSetting, RaffleResult, Participation, Advertisement
from .. import db
from datetime import datetime, timedelta

admin = Blueprint('admin', __name__)

@admin.before_request
@login_required
def assure_admin():
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('main.index'))

@admin.route('/dashboard')
def dashboard():
    parashot = Parasha.query.order_by(Parasha.week_end.asc()).all()
    donations = Donation.query.order_by(Donation.status.desc(), Donation.timestamp.desc()).all()
    users = User.query.order_by(User.role.asc(), User.username.asc()).all()
    
    # Settings for Commission
    commission_setting = GlobalSetting.query.filter_by(key='platform_commission_pct').first()
    if not commission_setting:
        commission_setting = GlobalSetting(key='platform_commission_pct', value='20', description='Platform commission percentage')
        db.session.add(commission_setting)
        db.session.commit()
    
    commission_pct = float(commission_setting.value) / 100.0
    total_confirmed = db.session.query(db.func.sum(Donation.amount)).filter_by(status='confirmed').scalar() or 0
    total_commission = total_confirmed * commission_pct
    
    # Settings for Raffle
    raffle_interval = GlobalSetting.query.filter_by(key='raffle_interval_parashot').first()
    if not raffle_interval:
        raffle_interval = GlobalSetting(key='raffle_interval_parashot', value='4', description='Number of parashot between raffles')
        db.session.add(raffle_interval)
        db.session.commit()
        
    last_raffle_date = GlobalSetting.query.filter_by(key='last_raffle_date').first()
    if not last_raffle_date:
        last_raffle_date = GlobalSetting(key='last_raffle_date', value=datetime.now().strftime('%Y-%m-%d'), description='Date of last raffle')
        db.session.add(last_raffle_date)
        db.session.commit()

    # Ad Revenue Calculation (Current Month)
    first_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    total_ad_revenue = db.session.query(db.func.sum(Advertisement.amount_paid)).filter(
        Advertisement.timestamp >= first_of_month
    ).scalar() or 0

    return render_template('admin/dashboard.html', 
                          parashot=parashot, 
                          donations=donations, 
                          users=users,
                          total_confirmed=total_confirmed,
                          total_commission=total_commission,
                          raffle_interval=raffle_interval.value,
                          last_raffle_date=last_raffle_date.value,
                          commission_pct=commission_setting.value,
                          total_ad_revenue=total_ad_revenue)

@admin.route('/update_settings', methods=['POST'])
def update_settings():
    comm_pct = request.form.get('commission_pct')
    raf_int = request.form.get('raffle_interval')
    
    if comm_pct:
        s = GlobalSetting.query.filter_by(key='platform_commission_pct').first()
        s.value = comm_pct
    if raf_int:
        s = GlobalSetting.query.filter_by(key='raffle_interval_parashot').first()
        s.value = raf_int
        
    db.session.commit()
    flash('Configuraciones actualizadas.', 'success')
    return redirect(url_for('admin.dashboard'))

@admin.route('/manage_ads')
def manage_ads():
    ads = Advertisement.query.order_by(Advertisement.timestamp.desc()).all()
    return render_template('admin/manage_ads.html', ads=ads)

@admin.route('/add_ad', methods=['GET', 'POST'])
def add_ad():
    if request.method == 'POST':
        ad = Advertisement(
            title=request.form.get('title'),
            line_1=request.form.get('line_1'),
            line_2=request.form.get('line_2'),
            line_3=request.form.get('line_3'),
            line_4=request.form.get('line_4'),
            address=request.form.get('address'),
            phone=request.form.get('phone'),
            image_url=request.form.get('image_url'),
            link_url=request.form.get('link_url'),
            position=request.form.get('position'),
            amount_paid=float(request.form.get('amount_paid', 0)),
            start_date=datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date(),
            end_date=datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
        )
        db.session.add(ad)
        db.session.commit()
        flash('Publicidad agregada con éxito.', 'success')
        return redirect(url_for('admin.manage_ads'))
    return render_template('admin/add_ad.html')

@admin.route('/edit_ad/<int:ad_id>', methods=['GET', 'POST'])
def edit_ad(ad_id):
    ad = Advertisement.query.get_or_404(ad_id)
    if request.method == 'POST':
        ad.title = request.form.get('title')
        ad.line_1 = request.form.get('line_1')
        ad.line_2 = request.form.get('line_2')
        ad.line_3 = request.form.get('line_3')
        ad.line_4 = request.form.get('line_4')
        ad.address = request.form.get('address')
        ad.phone = request.form.get('phone')
        ad.image_url = request.form.get('image_url')
        ad.link_url = request.form.get('link_url')
        ad.position = request.form.get('position')
        ad.amount_paid = float(request.form.get('amount_paid', 0))
        ad.start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
        ad.end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
        
        db.session.commit()
        flash('Publicidad actualizada correctamente.', 'success')
        return redirect(url_for('admin.manage_ads'))
    return render_template('admin/edit_ad.html', ad=ad)

@admin.route('/delete_ad/<int:ad_id>', methods=['POST'])
def delete_ad(ad_id):
    ad = Advertisement.query.get_or_404(ad_id)
    db.session.delete(ad)
    db.session.commit()
    flash('Publicidad eliminada.', 'info')
    return redirect(url_for('admin.manage_ads'))

@admin.route('/perform_raffle', methods=['POST'])
def perform_raffle():
    import random
    # 1. Calculate Prize Pool based on settings
    comm_setting = GlobalSetting.query.filter_by(key='platform_commission_pct').first()
    comm_pct = float(comm_setting.value) / 100.0 if comm_setting else 0.2
    
    last_raffle_setting = GlobalSetting.query.filter_by(key='last_raffle_date').first()
    last_raffle_date = datetime.strptime(last_raffle_setting.value, '%Y-%m-%d') if last_raffle_setting else datetime(2000,1,1)

    total_confirmed = db.session.query(db.func.sum(Donation.amount))\
        .filter(Donation.status == 'confirmed')\
        .filter(Donation.timestamp >= last_raffle_date)\
        .scalar() or 0
        
    prize_amount = total_confirmed * (1.0 - comm_pct)
    
    # 2. Get eligible users
    eligible_participants = User.query.filter(User.is_verified == True, User.points > 0).all()
    
    if not eligible_participants:
        flash('No hay participantes elegibles para el sorteo.', 'warning')
        return redirect(url_for('admin.dashboard'))
        
    winner = random.choice(eligible_participants)
    
    # 3. Record Raffle Result
    result = RaffleResult(
        winner_id=winner.id,
        amount=prize_amount,
        parashot_included="Periodo automático"
    )
    db.session.add(result)
    
    # 4. RESET POINTS
    User.query.update({User.points: 0})
    
    # 5. Update last raffle date
    if last_raffle_setting:
        last_raffle_setting.value = datetime.now().strftime('%Y-%m-%d')
    
    db.session.commit()
    
    flash(f'¡Sorteo realizado! Ganador: {winner.username}. Premio: ${prize_amount:.2f}', 'success')
    return redirect(url_for('admin.dashboard'))

@admin.route('/users')
def list_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.role = request.form.get('role')
        user.points = int(request.form.get('points', 0))
        
        db.session.commit()
        flash(f'Usuario {user.username} actualizado correctamente.', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/edit_user.html', user=user)

@admin.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if current_user.id == user_id:
        flash('No puedes eliminarte a ti mismo.', 'danger')
        return redirect(url_for('admin.dashboard'))
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f'Usuario {user.username} eliminado.', 'warning')
    return redirect(url_for('admin.dashboard'))

@admin.route('/confirm_donation/<int:donation_id>')
def confirm_donation(donation_id):
    d = Donation.query.get_or_404(donation_id)
    d.status = 'confirmed'
    db.session.commit()
    flash('¡Donación confirmada con éxito!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin.route('/delete_donation/<int:donation_id>', methods=['POST'])
def delete_donation(donation_id):
    d = Donation.query.get_or_404(donation_id)
    db.session.delete(d)
    db.session.commit()
    flash('Donación eliminada.', 'info')
    return redirect(url_for('admin.dashboard'))

@admin.route('/add_parasha', methods=['GET', 'POST'])
def add_parasha():
    if request.method == 'POST':
        name_es = request.form.get('name_es')
        name_en = request.form.get('name_en')
        name_he = request.form.get('name_he')
        start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d')
        end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d')
        
        parasha = Parasha(name_es=name_es, name_en=name_en, name_he=name_he, week_start=start_date, week_end=end_date)
        db.session.add(parasha)
        db.session.commit()
        
        flash('Parasha added!')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/add_parasha.html')

@admin.route('/add_question/<int:parasha_id>', methods=['GET', 'POST'])
def add_question(parasha_id):
    if request.method == 'POST':
        q = Question(
            parasha_id=parasha_id,
            text_es=request.form.get('text_es'),
            text_en=request.form.get('text_en'),
            text_he=request.form.get('text_he'),
            option_a_es=request.form.get('a_es'),
            option_a_en=request.form.get('a_en'),
            option_a_he=request.form.get('a_he'),
            option_b_es=request.form.get('b_es'),
            option_b_en=request.form.get('b_en'),
            option_b_he=request.form.get('b_he'),
            option_c_es=request.form.get('c_es'),
            option_c_en=request.form.get('c_en'),
            option_c_he=request.form.get('c_he'),
            correct_option=request.form.get('correct')
        )
        db.session.add(q)
        db.session.commit()
        flash('Question added!')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/add_question.html', parasha_id=parasha_id)

@admin.route('/edit_question/<int:question_id>', methods=['GET', 'POST'])
def edit_question(question_id):
    q = Question.query.get_or_404(question_id)
    if request.method == 'POST':
        q.text_es = request.form.get('text_es')
        q.text_en = request.form.get('text_en')
        q.text_he = request.form.get('text_he')
        q.option_a_es = request.form.get('a_es')
        q.option_a_en = request.form.get('a_en')
        q.option_a_he = request.form.get('a_he')
        q.option_b_es = request.form.get('b_es')
        q.option_b_en = request.form.get('b_en')
        q.option_b_he = request.form.get('b_he')
        q.option_c_es = request.form.get('c_es')
        q.option_c_en = request.form.get('c_en')
        q.option_c_he = request.form.get('c_he')
        q.correct_option = request.form.get('correct')
        
        db.session.commit()
        flash('Pregunta actualizada correctamente.', 'success')
        return redirect(url_for('admin.manage_questions', parasha_id=q.parasha_id))
    return render_template('admin/edit_question.html', q=q)

@admin.route('/delete_question/<int:question_id>', methods=['POST'])
def delete_question(question_id):
    q = Question.query.get_or_404(question_id)
    parasha_id = q.parasha_id
    db.session.delete(q)
    db.session.commit()
    flash('Pregunta eliminada.', 'warning')
    return redirect(url_for('admin.manage_questions', parasha_id=parasha_id))

@admin.route('/manage_questions/<int:parasha_id>')
def manage_questions(parasha_id):
    parasha = Parasha.query.get_or_404(parasha_id)
    return render_template('admin/manage_questions.html', parasha=parasha)

@admin.route('/add_donation', methods=['GET', 'POST'])
def add_donation():
    if request.method == 'POST':
        from .main import get_current_parasha_internal
        current_p = get_current_parasha_internal()
        
        d = Donation(
            donor_name=request.form.get('donor_name'),
            amount=float(request.form.get('amount')),
            donation_type=request.form.get('type'),
            recipient_name=request.form.get('recipient'),
            status='confirmed',
            parasha_id=current_p.id if current_p else None
        )
        db.session.add(d)
        db.session.commit()
        flash('Donación registrada manualmente con éxito.', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/add_donation.html')
