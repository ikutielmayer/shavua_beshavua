from flask import Flask, request, g, session
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel
from flask_mail import Mail
from dotenv import load_dotenv
import os

load_dotenv()
from whitenoise import WhiteNoise

db = SQLAlchemy()
login_manager = LoginManager()
babel = Babel()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_shavua_beshavua')
    
    # DB URI Handling for Heroku (ClearDB/Postgres)
    db_url = os.getenv('DATABASE_URL') or os.getenv('CLEARDB_DATABASE_URL') or os.getenv('SQLALCHEMY_DATABASE_URI')
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Enable WhiteNoise
    app.wsgi_app = WhiteNoise(app.wsgi_app, root='app/static/', prefix='static/')
    
    # Mail Config
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    babel.init_app(app, locale_selector=get_locale)
    mail.init_app(app)

    with app.app_context():
        # Import blueprints
        from .routes.auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)

        from .routes.main import main as main_blueprint
        app.register_blueprint(main_blueprint)

        from .routes.admin import admin as admin_blueprint
        app.register_blueprint(admin_blueprint, url_prefix='/admin')

        from .routes.user import user_routes as user_blueprint
        app.register_blueprint(user_blueprint)

        from .translations import translate
        @app.context_processor
        def inject_translate():
            return dict(translate=lambda key: translate(key, g.locale))

        @app.before_request
        def handle_locale():
            # 1. Manual selection in URL (?lang=...)
            target_lang = request.args.get('lang')
            if target_lang in ['es', 'en', 'he']:
                session['lang'] = target_lang
                if current_user.is_authenticated:
                    current_user.language = target_lang
                    db.session.commit()
            
            # 2. Check session
            if not session.get('lang'):
                # 3. Check user profile
                if current_user.is_authenticated and current_user.language:
                    session['lang'] = current_user.language
                else:
                    # 4. Auto-detect
                    detected = request.accept_languages.best_match(['es', 'en', 'he'])
                    session['lang'] = detected if detected else 'es'
            
            g.locale = session.get('lang', 'es')

        # Create tables
        db.create_all()

    return app

def get_locale():
    return session.get('lang') or request.accept_languages.best_match(['es', 'en', 'he']) or 'es'
