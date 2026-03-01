from flask import Blueprint, render_template, request, g, flash, redirect, url_for, session
from flask_login import current_user
from ..models import Donation, Participation, Parasha, User, RaffleResult, GlobalSetting, Advertisement
from .. import db, mail
from flask_mail import Message
from datetime import datetime, time, timedelta
import pytz
import os
from ..translations import translate

main = Blueprint('main', __name__)

def is_shabbat():
    # Placeholder for Shabbat check
    now = datetime.now()
    weekday = now.weekday() # 4 is Friday, 5 is Saturday
    if weekday == 4 and now.time() >= time(17, 30):
        return True
    if weekday == 5 and now.time() <= time(20, 30):
        return True
    return False

def get_current_parasha_internal():
    now = datetime.now()
    weekday = now.weekday()
    
    # Calculate target Saturday for the Parasha
    # From Motzei Shabbat (Saturday 20:30) until Friday, we show the coming Shabbat's Parasha
    days_to_saturday = (5 - weekday) % 7
    if weekday == 5 and now.time() >= time(20, 30):
        days_to_saturday = 7
    
    target_saturday = (now + timedelta(days=days_to_saturday)).date()
    
    # Find Parasha associated with that Saturday
    parasha = Parasha.query.filter(Parasha.week_end >= target_saturday).order_by(Parasha.week_end.asc()).first()
    return parasha

@main.before_app_request
def check_shabbat():
    if is_shabbat():
        if request.endpoint and 'static' not in request.endpoint:
            return render_template('shabbat.html'), 503

@main.route('/report_donation', methods=['POST'])
def report_donation():
    donor_name = request.form.get('donor_name')
    amount_str = request.form.get('amount')
    amount = float(amount_str) if amount_str else 0
    donation_type = request.form.get('type')
    recipient = request.form.get('recipient')
    duration_type = request.form.get('duration_type', 'single')  # single, monthly, yearly, specific
    
    # Determine which parashot to assign
    selected_parasha_ids = request.form.getlist('parasha_ids')  # multiple specific parashot
    
    current_p = get_current_parasha_internal()

    donations_created = []

    if duration_type == 'single':
        # One donation for the current parasha
        d = Donation(
            donor_name=donor_name, amount=amount,
            donation_type=donation_type, recipient_name=recipient,
            status='pending', duration_type='single', weeks_count=1,
            parasha_id=current_p.id if current_p else None
        )
        db.session.add(d)
        donations_created.append(d)

    elif duration_type == 'specific' and selected_parasha_ids:
        # Split amount equally among selected parashot
        per_amount = round(amount / len(selected_parasha_ids), 2)
        for pid in selected_parasha_ids:
            d = Donation(
                donor_name=donor_name, amount=per_amount,
                donation_type=donation_type, recipient_name=recipient,
                status='pending', duration_type='specific', weeks_count=len(selected_parasha_ids),
                parasha_id=int(pid)
            )
            db.session.add(d)
            donations_created.append(d)

    elif duration_type == 'monthly':
        # Get parashot for the next ~4 weeks
        from datetime import date, timedelta
        today = date.today()
        month_end = today + timedelta(weeks=4)
        monthly_parashot = Parasha.query.filter(
            Parasha.week_end >= today,
            Parasha.week_end <= month_end
        ).order_by(Parasha.week_end.asc()).all()
        if not monthly_parashot:
            monthly_parashot = [current_p] if current_p else []
        per_amount = round(amount / len(monthly_parashot), 2) if monthly_parashot else amount
        for p in monthly_parashot:
            d = Donation(
                donor_name=donor_name, amount=per_amount,
                donation_type=donation_type, recipient_name=recipient,
                status='pending', duration_type='monthly', weeks_count=len(monthly_parashot),
                parasha_id=p.id
            )
            db.session.add(d)
            donations_created.append(d)

    elif duration_type == 'yearly':
        # Get all parashot for the next 52 weeks
        from datetime import date, timedelta
        today = date.today()
        year_end = today + timedelta(weeks=52)
        yearly_parashot = Parasha.query.filter(
            Parasha.week_end >= today,
            Parasha.week_end <= year_end
        ).order_by(Parasha.week_end.asc()).all()
        if not yearly_parashot:
            yearly_parashot = [current_p] if current_p else []
        per_amount = round(amount / len(yearly_parashot), 2) if yearly_parashot else amount
        for p in yearly_parashot:
            d = Donation(
                donor_name=donor_name, amount=per_amount,
                donation_type=donation_type, recipient_name=recipient,
                status='pending', duration_type='yearly', weeks_count=len(yearly_parashot),
                parasha_id=p.id
            )
            db.session.add(d)
            donations_created.append(d)

    db.session.commit()
    
    # Send Email to Admin
    try:
        admin_email = os.getenv('ADMIN_EMAIL')
        if admin_email and donations_created:
            first_d = donations_created[0]
            msg = Message("Nueva Donación Informada - Shavua BeShavua",
                          recipients=[admin_email])
            
            motive_label = translate('leiluy_nishmat', g.locale) if donation_type == "le'iluy nishmat" else translate('refua', g.locale) if donation_type == 'refua' else translate('hazlaja', g.locale) if donation_type == 'hazlaja' else 'Otro'
            approve_url = url_for('admin.confirm_donation', donation_id=first_d.id, _external=True)
            
            duration_labels = {'single': 'Semana actual', 'monthly': 'Mensual (próx. 4 semanas)', 'yearly': 'Anual (próx. 52 semanas)', 'specific': f'{len(donations_created)} parashas específicas'}
            
            msg.body = f"""
            Se ha informado una nueva donación pendiente de aprobación:
            
            Donante: {donor_name}
            Monto Total: ${amount}
            Tipo de duración: {duration_labels.get(duration_type, duration_type)}
            Cantidad de recordes creados: {len(donations_created)}
            Motivo: {motive_label}
            Beneficiario: {recipient}
            
            Para aprobar la primera donación, haz clic aquí:
            {approve_url}
            
            (Deberás estar logueado como admin en tu navegador para que el enlace funcione directamente).
            """
            mail.send(msg)
    except Exception as e:
        print(f"Error enviando email: {e}")

    flash(translate('donation_report_success', g.locale), 'success')
    return redirect(url_for('main.donate'))

@main.route('/donate')
def donate():
    # Pass future parashot for specific choice
    future_parashot = Parasha.query.filter(Parasha.week_end >= datetime.now().date()).order_by(Parasha.week_end.asc()).limit(52).all()
    return render_template('donate.html', future_parashot=future_parashot)
@main.route('/')
def index():
    # Prize Pool Calculation: ONLY donations after the last raffle
    last_raffle_setting = GlobalSetting.query.filter_by(key='last_raffle_date').first()
    if last_raffle_setting:
        last_raffle_date = datetime.strptime(last_raffle_setting.value, '%Y-%m-%d')
    else:
        last_raffle_date = datetime(2026, 1, 1) # Default far back

    # Prize Pool Calculation
    comm_setting = GlobalSetting.query.filter_by(key='platform_commission_pct').first()
    comm_pct = float(comm_setting.value) / 100.0 if comm_setting else 0.2

    total_donated_period = db.session.query(db.func.sum(Donation.amount))\
        .filter(Donation.status == 'confirmed')\
        .filter(Donation.timestamp >= last_raffle_date)\
        .scalar() or 0
    prize_pool = total_donated_period * (1.0 - comm_pct)
    
    # Ads
    today = datetime.now().date()
    left_ads = Advertisement.query.filter(Advertisement.status == 'active', Advertisement.position == 'left', Advertisement.start_date <= today, Advertisement.end_date >= today).all()
    right_ads = Advertisement.query.filter(Advertisement.status == 'active', Advertisement.position == 'right', Advertisement.start_date <= today, Advertisement.end_date >= today).all()
    
    # Latest Raffle Winner
    latest_winner = RaffleResult.query.order_by(RaffleResult.timestamp.desc()).first()
    
    # Latest donations (global, but could be filtered)
    donations = Donation.query.filter_by(status='confirmed').order_by(Donation.timestamp.desc()).limit(5).all()
    
    # Mask donor names
    def mask_simple(name):
        if not name: return "Anónimo"
        parts = name.split()
        if len(parts) >= 2:
            return f"{parts[0][:2]}*** {parts[1][:2]}***"
        return f"{name[:2]}***"

    for d in donations:
        d.display_name = mask_simple(d.donor_name)

    # New stats
    total_donors = db.session.query(db.func.count(db.distinct(Donation.donor_name))).filter_by(status='confirmed').scalar() or 0
    total_participants = db.session.query(db.func.count(User.id)).filter(User.role == 'participant').scalar() or 0
    
    current_parasha = get_current_parasha_internal()
    
    # Recent Participations
    recent_participations = db.session.query(Participation, User).join(User).order_by(Participation.timestamp.desc()).limit(10).all()
    
    processed_participations = []
    for p, user in recent_participations:
        # Calculate percentage
        total_q = Parasha.query.get(p.parasha_id).questions
        count_q = len(total_q)
        percentage = (p.score / count_q * 100) if count_q > 0 else 0
        
        # Format masked name
        fname = user.first_name or user.username
        lname = user.last_name or ""
        masked = f"{fname[:2]}*** {lname[:2]}***" if lname else f"{fname[:2]}***"
        
        processed_participations.append({
            'masked_user': masked,
            'percentage': int(percentage),
            'timestamp': p.timestamp
        })

    return render_template('index.html', 
                          prize_pool=prize_pool, 
                          donations=donations,
                          total_donors=total_donors,
                          total_participants=total_participants,
                          current_parasha=current_parasha,
                          recent_participations=processed_participations,
                          latest_winner=latest_winner,
                          left_ads=left_ads,
                          right_ads=right_ads)
