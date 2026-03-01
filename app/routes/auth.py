from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, session, g
import random
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from ..models import User
from .. import db, login_manager, mail
from ..translations import translate

auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def send_verification_email(user):
    msg = Message(translate('verify_email_subject', user.language),
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[user.email])
    
    msg.body = f"{translate('verify_email_body', user.language)}: {user.verification_code}"
    mail.send(msg)

def send_reset_email(user):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = s.dumps(user.email, salt='reset-password-salt')
    msg = Message('Restablecer Contraseña - Shavua BeShavua',
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[user.email])
    
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    
    msg.body = f'''Para restablecer tu contraseña, haz clic en el siguiente enlace:
{reset_url}

Si no solicitaste este cambio, simplemente ignora este correo.
'''
    mail.send(msg)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        identifier = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        user = User.query.filter((User.email == identifier) | (User.username == identifier)).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=remember)
            return redirect(url_for('main.index'))
        flash(translate('invalid_login', g.locale), 'danger')
    return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone')
        has_whatsapp = True if request.form.get('has_whatsapp') else False
        
        user = User.query.filter((User.email == email) | (User.username == username)).first()
        if user:
            flash(translate('user_exists', g.locale), 'warning')
            return redirect(url_for('auth.signup'))
        
        verification_code = str(random.randint(100000, 999999))
        
        new_user = User(
            email=email, 
            username=username, 
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            has_whatsapp=has_whatsapp,
            password=generate_password_hash(password, method='scrypt'),
            language=session.get('lang', 'es'),
            verification_code=verification_code,
            is_verified=False
        )
        db.session.add(new_user)
        db.session.commit()
        
        try:
            send_verification_email(new_user)
            flash(translate('verification_sent', g.locale), 'info')
        except Exception as e:
            print(f"Error sending verification: {e}")
            flash('Error sending verification email.', 'danger')

        session['verify_user_id'] = new_user.id
        return redirect(url_for('auth.verify_email'))
    return render_template('signup.html')

@auth.route('/verify_email', methods=['GET', 'POST'])
def verify_email():
    user_id = session.get('verify_user_id')
    if not user_id:
        return redirect(url_for('auth.signup'))
    
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('auth.signup'))

    if request.method == 'POST':
        code = request.form.get('code')
        if code == user.verification_code:
            user.is_verified = True
            user.verification_code = None
            db.session.commit()
            login_user(user)
            session.pop('verify_user_id', None)
            flash(translate('account_verified', g.locale), 'success')
            return redirect(url_for('main.index'))
        else:
            flash(translate('invalid_code', g.locale), 'danger')
            
    return render_template('verify_email.html', email=user.email)

@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        email = request.form.get('email')
        print(f"DEBUG: Intentando recuperar contraseña para: {email}")
        user = User.query.filter_by(email=email).first()
        if user:
            print(f"DEBUG: Usuario encontrado: {user.username}. Enviando email...")
            try:
                send_reset_email(user)
                flash(translate('reset_email_sent', g.locale), 'info')
            except Exception as e:
                print(f"DEBUG: Error al enviar email: {str(e)}")
                flash(f'Error al enviar el correo: {str(e)}')
            return redirect(url_for('auth.login'))
        else:
            print(f"DEBUG: Usuario NO encontrado para el email: {email}")
            flash(translate('email_not_found', g.locale), 'warning')
    return render_template('forgot_password.html')

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='reset-password-salt', max_age=3600)
    except SignatureExpired:
        flash('El enlace ha expirado.')
        return redirect(url_for('auth.forgot_password'))
    except:
        flash('Enlace inválido.')
        return redirect(url_for('auth.forgot_password'))
        
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('Usuario no encontrado.')
        return redirect(url_for('auth.forgot_password'))
        
    if request.method == 'POST':
        password = request.form.get('password')
        user.password = generate_password_hash(password, method='scrypt')
        db.session.commit()
        flash('Tu contraseña ha sido actualizada.')
        return redirect(url_for('auth.login'))
        
    return render_template('reset_password.html', token=token)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
